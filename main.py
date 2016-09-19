"""

This script counts fields in csv (excel style) file.
There is support of external python functions.

Babichev Oleg (194 group)
19.09.2016

"""

import csv
import os
import re
from math import *
import sys


def get_module_name(path_to_file):
    path_parts = path_to_file.split(os.path.sep)
    return path_parts[-1][:-3]


if len(sys.argv) == 4:
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[3])))
    exec("from " + get_module_name(sys.argv[3]) + " import *")


def main(argv):
    path_from, path_to = parse_args(argv)
    with open(path_from, 'r') as fileFrom:
        data = list(csv.reader(fileFrom, delimiter=','))

    process(data)

    with open(path_to, 'w') as fileTo:
        writer = csv.writer(fileTo)
        writer.writerows(data)


def parse_args(argv):
    from_ = argv[1]
    to_ = argv[2]

    return from_, to_


def process(data):
    for i, _ in enumerate(data):
        for j, item in enumerate(data[i]):
            data[i][j] = process_item(item, data)

    return data


def process_item(item, data):
    if item.startswith('='):
        item = replace_links_by_values(item, data)
        try:
            return eval(item[1:])
        except NameError:
            return "ERROR"
    else:
        return item


def replace_links_by_values(item, data):
    for link in find_links_in_item(item):
        replacing_value = count_link(link, data)
        if isinstance(replacing_value, str):
            item = item.replace(link, '"' + replacing_value + '"')
        else:
            item = item.replace(link, str(replacing_value))
    return item


def find_links_in_item(item):
    return set(re.findall(r'[A-Z]\d+', item))


def count_link(link, data):
    value = data[int(link[1:]) - 1][letter_to_position(link[0])]

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def letter_to_position(letter):
    return "ABCDEFGHIKLMNOPQRSTVXYZ".index(letter)


def show_usage_message():
    print("Usage: main.py <from> <to> [<script file>]")


if __name__ == "__main__":

    if len(sys.argv) < 3:
        show_usage_message()
    else:
        main(sys.argv)
