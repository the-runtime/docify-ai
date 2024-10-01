from redis import Redis
from rq import Queue
import requests
from time import time


def count_words_at_url(url):
    resp = requests.get(url)
    return len(resp.text.split())


def main():
    redis_conn = Redis.from_url()

    print(redis_conn.info())
    red_queue = Queue(connection=redis_conn)
    job = red_queue.enqueue(count_words_at_url, 'http://nvie.com')
    print(job.return_value())  # => None  # Changed to job.return_value() in RQ >= 1.12.0

    # Now, wait a while, until the worker is finished
    time.sleep(2)
    print(job.return_value())


if __name__ == '__main__':
    main()
