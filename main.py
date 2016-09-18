import csv
import os
import re
from math import *
import sys

if len(sys.argv) == 4:
    path_parts = sys.argv[3].split(os.path.sep)
    sys.path.append(os.path.dirname(os.path.abspath(sys.argv[3])))
    exec("from " + path_parts[-1][:-3] + " import *")


def main(argv):
    pathFrom, pathTo = parseArgs(argv)
    with open(pathFrom, 'r') as file:
        data = list(csv.reader(file, delimiter=','))

    process(data)

    with open(pathTo, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def parseArgs(argv):
    from_ = argv[1]
    to_ = argv[2]

    return from_, to_


def process(data):
    for i, _ in enumerate(data):
        for j, item in enumerate(data[i]):
            data[i][j] = processItem(item, data)

    return data


def processItem(item, data):
    if item.startswith('='):
        item = replaceLinksByValues(item, data)
        try:
            return eval(item[1:])
        except NameError:
            return "ERROR"
    else:
        return item


def replaceLinksByValues(item, data):
    print("before:", item)
    for link in findLinksInItem(item):
        replacingValue = countLink(link, data)
        if type(replacingValue) == str:
            item = item.replace(link, '"' + replacingValue + '"')
        else:
            item = item.replace(link, str(replacingValue))
    print("after:", item)
    return item


def findLinksInItem(item):
    return set(re.findall('[A-Z]\d+', item))


def countLink(link, data):
    value = data[int(link[1:]) - 1][letterToPosition(link[0])]

    try:
        return int(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    return value


def letterToPosition(letter):
    return "ABCDEFGHIKLMNOPQRSTVXYZ".index(letter)


def showUsageMessage():
    print("Usage: main.py <from> <to> [<script file>]")


if __name__ == "__main__":
    args = sys.argv

    if len(args) < 3:
        showUsageMessage()
    else:
        main(sys.argv)
