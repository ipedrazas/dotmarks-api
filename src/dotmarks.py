from eve import Eve
import os
# from utils import populate_dotmark, parse_log, process_attachment
from workers.postworker import populate_dotmark, parse_log, process_attachment
from flask import jsonify, abort
from crossdomain import cors


def after_insert_dotmark(items):
    for item in items:
        populate_dotmark.delay(item)


def after_insert_log(items):
    print str(items)
    for item in items:
        parse_log.delay(item)


def after_inserting_atachment(items):
    for item in items:
        process_attachment.delay(item)


#
# Hack to read settings when using gunicorn
#
SETTINGS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'settings.py')

app = Eve(settings=SETTINGS_PATH)


app.on_inserted_attachments += after_inserting_atachment
app.on_inserted_dotmarks += after_insert_dotmark
app.on_inserted_logs += after_insert_log


@app.route("/version")
def version():
    return '.dotMarks v0.1'


@app.route("/tags")
@cors(origin='*')
def get_all_tags():
    dotmarks = app.data.driver.db['dotmarks']
    unwind = {"$unwind": "$tags"}
    group = {"$group": {"_id": "$tags", "count": {"$sum": 1}}}
    sort = {"$sort": {"count": -1}}
    # limit = {"$limit": 40}

    cursor = dotmarks.aggregate([unwind, group, sort])
    docs = []
    total = 0
    page = 0
    page_size = 40
    for doc in cursor.result:
        if page < page_size:
            docs.append(doc)
        total += 1
        page += 1

    response = {"total": total, "_items": docs}

    return jsonify(response)


@app.route("/analytics/hours/<username>")
@cors(origin='*')
def analytics_per_hour(username=None):
    if username:
        match = {"$match": {"user": username}}
        group = {"$group": {"_id": "$time.hours", "count": {"$sum": 1}}}
        history = app.data.driver.db['history']
        sort = {"$sort": {"_id": 1}}
        limit = {"$limit": 25}

        return jsonify(history.aggregate([match, group, sort, limit]))
    abort(404)


@app.route("/analytics/days/<username>")
@cors(origin='*')
def analytics_per_day(username=None):
    if username:
        match = {"$match": {"user": username}}
        group = {"$group": {"_id": "$time.day", "count": {"$sum": 1}}}
        history = app.data.driver.db['history']
        sort = {"$sort": {"_id": 1}}
        limit = {"$limit": 32}

        return jsonify(history.aggregate([match, group, sort, limit]))
    abort(404)


@app.route("/analytics/weekdays/<username>")
@cors(origin='*')
def analytics_per_weekday(username=None):
    if username:
        match = {"$match": {"user": username}}
        group = {"$group": {"_id": "$time.weekday", "count": {"$sum": 1}}}
        history = app.data.driver.db['history']
        sort = {"$sort": {"_id": 1}}

        return jsonify(history.aggregate([match, group, sort]))
    abort(404)


@app.route("/analytics/domains/<username>")
@cors(origin='*')
def analytics_per_domain(username=None):
    if username:
        match = {"$match": {"user": username}}
        group = {"$group": {"_id": "$domain", "count": {"$sum": 1}}}
        sort = {"$sort": {"count": -1}}
        limit = {"$limit": 50}
        history = app.data.driver.db['history']

        return jsonify(history.aggregate([match, group, sort, limit]))
    abort(404)


@app.route("/analytics/searches/<username>")
@cors(origin='*')
def analytics_per_search(username=None):
    if username:
        history = app.data.driver.db['history']
        match = {"$match": {"user": username}}
        unwind = {"$unwind": "$search"}
        group = {"$group": {"_id": "$search", "count": {"$sum": 1}}}
        sort = {"$sort": {"count": -1}}
        limit = {"$limit": 40}

        return jsonify(history.aggregate([match, unwind, group, sort, limit]))
    abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
