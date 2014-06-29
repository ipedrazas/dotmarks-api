from urllib2 import Request, urlopen, URLError
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from urlparse import urlparse
from constants import LAST_UPDATED
from celery.utils.log import get_task_logger
from pymongo import MongoClient
from bson.objectid import ObjectId


logger = get_task_logger(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.eve


def get_date():
    return datetime.utcnow().replace(microsecond=0)


def get_title_from_url(url):
    print "getting title from " + url
    try:
        hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
               'AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu '
               'Chromium/34.0.1847.116 Chrome/34.0.1847.116 '
               'Safari/537.36'}

        req = Request(url, headers=hdr)
        soup = BeautifulSoup(urlopen(req))
        # print str(soup)
        if soup.title:
            return soup.title.string
        elif soup.h1:
            return soup.h1.string.strip()

    except IOError as e:
        logger.error(e)
        logger.error("    I/O error({0}): {1}".format(e.errno, e.strerror))
    except URLError, err:
        logger.error(err.reason)
    except AttributeError as at:
        logger.error(at)


def do_update(oid, updates):
    updates[LAST_UPDATED] = get_date()
    db.dotmarks.update({'_id': ObjectId(oid)}, {'$set': updates}, upsert=False)


def get_domain(url):
    parsed_uri = urlparse(url)
    # ignore the uri.scheme (http|s)
    domain = parsed_uri.netloc
    posWWW = domain.find('www')
    if posWWW != -1:
        domain = domain[4:]
    return domain


def tags_by_url(url):
    results = db.atags.find({'entries': get_domain(url)})
    tags = []
    for result in results:
        logger.info(result)
        tags.append(result['tag'])
    return tags


def tag_title(title):
    if title:
        print("tagging " + title)
        tokens = title.lower().split()
        print str(tokens)
        results = db.atags.find({'keywords': {'$in': tokens}}, {'tag': 1})
        tags = []
        for result in results:
            print str(result)
            tags.append(result['tag'])
        return tags


def auto_tag(item):
    atags = []
    at_url = tags_by_url(item['url'])
    if at_url:
        atags.extend(at_url)
    if 'title' in item:
        at_title = tag_title(item['title'])
        if at_title:
            atags.extend(at_title)

    return atags
