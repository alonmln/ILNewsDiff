#!/bin/bash
export TESTING=True

export NYT_TWITTER_CONSUMER_KEY=""
export NYT_TWITTER_CONSUMER_SECRET=""
export NYT_TWITTER_ACCESS_TOKEN=""
export NYT_TWITTER_ACCESS_TOKEN_SECRET=""

export PHANTOMJS_PATH="/usr/local/bin/phantomjs"

export OPENSSL_CONF=/etc/ssl/

source venv/bin/activate
python main.py
deactivate
