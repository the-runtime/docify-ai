from tiktoken import encoding_for_model, get_encoding

from core import logger

logger = logger.Logger(__name__)


# def adjust_max_tokens(
#         max_tokens: int, prompt: str, target: str = "Hello!"
# ) -> int:
#     """Adjust the maximum number of tokens based on th specific prompt."""
#     is_valid_pr

def get_token_count(text: str, encoding_name: str) -> int:
    """Returns the number of tokens in atext string."""
    encoding = get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens
