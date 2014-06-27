import multiprocessing


bind = 'unix:/tmp/gunicorn-api.dotmarks.dev.socket'
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 60
