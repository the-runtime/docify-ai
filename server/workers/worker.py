import time

from rq import Worker, Queue, Connection
from redis import Redis
from docifyai.core import logger

import asyncio
from pathlib import Path
from docifyai.core import model
from docifyai.services import get_repo
from docifyai.core import logger
from docifyai.utils import utils
from docifyai.core.preprocess import RepoParseFunc as repo_parse
from docifyai.langaugeSupport import get_lang_support
from docifyai.document.aiDoc import Aidoc
from docifyai.config.config import enVar

import threading

logger = logger.Logger(__name__)

# logger = logger.Logger(__name__)

"""Use logger in such a way that it can tell, from which job it is called from"""


def run_workers(env_config,
                num_threads: int = 4):  # num_threads = 4 because of 5 conn is allowed for elephant sql 1 base + 4 workers
    # Establish a connection to the redis server
    # redis_conn = Redis()
    #
    # # Create a queue for the worker to listen on
    # queue = Queue(queue_name, connection=redis_conn)
    #
    # def thread_function():
    #     while True:
    #         # job = queue.dequeue_any([queue], connection=redis_conn)
    #
    #         job_lis = queue.get_job()
    #         if len(job_lis) == 0:
    #             time.sleep(1)
    #             continue
    #         job_lis[0].connection = redis_conn
    #         job_lis[0].perform()
    #
    # threads = []
    # for _ in range(num_threads):
    #     thread = threading.Thread(target=thread_function)
    #     threads.append(thread)
    #     thread.start()
    #
    # # Wait for all threads to finish
    # for thread in threads:
    #     thread.join()
    try:
        # Create a connection to the Redis server
        redis_conn = Redis(host=env_config.redis_host, port=env_config.redis_port)
        worker = Worker(env_config.redis_queue_name, connection=redis_conn)
        worker.work()

    except Exception as excinfo:
        logger.error(f"Worker encountered as error: {excinfo}")
        raise


# if __name__ == "__main__":
#     logger.info("RQ worker started.")
#     try:
#         run_workers("job_objects5")
#     except KeyboardInterrupt:
#         logger.info("RQ worker stopped buy user.")
