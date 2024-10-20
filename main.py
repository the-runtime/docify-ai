import uvicorn
from server.app import app
from docifyai.core import logger

logger = logger.Logger(__name__)

if __name__ == "__main__":
    uvicorn.run(app, port=8080)
    logger.info("Uvicorn started on port 8080")

