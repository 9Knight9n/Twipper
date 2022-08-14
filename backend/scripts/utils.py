import string


def remove_punctuation(text: str):
    text = text.replace("&amp;", " ")
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text
