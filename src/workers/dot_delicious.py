from pymongo import MongoClient
from bson.objectid import ObjectId
import gridfs
from BeautifulSoup import BeautifulSoup, SoupStrainer
from dot_utils import get_title_from_url, get_date
import os


mongo_host = os.environ.get('MONGODB_PORT_27017_TCP_ADDR')
mongo_port = os.environ.get('MONGODB_PORT_27017_TCP_PORT')
MONGO_URL = 'mongodb://' + mongo_host + ":" + mongo_port + '/'

client = MongoClient(MONGO_URL)


db = client.eve
fs = gridfs.GridFS(db)
dks = db.dotmarks
users = db.users

LAST_UPDATED = '_updated'


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
                new_id = dks.insert(dk)
                if new_id:
                    users.update({'username': attachment['user']},
                                 {"$inc": {"dots": 1},
                                  "$set": {LAST_UPDATED: get_date()}},
                                 upsert=False)
