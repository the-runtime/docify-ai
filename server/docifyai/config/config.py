import os
import sys

from docifyai.core import logger
from dotenv import load_dotenv

logger = logger.Logger(__name__)


class enVar:
    def __init__(self, path: str = ".env"):
        if load_dotenv(path):
            logger.info("Environment Variables loaded")
            self.azure_openai_key = os.getenv("AZURE_OPENAI_KEY")
            self.model_name = os.getenv("MODEL_NAME")
            self.model_endpoint = os.getenv("ENDPOINT")
            self.tokens = os.getenv("TOKENS")
            self.max_tokens = os.getenv("MAX_TOKENS")
            self.temperature = os.getenv("TEMPERATURE")
            self.github_token = os.getenv("GITHUB_TOKEN")
            self.postgres_url = os.getenv("POSTGRES_URL")
            self.brevo_key = os.getenv("BREVO_KEY")
        else:
            logger.error("Problem loading env file, make sure it is available")
            sys.exit()
