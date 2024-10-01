from tiktoken import encoding_for_model, encoding_name_for_model, get_encoding, Encoding

from docifyai.core import logger

logger = logger.Logger(__name__)


def adjust_max_tokens(
        max_tokens: int, prompt: str, target: str = "Hello!"
) -> int:
    """Adjust the maximum number of tokens on the specific prompt."""
    is_valid_prompt = prompt.strip().startswith(target.strip())
    adjusted_max_tokens = max_tokens if is_valid_prompt else max_tokens // 3
    return adjusted_max_tokens


def get_token_count(text: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = get_encoding(encoding_name)
    num_tokens = len(encoding.encode(text))
    return num_tokens


# def get_token_encoder() -> Encoding:
#     """The token encoder to use for the model."""
#     return (
#         encoding_for_model("gpt-3.5-turbo")
#         if "gpt"
#         else get_encoding("cl199k_base")
#     )


# need to change this as we have to send alot of data
# can't lose code data like this
# may have to break the code base info parts and send to the model in the same context


def truncate_tokens(text: str, max_tokens: int) -> str:
    """Truncate a text string to a maximum number of tokens."""
    # needs an implementation
    if not text:
        return text
    try:
        encoder = encoding_for_model("gpt-4o-mini")

        prompt_token_total = len(encoder.encode(text))
        if prompt_token_total <= max_tokens:
            return text
        char_total = len(text)
        chars_per_token = char_total / prompt_token_total
        truncated_total = int(chars_per_token * max_tokens)
        return text[:truncated_total]

    except Exception as excinfo:
        logger.error(f"Error truncating tokens: {excinfo}")
        return text
