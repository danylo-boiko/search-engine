from re import escape, sub
from string import punctuation


def remove_punctuation(text: str) -> str:
    return sub(f"[{escape(punctuation)}]", "", text)
