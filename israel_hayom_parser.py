import collections
import hashlib
from datetime import datetime

from base_parser import BaseParser
from rss_parser import RSSParser

ISRAEL_HAYOM_RSS = "https://www.israelhayom.co.il/rss.xml"


class IsraelHayomParser(RSSParser):
    def __init__(self, tz):
        RSSParser.__init__(self, ISRAEL_HAYOM_RSS)
        self.tz = tz

    @staticmethod
    def get_source():
        return "IsraelHayom"
        
    def should_use_first_item_dedup(self):
        return True

    def _validate_change(self, url: str, new: str):
        return BaseParser.html_validator(url, new)

    def entry_to_dict(self, article):
        article_dict = dict()
        article_dict['article_id'] = article.guid
        article_dict['article_source'] = self.get_source()
        article_dict['url'] = article.link
        article_dict['title'] = article.title
        article_dict['abstract'] = self._strip_html(article['description'])
        od = collections.OrderedDict(sorted(article_dict.items()))
        article_dict['hash'] = hashlib.sha224(
            repr(od.items()).encode('utf-8')).hexdigest()
        article_dict['date_time'] = datetime.now(self.tz)
        return article_dict
