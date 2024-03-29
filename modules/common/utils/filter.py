def remove_punctuation_marks(text: str) -> str:
    return "".join([char for char in text if char not in set("!\"#$%&()*+-,/:;<=>?@[\\]^_`{|}~.")])
