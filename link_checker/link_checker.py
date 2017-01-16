#! /usr/bin/env python3

import yaml
import requests
import logging

RETURN_STATUS_WARNING = "{}: Bad status returned = {}"


def check_links(links):
    for link in links:
        r = requests.get(link['url'])

        if r.status_code != 200:
            logging.warning(
                RETURN_STATUS_WARNING.format(link['url'], r.status_code))


def main():
    documents = yaml.load_all(open("links.yml", "r"))

    for doc in documents:
        for link_section in doc:
            check_links(link_section['links'])


if __name__ == "__main__":
    main()
