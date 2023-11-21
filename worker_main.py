from docifyai.core import logger
from server.workers import worker
from server.config import config
logger = logger.Logger(__name__)

env_config = config.enVar()

if __name__ == "__main__":
    logger.info("RQ worker started.")
    try:
        worker.run_workers(env_config)  # get from env file rather than hard code it
    except KeyboardInterrupt:
        logger.info("RQ worker stopped buy user.")
