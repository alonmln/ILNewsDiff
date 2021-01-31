import logging

import feedparser

from base_parser import BaseParser


class RSSParser(BaseParser):
    def __init__(self, rss_url):
        BaseParser.__init__(self)
        self.url = rss_url

    def parse(self):
        r = feedparser.parse(self.url)

        if r is None:
            logging.warning('Empty response RSS')
            return
        else:
            logging.info('Parsing %s', r.channel.title)
        self.loop_entries(r.entries)           
