import os
import sys

from docifyai.core import logger
from dotenv import load_dotenv

logger = logger.Logger(__name__)


class enVar:
    def __init__(self, path: str = ".env"):
        if load_dotenv(path):
            logger.info("Environment Variables loaded")
            self.postgres_url = os.getenv("POSTGRES_URL")
            self.blob_container_name = os.getenv("BLOB_CONTAINER_NAME")
            self.azure_blob_key = os.getenv("AZURE_BLOB_KEY")
            self.server_secret_key = os.getenv("SERVER_SECRET_KEY")
            self.google_json_file = os.getenv("GOOGLE_JSON_FILE")
            self.redis_host = os.getenv("REDIS_HOST")
            self.redis_port = os.getenv("REDIS_PORT")
            self.redis_password = os.getenv("REDIS_PASSWORD")
            self.redis_queue_name = os.getenv("REDIS_QUEUE_NAME")

        else:
            logger.error("Problem loading env file, make sure it is available")
            sys.exit()
