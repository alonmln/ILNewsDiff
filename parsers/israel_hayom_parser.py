from parsers import parser_utils
from rss_parser import RSSParser
import validators.content_validator
import validators.israel_hayom_sports_validator

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

    def get_tweet_validators(self):
        return [validators.content_validator, validators.israel_hayom_sports_validator]

    def entry_to_dict(self, article):
        return parser_utils.standard_entry_to_dict(article, self.get_source(), self.tz)
