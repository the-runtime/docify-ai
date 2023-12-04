import asyncio
import time
from typing import Dict, Tuple, List
from pathlib import Path
import httpx
from docifyai.core import logger
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
from docifyai.config import config


class OpenAIHandler:
    """OpenAI Handler for generating text from the code """

    logger = logger.Logger(__name__)

    def __init__(self, env_var: config.enVar):
        """Initialize the OpenAi Handler"""

        # should come from config rather than hard coded
        self.endpoint = env_var.model_endpoint
        self.encoding = "cl100k_base"
        self.model = env_var.model_name
        self.tokens = int(env_var.tokens)
        self.tokens_max = int(env_var.max_tokens)
        self.temperature = float(env_var.temperature)
        self.rate_limit = 5
        self.cache = TTLCache(maxsize=500, ttl=600)
        self.http_client = httpx.AsyncClient(
            http2=True,
            timeout=300,
            limits=httpx.Limits(
                max_keepalive_connections=10, max_connections=100
            ),
        )
        self.last_requests_time = time.monotonic()
        self.rate_limit_semaphore = asyncio.Semaphore(self.rate_limit)
        self.last_request_time = time.monotonic()

        # to be imported from env
        self.api_key = env_var.azure_openai_key

    async def code_to_text(
            self, ignore: dict, files: Dict[Path, str], prompt: str, depend_dict: Dict[Path, List[Path]]
    ) -> List[Tuple]:
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
            depend_files = depend_dict.get(path)
            prompt_3rd = "["
            if depend_files:
                for file_path in depend_files:
                    depend_content = files.get(file_path)
                    if depend_content:
                        prompt_3rd += f"Path: {file_path} \nContents: {depend_content}"
            prompt_3rd += "]"
            prompt_code = prompt.format(str(path), contents, prompt_3rd)
            # print(prompt_code)
            # prompt_code = f"{prompt}"
            tasks.append(
                asyncio.create_task(
                    self.generate_text(str(path), prompt_code, self.tokens)
                )
            )

        results = await asyncio.gather(*tasks)

        filter_results = []

        for result in results:
            if isinstance(result, Exception):
                self.logger.error(f"Task failed with exception: {result}")
            else:
                filter_results.append(result)
        return filter_results

    async def folder_to_text(self, code_details: Dict[str, str], working_folder: Path, temp_dir: str, prompt: str) -> \
            List[Tuple[str, str]]:
        """Generates text using prompts and azure OpenAI's GPT model"""
        # use prompt text instead of empty string
        tasks = []
        if working_folder.is_dir():  # always true as this is the initial directory of the project
            for child in working_folder.iterdir():
                prompt_var_text = ""
                if child.is_file():
                    value_prompt = code_details.get(str(child.relative_to(temp_dir)))
                    file_path = str(child.relative_to(working_folder))
                    if value_prompt:
                        prompt_var_text += f"path: {str(file_path)} \nDescription: {value_prompt}\n"
                        prompt_text = prompt.format(prompt_var_text)
                        tasks.append(
                            asyncio.create_task(
                                self.generate_text(str(child.relative_to(working_folder)), prompt_text, self.tokens)
                            )
                        )
                        continue
                elif child.is_dir():
                    for file_child in child.rglob("*"):
                        if file_child.is_file():
                            value_prompt = code_details.get(str(file_child.relative_to(temp_dir)))
                            file_path = str(file_child.relative_to(working_folder))
                            if value_prompt:
                                prompt_var_text += f"path: {file_path} \nDescription: {value_prompt}\n"
                                prompt_text = prompt.format(prompt_var_text)

                                tasks.append(
                                    asyncio.create_task(
                                        self.generate_text(str(child.relative_to(temp_dir)), prompt_text,
                                                           self.tokens)
                                    )
                                )
                                continue
        final_result = []
        results = await asyncio.gather(*tasks)

        for result in results:
            if isinstance(result, Exception):
                self.logger.error("Task failed with exception: ", result)
            else:
                final_result.append(result)

        return final_result

    async def get_text_for_intro(self, folder_details: Dict[str, str], prompt: str) -> Tuple[str, str]:
        prompt_str = ""
        for name, text in folder_details.items():
            if Path(name).is_file():
                prompt_str += f"Filename: {name}\nDetails: {text}\n"
            else:
                prompt_str += f"Package/Folder name: {str}\n Details: {text}\n"
        prompt_final = prompt.format(prompt_str)

        result = await self.generate_text("Introduction", prompt_final, self.tokens)
        if isinstance(result, Exception):
            self.logger.error("Error getting Intro for the project ", result)
            return "Introduction", ""
        else:
            return result

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
                                "content": "You are an automatic code documentation generator, which generates documentation in docx format.",
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
                summary = data["choices"][0]["message"]["content"]

                # self.logger.info(
                #     f"\nProcessing prompt: {index}\nResponse: {summary}"
                # )
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
            self.logger.error(f"Exception hello:\n{str(excinfo)}")
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
