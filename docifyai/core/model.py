import asyncio
import time
from typing import Dict, Tuple
import httpx
import logger
import openai
from cachetools import TTLCache

from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)
from docifyai.core.tokens import get_token_count, truncate_tokens


class OpenAIHandler:
    """OpenAI Handler for generating text from the code """

    logger = logger.Logger(__name__)

    def __init__(self):
        """Intialize the OpenAi Handler"""

        # should come from config rather than hard coded
        self.endpoint = "https://doc.openai.azure.com/openai/deployments/test-doc/chat/completions/?api-version=2023-05-15"
        self.encoding = "cl100k_base"
        self.model = "gpt-3.5-turbo"
        self.tokens = 650
        self.tokens_max = 3800
        self.temperature = 1.1
        self.rate_limit = 3
        self.cache = TTLCache(maxsize=500, ttl=600)
        self.http_client = httpx.AsyncClient(
            http2=True,
            timeout=30,
            limits=httpx.Limits(
                max_keepalive_connections=10, max_connections=100
            ),
        )
        self.last_requests_time = time.monotonic()
        self.rate_limit_semaphore = asyncio.Semaphore(self.rate_limit)
        self.last_request_time = time.monotonic()

        # to be imported from env
        self.api_key = "41f2c19fbaf343a0b93ec51f17107f28"

    async def code_to_text(
            self, ignore: dict, files: Dict[str, str], prompt: str
    ) -> Dict[str, str]:
        """converts code to natural language by using large language model"""

        tasks = []
        for path, contents in files.items():
            if not (
                    all(
                        idir not in path.parts
                        for idir in ignore.get("directories", [])
                    )
                    and path.name not in ignore.get("files", [])
                    and path.suffix[1:] not in ignore.get("extensions", [])
            ):
                self.logger.warning(f"Ignoring file:{path}")
                continue

            prompt_code = prompt.format(str(path), contents)
            tasks.append(
                asyncio.create_task(
                    self.generate_text(path, prompt_code, self.tokens)
                )
            )

        results = await asyncio.gather(*tasks, return_exceptions=True)

        filter_results = []

        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Task failed with exception: {result}")
            else:
                filter_results.append(result)
        return filter_results

    async def generate_text(
            self, index: str, prompt: str, tokens: int
    ) -> Tuple[str, str]:
        """Handles the request to the OpenAi API to generate text"""
        try:
            token_count = get_token_count(prompt, self.encoding)

            if token_count > tokens:
                prompt = truncate_tokens(prompt, tokens)

            async with self.rate_limit_semaphore:
                response = await self.http_client.post(
                    self.endpoint,
                    headers={"api-key": self.api_key},
                    json={
                        "messages": [
                            {
                                "role": "system",
                                "content": "You're a brilliant Tech Lead.",
                            },
                            {
                                "role": "user", "content": prompt,
                            }
                        ],
                        "model": self.model,
                        "temperature": self.temperature,
                        "max_tokens": tokens
                    },
                )
                response.raise_for_status()
                data = response.json()
                summary = data["choises"][0]["message"]["content"]

                self.logger.info(
                    f"\nProcessing prompt: {index}\nResponse: {summary}"
                )
                self.cache[prompt] = summary
                return index, summary


        # don't know what those exceptions are and how they are being handled.
        except openai.error.OpenAIError as excinfo:
            self.logger.error(f"OpenAI Exception:\n{str(excinfo)}")
            return await self.null_summary(
                index, f"OpenAI exception: {excinfo.response.status_code}"
            )

        except httpx.HTTPStatusError as excinfo:
            self.logger.error(f"HTTPStatus Exception:\n{str(excinfo)}")
            return await self.null_summary(
                index, f"HTTPStatus Exception: {excinfo.response.status_code}"
            )
        except RetryError as excinfo:
            self.logger.error(f"RetryError Exception:\n{str(excinfo)}")
            return await self.null_summary(
                index, f"RetryError Exception: {excinfo}"
            )

        except Exception as excinfo:
            self.logger.error(f"Exception:\n{str(excinfo)}")
            return await self.null_summary(index, f"Exception: {excinfo}")

        finally:
            self.last_request_time = time.monotonic()

    @staticmethod
    async def null_summary(index: str, summary: str) -> Tuple[str, str]:
        """Handles any exception raised while requesting the API."""
        return index, summary

    async def close(self):
        """Close the HTTP client."""
        await self.http_client.aclose()
