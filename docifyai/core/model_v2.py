import asyncio
import time
from typing import Dict, Tuple, List
from pathlib import Path
import httpx
from docifyai.core import logger
from docifyai.utils import utils
# import openai
from cachetools import TTLCache

from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed
)
from docifyai.core.tokens import get_token_count, truncate_tokens
from docifyai.config import config


class OpenAIHandler:
    """OpenAI Handler for generating text from the code """

    logger = logger.Logger(__name__)

    def __init__(self, env_var: config.enVar, temp_dir: str):
        """Initialize the OpenAi Handler"""

        self.temp_dir = Path(temp_dir)

        # should come from config rather than hard coded
        self.endpoint = env_var.model_endpoint
        self.encoding = "o200k_base"
        self.model = env_var.model_name
        self.tokens = int(env_var.tokens)
        self.tokens_max = int(env_var.max_tokens)
        self.temperature = float(env_var.temperature)
        self.rate_limit = 10
        self.cache = TTLCache(maxsize=500, ttl=600)
        self.http_client = httpx.AsyncClient(
            http2=True,
            timeout=20 * 60,
            limits=httpx.Limits(
                max_keepalive_connections=10, max_connections=100
            ),
        )
        self.last_requests_time = time.monotonic()
        self.rate_limit_semaphore = asyncio.Semaphore(self.rate_limit)
        self.last_request_time = time.monotonic()

        # to be imported from env
        self.api_key = env_var.azure_openai_key

    async def read_code(
            self, ignore: dict, files: Dict[Path, str], prompt: str, depend_dict: Dict[Path, List[Path]]
    ) -> List[Tuple]:
        """ give 2 or three lines of  summary of the code """

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
            # not using prompt_3rd as depend files is not used now
            prompt_3rd += "]"
            prompt_code = prompt.format(str(path), contents)
            # print(prompt_code)
            # prompt_code = f"{prompt}"
            tasks.append(
                asyncio.create_task(
                    self.generate_text(str(path), prompt_code, self.tokens, utils.get_role_content(0))
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

    async def get_initial_overview_of_project(self, code_details: Dict[str, str], prompt: str) -> str | None:
        """some info might get truncated due to excess number of tokens"""
        """may need to breakdown so that all info is accounted in the formation of initial_overview // partially done"""
        temp_prompt = ""
        for code_path, code_sum in code_details.items():
            temp_prompt += f"Path: {code_path}\nCode Summary: {code_sum}\n"

        prompt_final = prompt.format(temp_prompt)
        result = await self.generate_text("Basic Understanding", prompt_final, self.tokens, utils.get_role_content(1))
        if isinstance(result, Exception):
            self.logger.error("Error getting initial overview of the ")
            return None
        return result[1]

    async def get_chapters_name(self, init_overview, code_details: Dict[str, str], prompt: str) -> Dict[str, List[
        str]] | None:
        """Use chat-gpt to get the chapters required
        Use code_info alongside initial_overview to generate chapters with path of files associated with it
        something like
            token_ratio = tokencount(info) / max_tokens
            if token_ratio >= 1:
                for info in infos:
                    info = truncate(info relative to ratio)

        """
        """ we should use code_details as json for gpt to have better understanding of it"""
        json_code_details = utils.dict_to_json(code_details)
        final_prompt = prompt.format(init_overview, json_code_details)
        result = await self.generate_text("Chapters", final_prompt, self.tokens, utils.get_role_content(2))
        if isinstance(result, Exception):
            self.logger.error("Error getting chapters for the project documentation")
            return None
        return utils.get_json_from_gpt_response(result[1])

    async def get_chapter_contents(self, init_overview: str, contents: Dict[str, list[str]], files: Dict[Path, str],
                                   prompt: str) -> List[Tuple[str, str]]:
        """Returns content of chapters"""
        tasks = []
        for chapter_name, chapter_files in contents.items():
            # path in chapter_files is relative
            try:
                temp_prompt = ""
                for req_file in chapter_files:
                    temp_file = Path(req_file)
                    temp_prompt += f"File Path: {req_file}\nCode: {files[temp_file]}"
                final_prompt = prompt.format(chapter_name, init_overview, temp_prompt)
                tasks.append(
                    asyncio.create_task(
                        self.generate_text(chapter_name, final_prompt, self.tokens, utils.get_role_content(3))
                    )
                )
            except Exception as excinfo:
                # sometime gpt responds with non-existing files
                self.logger.error(excinfo)

        final_result = []
        results = await asyncio.gather(*tasks)
        for result in results:
            if isinstance(result, Exception):
                self.logger.error("Task failed with exception: ", result)
            else:
                final_result.append(result)

        return final_result

    async def get_intro_content(self, init_overview: str, chapter_contents: List[Tuple[str, str]],
                                compression_prompt: str, intro_prompt: str) -> str:
        """Pass compressed version of contents of the all the chapters in the project
        to get a proper intro to the project"""
        tasks = []
        for name, contents in chapter_contents:
            final_prompt = compression_prompt.format(init_overview, contents)
            tasks.append(
                asyncio.create_task(self.generate_text(name, final_prompt, self.tokens, utils.get_role_content(4)))
            )
        results = await asyncio.gather(*tasks)
        compressed_contents = []

        for result in results:
            if isinstance(result, Exception):
                self.logger.error("Task failed with exception: ", result)
            else:
                compressed_contents.append(result)

        temp_prompt = ""
        for content in compressed_contents:
            temp_prompt += f"Chapter Name: {content[0]}\nChapter Overview: {content[1]}\n"

        final_prompt = intro_prompt.format(init_overview, temp_prompt)

        _, intro = await self.generate_text("Intro", final_prompt, self.tokens, utils.get_role_content(4))

        return intro

    @retry(
        stop=stop_after_attempt(5),
        # wait=wait_fixed(30),
        wait=wait_exponential(multiplier=1, min=10, max=30),
        retry=(
                retry_if_exception_type(Exception)
                | retry_if_exception_type(httpx.HTTPStatusError)
        ),
    )
    async def generate_text(
            self, index: str, prompt: str, tokens: int, role_contents: str
    ) -> Tuple[str, str]:
        """Handles the request to the OpenAi API to generate text"""
        try:
            token_count = get_token_count(prompt, self.encoding)

            if token_count > tokens:
                self.logger.debug(f"True Processing {index} \n token count{token_count}")
                prompt = truncate_tokens(prompt, tokens)
            # else:
            #     self.logger.debug(f"False Processing {index} \n token count: {token_count}")

            async with self.rate_limit_semaphore:
                response = await self.http_client.post(
                    self.endpoint,
                    headers={
                        "Content-Type": "application/json",
                        "api-key": self.api_key
                    },
                    json={
                        "messages": [
                            {
                                "role": "system",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": role_contents,
                                    }
                                ]
                            },
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    }
                                ]
                            }
                        ],
                        "temperature": self.temperature,
                        "top_p": 0.95,
                        "max_tokens": self.tokens_max
                    }
                )
                response.raise_for_status()
                data = response.json()
                summary = data["choices"][0]["message"]["content"]

                self.logger.info(
                    f"\nProcessing prompt: {index}\nResponse: {summary}"
                )
                self.cache[prompt] = summary
                return index, summary


        # don't know what those exceptions are and how they are being handled.
        # except openai.error.OpenAIError as excinfo:
        #     self.logger.error(f"OpenAI Exception:\n{str(excinfo)}")
        #     return await self.null_summary(
        #         index, f"OpenAI exception: {excinfo.response.status_code}"
        #     )

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
