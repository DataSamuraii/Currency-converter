import openai
import tiktoken

openai.api_key = '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'


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not implemented for model {model}. 
            See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # ever


def get_chunks(text):
    """Splits text into chunks of at most 10k tokens."""
    messages = [{"content": text}]
    chunks = []
    while messages:
        chunk = ""
        while messages and num_tokens_from_messages([chunk] + messages) <= 10000:
            chunk += messages.pop(0)["content"]
        chunks.append({"content": chunk})
    return chunks


def main():
    with open("AI unlocked full.txt", "r", encoding="utf-8") as f:
        text = f.read()
    chunks = get_chunks(text)
    prompt = input("First you should sum up the whole text, then analyze it, extract chapter, and specify the chapter start timestamp. Don't write Chapter number in the Chapter name.")
    responses = []
    for chunk in chunks:
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt + chunk,
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.7,
        )
        responses.append(response.choices[0].text)

    with open("AI unlocked full chaptered.txt", "w") as f:
        f.write("\n".join(responses))


if __name__ == "__main__":
    main()
