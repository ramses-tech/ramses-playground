#!/usr/bin/env python
from argparse import ArgumentParser

import json
import requests
import sys


def main(argv=sys.argv):
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        '-n', '--number', help='Number of objects to create',
        default=10, type=int)
    parser.add_argument(
        '-u', '--url', help='Images EXIF API url',
        default='http://localhost:6543/api/images', type=str)
    options = parser.parse_args()



def fetch_images_list(options):
    pass


def populate_images_api(options):
    pass
