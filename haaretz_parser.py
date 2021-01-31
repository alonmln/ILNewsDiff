import collections
import hashlib
from datetime import datetime

from base_parser import BaseParser
from html_utils import strip_html
from rss_parser import RSSParser
from validators import html_validator

HAARETZ_RSS = "https://www.haaretz.co.il/cmlink/1.1617539"


class HaaretzParser(RSSParser):
    def __init__(self, tz):
        RSSParser.__init__(self, HAARETZ_RSS)
        self.tz = tz

    @staticmethod
    def get_source():
        return "Haaretz"

    def should_use_first_item_dedup(self):
        return True

    def _validate_change(self, url: str, new: str):
        return html_validator(url, new)

    def entry_to_dict(self, article):
        article_dict = dict()
        article_dict['article_id'] = article.guid
        article_dict['article_source'] = self.get_source()
        article_dict['url'] = article.link
        article_dict['title'] = article.title
        article_dict['abstract'] = strip_html(article['description'])
        od = collections.OrderedDict(sorted(article_dict.items()))
        article_dict['hash'] = hashlib.sha224(
            repr(od.items()).encode('utf-8')).hexdigest()
        article_dict['date_time'] = datetime.now(self.tz)
        return article_dict

