import re
import string


def find_first_non_repeating_char(text):
    words = text.split()
    unique_chars = []

    for word in words:
        # Remove punctuation from the word
        word = re.sub(f'[{string.punctuation}]', '', word)

        for char in word:
            if word.count(char) == 1:
                unique_chars.append(char)
                break  # move to the next word once we've found a unique char

    # Now find the first non-repeating char in unique_chars
    for char in unique_chars:
        if unique_chars.count(char) == 1:
            return char

    return None  # If there's no non-repeating char


text = 'C makes it easy for you to shoot yourself in the foot. C++ makes that harder, but when you do, it blows away your whole leg. (с) Bjarne Stroustrup'
print(find_first_non_repeating_char(text))  # e
