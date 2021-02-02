from pytz import timezone

import feedparser

import validators
from israel_hayom_parser import IsraelHayomParser as Parser

TIMEZONE = 'Israel'
LOCAL_TZ = timezone(TIMEZONE)


def main():
    parser = Parser(LOCAL_TZ)
    r = feedparser.parse(parser.url)

    if r is None:
        print("RSS was empty")
        return

    print(f"Checking {len(r.entries)} entries")
    for entry in r.entries[::-1]:
        entry_dict = parser.entry_to_dict(entry)
        url = entry_dict["url"]
        title = entry_dict["title"]
        description = entry_dict["abstract"]
        if not validators.validate_string_in_html(url, title):
            print(f"Could not find title \n{title} \nin {url}")
        if not validators.validate_string_in_html(url, description):
            print(f"Could not find description \n{description}\nin {url}")

    print("Finished iterating")


if __name__ == '__main__':
    main()
