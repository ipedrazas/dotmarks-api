
from celery import Celery
from pymongo import MongoClient
from bson.objectid import ObjectId
from dot_delicious import parse_html
from dot_utils import get_date, get_title_from_url, do_update
from dot_utils import auto_tag
from celery.utils.log import get_task_logger
import os


LAST_UPDATED = '_updated'

logger = get_task_logger(__name__)

celery_host = os.environ.get('REDIS_PORT_6379_TCP_ADDR'),
celery_port = os.environ.get('REDIS_PORT_6379_TCP_PORT')

mongo_host = os.environ.get('MONGODB_PORT_27017_TCP_ADDR')
mongo_port = os.environ.get('MONGODB_PORT_27017_TCP_PORT')

CELERY_URL = 'redis://' + celery_host + ":" + celery_port
MONGO_URL = 'mongodb://' + mongo_host + ":" + mongo_port + '/'

client = MongoClient(MONGO_URL)
db = client.eve


REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR')
REDIS_PORT = os.environ.get('REDIS_PORT_6379_TCP_PORT')

CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT

celery = Celery('dotmarks', broker=CELERY_BROKER_URL)


@celery.task()
def process_attachment(item):
    if '_id' in item:
        parse_html(item['_id'])


@celery.task()
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


@celery.task()
def populate_dotmark(item):
    logger.info("processing %s" % item['url'])
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
