#!/bin/bash
export TESTING=True

export TWITTER_CONSUMER_KEY=""
export TWITTER_CONSUMER_SECRET=""
export TWITTER_ACCESS_TOKEN=""
export TWITTER_ACCESS_TOKEN_SECRET=""

export PHANTOMJS_PATH="/usr/local/bin/phantomjs"

export OPENSSL_CONF=/etc/ssl/

source venv/bin/activate
python main.py
deactivate
