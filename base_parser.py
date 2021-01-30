import logging
import os
import time
from typing import Dict

import bleach
import requests

from data_provider import DataProvider
from twitter_helper import upload_media, tweet_text, tweet_with_media
from image_diff_generator import generate_image_diff

if 'TESTING' in os.environ:
    if os.environ['TESTING'] == 'False':
        TESTING = False
    else:
        TESTING = True
else:
    TESTING = True

MAX_RETRIES = 10
RETRY_DELAY = 3


class BaseParser():
    def __init__(self, api, phantomjs_path):
        self.phantomjs_path = phantomjs_path
        self.data_provider = DataProvider()

    def parse(self):
        raise NotImplemented

    def entry_to_dict(self, article):
        raise NotImplemented() 

    def tweet(self, text: str, article_id: str, url: str, image_path: str):
        image_id = upload_media(image_path)
        logging.info(f'Media ready with id: {image_id}')
        logging.info(f'Text to tweet: {text}')
        logging.info(f'Article id: {article_id}')
        reply_to = self.data_provider.get_previous_tweet_id(article_id)
        if reply_to is None:
            logging.info(f'Tweeting url: {url}')
            tweet = tweet_text(url)
            # if TESTING, give a random id based on time
            reply_to = tweet.id if not TESTING else time.time()
        logging.info(f'Replying to: {reply_to}')
        tweet = tweet_with_media(text, image_id, reply_to)
        # if TESTING, give a random id based on time
        tweet_id = time.time() if TESTING else tweet.id
        logging.info(f'Id to store: {tweet_id}')
        self.data_provider.update_tweet_db(article_id, tweet_id)

    @staticmethod
    def get_page(url, header=None, payload=None):
        r = None
        for x in range(MAX_RETRIES):
            try:
                r = requests.get(url=url, headers=header, params=payload)
            except BaseException as e:
                if x == MAX_RETRIES - 1:
                    print('Max retries reached')
                    logging.warning('Max retries for: %s', url)
                    return None
                if '104' not in str(e):
                    print('Problem with url {}'.format(url))
                    print('Exception: {}'.format(str(e)))
                    logging.exception('Problem getting page')
                    return None
                time.sleep(RETRY_DELAY)
            else:
                break
        return r

    @staticmethod
    def strip_html(html: str):
        """
        a wrapper for bleach.clean() that strips ALL tags from the input
        """
        tags = []
        attr = {}
        styles = []
        strip = True
        return bleach.clean(html,
                            tags=tags,
                            attributes=attr,
                            styles=styles,
                            strip=strip)

    def store_data(self, data: Dict):
        if self.data_provider.is_article_tracked(data['article_id']):
            count = self.data_provider.get_article_version_count(data[
                    'article_id'], data['hash'])
            if count != 1:  # Changed
                self.data_provider.add_article_version(data)
                self.tweet_all_changes(data)
        else:
            self.data_provider.track_article(data)

    def tweet_change(self, previous_data: str, current_data: str,
                        tweet_text: str, article_id: str, url: str):
        if len(previous_data) == 0 or len(current_data) == 0:
            logging.info('Old or New empty')
            return 
        if previous_data == current_data:
            return
        saved_image_diff_path = generate_image_diff(previous_data, current_data, self.phantomjs_path)
        self.tweet(tweet_text, article_id, url, saved_image_diff_path)

    def tweet_all_changes(self, data: Dict):
        article_id = data['article_id']
        url = data['url']
        previous_version = self.data_provider.get_previous_article_version(article_id)
        self.tweet_change(previous_version['title'], data['title'], "שינוי בכותרת", article_id, url)
        self.tweet_change(previous_version['abstract'], data['abstract'], "שינוי בתת כותרת", article_id, url)

    def loop_entries(self, entries):
        for article in entries:
            try:
                article_dict = self.entry_to_dict(article)
                current_ids = set()
                self.store_data(article_dict)
                current_ids.add(article_dict['article_id'])
                self.data_provider.remove_old(current_ids)
            except BaseException as e:
                logging.exception(f'Problem looping entry: {article}')
                print('Exception: {}'.format(str(e)))
                print('***************')
                print(article)
                print('***************')
