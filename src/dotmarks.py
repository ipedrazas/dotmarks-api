from eve import Eve
import os
# from utils import populate_dotmark, parse_log, process_attachment
from workers.postworker import populate_dotmark, parse_log, process_attachment
from flask import jsonify


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
    return '.dotMarks v0.0.1a'


@app.route("/tags")
def get_all_tags():
    dotMarks = app.data.driver.db['dotmarks']
    return jsonify(dotMarks.distinct('tags'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
