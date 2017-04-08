#! /usr/bin/env python3

import yaml
import requests
import logging

RETURN_STATUS_WARNING = "ERROR - {}: Bad status returned = {}"
RETURN_STATUS_OK = "OK - {}: Status returned = {}"
RETURN_STATUS_EXCEPTION = "EXCEPTION - {}: Exception = {}"


def check_links(links):
    for link in links:
        try:
            r = requests.get(link['url'], verify=link['verify'])

            if r.status_code != 200 and r.status_code != 403:
                logging.warning(
                    RETURN_STATUS_WARNING.format(link['url'], r.status_code))
            else:
                logging.info(
                    RETURN_STATUS_OK.format(link['url'], r.status_code))

        except Exception as e:
            logging.error(
                RETURN_STATUS_EXCEPTION.format(link['url'], e))


def main():
    documents = yaml.load_all(open("links.yml", "r"))

    for doc in documents:
        for link_section in doc:
            check_links(link_section['links'])


if __name__ == "__main__":
    main()
