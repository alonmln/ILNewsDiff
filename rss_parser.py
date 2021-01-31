import logging

import feedparser

from base_parser import BaseParser


class RSSParser(BaseParser):
    def __init__(self, rss_url):
        BaseParser.__init__(self)
        self.url = rss_url

    def parse(self):
        r = feedparser.parse(self.url)
        import urllib.request
        with urllib.request.urlopen(self.url) as response:
            data = response.read()
            import datetime
            with open(f"./{self.get_source()}_{str(datetime.datetime.now()).replace(':','')}.xml", "wb") as f:
                f.write(data)
        if r is None:
            logging.warning('Empty response RSS')
            return
        else:
            logging.info('Parsing %s', r.channel.title)
        self.loop_entries(r.entries)           
