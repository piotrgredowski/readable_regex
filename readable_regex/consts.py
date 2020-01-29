from enum import Enum


class Characters(Enum):
    DIGIT = r"\d"
    WORD_CHAR = r"\w"
    WHITESPACE_CHAR = r"\s"
    NOT_DIGIT = r"\D"
    NOT_WORD_CHAR = r"\W"
    NOT_WHITESPACE_CHAR = r"\S"


class Anchors(Enum):
    START = r"^"
    END = r"$"


class Quantifiers(Enum):
    ONCE_OR_NONE = r"?"

