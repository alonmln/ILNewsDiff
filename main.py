#!/usr/bin/python3

import logging
import os
import sys

from pytz import timezone

from haaretz_parser import HaaretzParser
from israel_hayom_parser import IsraelHayomParser

TIMEZONE = 'Israel'
LOCAL_TZ = timezone(TIMEZONE)

if 'LOG_FOLDER' in os.environ:
    LOG_FOLDER = os.environ['LOG_FOLDER']
else:
    LOG_FOLDER = ''


def main():
    # logging
    logging_filehandler = logging.FileHandler(filename=LOG_FOLDER + 'titlediff.log',
                                              encoding='utf-8', mode='a+')
    handlers = [logging_filehandler, logging.StreamHandler(sys.stdout)]
    logging.basicConfig(handlers=handlers,
                        format='%(asctime)s %(name)13s %(levelname)8s: %(message)s',
                        level=logging.DEBUG)

    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    logging.info('Starting script')

    try:
        logging.debug('Starting Parsers')
        parsers = [HaaretzParser(LOCAL_TZ), IsraelHayomParser(LOCAL_TZ)]
        for parser in parsers:
            logging.info(f"Parsing {parser.get_source()}")
            parser.parse()
        logging.debug('Finished')
    except:
        logging.exception('Parser')

    logging.info('Finished script')


if __name__ == "__main__":
    main()
