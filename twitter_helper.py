import os
import sys
import logging

import tweepy

consumer_key = os.environ.get('TWITTER_CONSUMER_KEY')
consumer_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
access_token = os.environ.get('TWITTER_ACCESS_TOKEN')
access_token_secret = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.secure = True
auth.set_access_token(access_token, access_token_secret)
twitter_api = tweepy.API(auth)

if 'TESTING' in os.environ:
    if os.environ['TESTING'] == 'False':
        TESTING = False
    else:
        TESTING = True
else:
    TESTING = True


def upload_media(filename):
    if TESTING:
        return 1
    try:
        response = twitter_api.media_upload(filename)
    except Exception:
        print(sys.exc_info()[0])
        logging.exception('Media upload')
        raise
    return response.media_id_string


def tweet_with_media(text: str, image_id: str, reply_to=None):
    logging.debug(f"Tweeting {text} with {image_id} in reply to {reply_to}")
    if TESTING:
        print(text, image_id, reply_to)
        return True
    try:
        update_tweet_params = {"status": text, "media_ids": [image_id]}
        if reply_to is not None:
            update_tweet_params["in_reply_to_status_id"] = reply_to
        tweet_id = twitter_api.update_status(**update_tweet_params)
    except Exception:
        logging.exception('Tweet with media failed')
        print(sys.exc_info()[0])
        return False
    return tweet_id


def tweet_text(text: str):
    if TESTING:
        print(text)
        return True
    try:
        tweet_id = twitter_api.update_status(status=text)
    except Exception:
        logging.exception('Tweet text failed')
        print(sys.exc_info()[0])
        return False
    return tweet_id
