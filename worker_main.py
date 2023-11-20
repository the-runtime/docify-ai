from docifyai.core import logger
from server.workers import worker
logger = logger.Logger(__name__)

if __name__ == "__main__":
    logger.info("RQ worker started.")
    try:
        worker.run_workers("queue_for_jobs_to_worker")
    except KeyboardInterrupt:
        logger.info("RQ worker stopped buy user.")
