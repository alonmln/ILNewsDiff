import logging
import os
import time
from typing import Dict

from data_provider import DataProvider
from twitter_helper import upload_media, tweet_text, tweet_with_media
from image_diff_generator import ImageDiffGenerator

if 'TESTING' in os.environ:
    if os.environ['TESTING'] == 'False':
        TESTING = False
    else:
        TESTING = True
else:
    TESTING = True

MAX_RETRIES = 10
RETRY_DELAY = 3


class BaseParser:
    def __init__(self):
        self.data_provider = DataProvider()

    def parse(self):
        raise NotImplementedError

    def entry_to_dict(self, article):
        raise NotImplementedError

    def should_use_first_item_dedup(self):
        return NotImplementedError

    @staticmethod
    def get_source():
        raise NotImplementedError

    def get_integrity_validators(self):
        return []

    def get_tweet_validators(self):
        return []

    @staticmethod
    def validate(validators: list, url: str, old: str, new: str):
        for validator in validators:
            if not validator.validate_change(url, old, new):
                logging.info(
                    f"Detected error. old was \n{old}\n new was \n{new}\n url {url} type: {validator.__name__}")
                return False
        return True

    def tweet(self, text: str, article_id: str, url: str, image_path: str):
        image_id = upload_media(image_path)
        logging.info(f'Media ready with id: {image_id}')
        logging.info(f'Text to tweet: {text}')
        logging.info(f'Article id: {article_id}')
        reply_to = self.data_provider.get_previous_tweet_id(article_id, self.get_source())
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
        self.data_provider.update_tweet_db(article_id, self.get_source(), tweet_id)

    def store_data(self, data: Dict):
        if self.data_provider.is_article_tracked(data['article_id'], self.get_source()):
            count = self.data_provider.get_article_version_count(data[
                                                                     'article_id'], self.get_source(), data['hash'])
            if count != 1:  # Changed
                self.tweet_all_changes(data)
        else:
            self.data_provider.track_article(data)

    def tweet_change(self, previous_data: str, current_data: str, text_to_tweet: str, article_id: str, url: str):
        saved_image_diff_path = ImageDiffGenerator.generate_image_diff(previous_data, current_data, text_to_tweet)
        self.tweet(text_to_tweet, article_id, url, saved_image_diff_path)

    def tweet_all_changes(self, data: Dict):
        article_id = data['article_id']
        url = data['url']
        previous_version = self.data_provider.get_previous_article_version(article_id, self.get_source())

        save_to_db = False

        if self.validate(self.get_integrity_validators(), url, previous_version['title'], data['title']):
            save_to_db = True
            if self.should_tweet(url, previous_version['title'], data['title']):
                self.tweet_change(previous_version['title'], data['title'], "שינוי בכותרת", article_id, url)

        if self.validate(self.get_integrity_validators(), url, previous_version['abstract'], data['abstract']):
            save_to_db = True
            if self.should_tweet(url, previous_version['abstract'], data['abstract']):
                self.tweet_change(previous_version['abstract'], data['abstract'], "שינוי בכותרת משנה", article_id, url)

        if save_to_db:
            self.data_provider.increase_article_version(data)

    def should_tweet(self, url: str, previous_data: str, current_data: str):
        if len(previous_data) == 0 or len(current_data) == 0:
            return False
        if previous_data == current_data:
            return False
        if not self.validate(self.get_tweet_validators(), url, previous_data, current_data):
            return False

        return True

    def loop_entries(self, entries):
        articles = {}
        for article in entries:
            try:
                article_dict = self.entry_to_dict(article)
                if article_dict['article_id'] not in articles or not self.should_use_first_item_dedup():
                    articles[article_dict['article_id']] = article_dict
            except BaseException:
                logging.exception(f'Problem looping entry: {article}')
        for article_dict in articles.values():
            try:
                self.store_data(article_dict)
            except BaseException:
                logging.exception(f'Problem looping entry: {article_dict}')
