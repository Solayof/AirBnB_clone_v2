#!/usr/bin/python3
import sys
import requests
from lxml import html
import re
import MySQLdb
import uuid


def add_states(number=1):
    conn = MySQLdb.connect(host="localhost", port=3306, user=sys.argv[1], passwd=sys.argv[2], db=sys.argv[3], charset="utf8")
    cur = conn.cursor()

    for i in range(number):
        cur.execute("INSERT INTO `states` (id, created_at, updated_at, name) VALUES ('{}','2016-03-25 19:42:40','2016-03-25 19:42:40','state{}');".format(str(uuid.uuid4()), i))

    conn.commit()
    cur.close()
    conn.close()


def validate_number(number):

    NO_PROXY = {
        'no': 'pass',
    }

    ## Request
    page = requests.get('http://0.0.0.0:5000/states_list', proxies=NO_PROXY)
    if int(page.status_code) != 200:
        return False, "Status fail: {}".format(page.status_code)

    ## Parsing
    tree = html.fromstring(page.content)
    if tree is None:
        return False, "Can't parse page"

    # LI tags
    li_tags = list(filter(None, [x.replace(" ", "").strip(" ").strip("\n").strip("\t") for x in tree.xpath('//body/ul/li/text()')]))
    if li_tags is None or len(li_tags) != number:
        return False, "Doesn't find {} LI tags (found {})".format(number, len(li_tags))

    return True, None


# Test initial state
res, msg = validate_number(5)
if not res:
    print("ERROR: {}".format(msg))

# Add 1 new states
add_states(1)

# Test 6 states
res, msg = validate_number(6)
if not res:
    print("ERROR: {}".format(msg))

print("OK", end="")
