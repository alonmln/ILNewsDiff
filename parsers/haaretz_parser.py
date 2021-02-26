import validators.html_validator
import validators.content_validator
import validators.haaretz_sports_validator
from parsers import parser_utils
from rss_parser import RSSParser

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

    def get_integrity_validators(self):
        return [validators.html_validator]

    def get_tweet_validators(self):
        return [validators.content_validator, validators.haaretz_sports_validator]

    def entry_to_dict(self, article):
        return parser_utils.standard_entry_to_dict(article, self.get_source(), self.tz)
