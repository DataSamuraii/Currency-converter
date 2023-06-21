import openai
import re

import tiktoken
from tiktoken import Tokenizer
from tiktoken.models import GPT2

def chunk_text(text, max_tokens=10000):
    tokenizer = Tokenizer(GPT2())
    all_tokens = tokenizer.encode(text)

    chunks = []
    current_chunk = []
    for token in all_tokens:
        if len(current_chunk) + len(token) > max_tokens:
            chunks.append(current_chunk)
            current_chunk = [token]
        else:
            current_chunk.append(token)

    if current_chunk:
        chunks.append(current_chunk)

    return [''.join(chunk) for chunk in chunks]

 openai.api_key = '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'


def num_tokens_from_messages(messages, model="gpt-3.5-turbo"):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    for message in messages:
        num_tokens += len(encoding.encode(message))

    return num_tokens


def chunk_text(text, max_tokens=10000):
    tokenizer = Tokenizer(models.Model(models.ByteLevelBPE, 'gpt2', None))
    token_list = list(tokenizer.tokenize(text))
    chunks = ['']
    chunk_id = 0
    for token in token_list:
        if len(chunks[chunk_id] + token) > max_tokens:
            chunks.append(token)
            chunk_id += 1
        else:
            chunks[chunk_id] += token
    return chunks


def make_api_calls(chunks):
    responses = []
    for chunk in chunks:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=chunk,
            max_tokens=10000
        )
        responses.append(response.choices[0].text.strip())
    return responses


def main():
    openai.api_key = 'your_api_key_here'

    with open('AI unlocked full.txt', 'r') as file:
        data = file.read()

    data = re.sub(r"WEBVTT\n\n", "", data)
    chunks = chunk_text(data)

    responses = make_api_calls(chunks)

    with open('AI unlocked full chaptered.txt', 'w') as file:
        for response in responses:
            file.write(response + "\n")


if __name__ == "__main__":
    main()