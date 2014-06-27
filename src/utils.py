from urllib2 import Request, urlopen, URLError
from BeautifulSoup import BeautifulSoup, SoupStrainer
from datetime import datetime
import hashlib
from urlparse import urlparse
from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app as app
import os
import gridfs


MONGO_HOST = os.environ.get('MONGODB_PORT_27017_TCP_ADDR')
MONGO_PORT = os.environ.get('MONGODB_PORT_27017_TCP_PORT')
MONGO_URL = 'mongodb://' + MONGO_HOST + ':' + MONGO_PORT

client = MongoClient(MONGO_URL)
db = client.eve
fs = gridfs.GridFS(db)
dks = db.dotmarks


LAST_UPDATED = '_updated'


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
        app.logger.error(e)
        app.logger.error("    I/O error({0}): {1}".format(e.errno, e.strerror))
    except URLError, err:
        app.logger.error(err.reason)
    except AttributeError as at:
        app.logger.error(at)


def get_hash(email):
    m = hashlib.sha1()
    m.update(email + str(get_date()))
    return m.hexdigest()


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
        app.logger.info(result)
        tags.append(result['tag'])
    return tags


def tag_title(title):
    if title:
        print ("tagging " + title)
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


def populate_dotmark(item):
    app.logger.info("processing %s" % item['url'])
    updates = {}
    if 'url' and '_id' in item:
        if 'title' not in item or not item['title']:
            updates['title'] = get_title_from_url(item['url'])
            item['title'] = updates['title']

        atags = auto_tag(item)
        if atags:
            updates['atags'] = atags

        if updates:
            do_update(item['_id'], updates)


def parse_log(item):
    if 'source_id' in item:
        oid = item['source_id']
        if(item['action'] == 'click'):
            db.dotmarks.update(
                {"_id": ObjectId(oid)},
                {"$inc": {"views": 1}, "$set": {LAST_UPDATED: get_date()}},
                upsert=False)

        if(item['action'] == 'star'):
            updates = {'star': 'true' in item['value']}
            do_update(oid, updates)


def process_attachment(item):
    if '_id' in item:
        parse_html(item['_id'])


def parse_html(oid):
    cursor = db.attachments.find({'_id': ObjectId(oid)})
    for attachment in cursor:
        html = fs.get(attachment['file']).read()
        # print html
        for link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
            if link:
                # print link.contents
                dk = {}
                dk['url'] = link['href']
                print "parsing " + link['href']
                if ',' in link['tags']:
                    tags = link['tags'].strip().split(',')
                    if tags:
                        dk['tags'] = tags
                dk['username'] = attachment['user']
                if link.contents[0]:
                    title = link.contents[0]
                    print title
                    if 'http' != title[:4]:
                        dk['title'] = title
                if 'title' not in dk:
                    dk['title'] = get_title_from_url(dk['url'])
                dks.insert(dk)
