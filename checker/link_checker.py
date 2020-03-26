#! /usr/bin/env python3

import yaml
import os
import requests
import logging
import schedule
from datetime import datetime, time as tm
import time
from logging.handlers import SMTPHandler

RETURN_STATUS_WARNING = "ERROR - {}: Bad status returned = {}"
RETURN_STATUS_OK = "OK - {}: Status returned = {}"
RETURN_STATUS_EXCEPTION = "EXCEPTION - {}: Exception = {}"

EMAIL_FROM_ADDRESS = os.environ["EMAIL_FROM_ADDRESS"]
EMAIL_TO_ADDRESS = os.environ["EMAIL_TO_ADDRESS"]
EMAIL_SMTP_SERVER = os.environ["EMAIL_SMTP_SERVER"]

logger = logging.getLogger('Link Checker')
logger.setLevel(logging.WARNING)

# create console handler and set level to debug
eh = SMTPHandler(
    # Mail server
    EMAIL_SMTP_SERVER,
    # From email address
    EMAIL_FROM_ADDRESS,
    # To email address
    EMAIL_TO_ADDRESS,
    # Email subject
    'Link Checker')

eh.setLevel(logging.WARNING)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')

# add formatter to ch
eh.setFormatter(formatter)

# add ch to logger
logger.addHandler(eh)


def check_link(link):
    try:
        r = requests.get(link['url'], verify=link['verify'])

        if r.status_code != 200 and r.status_code != 403:
            logger.warning(
                RETURN_STATUS_WARNING.format(link['url'], r.status_code))
        else:
            logger.info(
                RETURN_STATUS_OK.format(link['url'], r.status_code))

    except Exception as e:
        logger.error(
            RETURN_STATUS_EXCEPTION.format(link['url'], e))


def check_links():
    documents = yaml.load_all(open("links.yml", "r"))

    for doc in documents:
        for link_section in doc:
            for link in link_section['links']:
                check_link(link)


schedule.every(10).minutes.do(check_links)

if __name__ == "__main__":
    while True:
        if tm(7,0) <= datetime.now().time() <= tm(19,0):
            schedule.run_pending()

        time.sleep(60)
