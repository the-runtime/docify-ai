import tiktoken


def count_tokens_in_file(file_path: str, model: str = "gpt-4o-mini"):
    # Load the appropriate tokenizer for the model (gpt-4 or gpt-3.5-turbo, etc.)
    encoding = tiktoken.encoding_for_model(model)
    print("Encoding: ", encoding)
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Encode the text and count the tokens
    tokens = encoding.encode(text)
    token_count = len(tokens)

    return token_count


# Example usage:
file_path = "data.txt"  # Replace with your file path
tokens = count_tokens_in_file(file_path)
print(f"Token count: {tokens}")
