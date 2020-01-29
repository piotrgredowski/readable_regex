from typing import List

from readable_regex.consts import Anchors, Quantifiers


class ReadableRegexError(Exception):
    pass


def get_reg_str(func):
    def wrapper(self, *args, **kwargs):
        wrong_args = []
        for arg in args:
            if not (isinstance(arg, ReadableRegex) or isinstance(arg, str)):
                wrong_args.append(arg)
        if wrong_args:
            raise ReadableRegexError(f"Not a ReadableRegex instance: {wrong_args}")
        args: List[ReadableRegex]
        reg_strs = [arg if isinstance(arg, str) else arg.as_string() for arg in args]
        if len(reg_strs) == 1:
            reg_strs = reg_strs[0]
        return func(self, reg_strs)

    return wrapper


class ReadableRegex:
    reg_str: str = r""

    def __repr__(self):
        return f"<ReadableRegex('{self.as_string()}')"

    def as_string(self):
        return self.reg_str

    def range(self, from_, to):
        self.reg_str += f"{from_}-{to}"
        return self

    @get_reg_str
    def once_or_none(self, expression):
        if isinstance(expression, list):
            expression = "".join(expression)

        self.reg_str += f"{expression}{Quantifiers.ONCE_OR_NONE.value}"
        return self

    @get_reg_str
    def one_from(self, expression):
        self.reg_str += f"[{expression}]"
        return self

    @get_reg_str
    def group(self, expression):
        self.reg_str += f"({expression})"
        return self

    def times(self, number):
        self.reg_str += f"{{{number}}}"
        return self

    @get_reg_str
    def alt(self, expressions):
        "Alternative/OR"
        self.reg_str += "|".join(expressions)
        return self

    def start_of_string(self):
        self.reg_str += Anchors.START.value
        return self

    def end_of_string(self):
        self.reg_str += Anchors.END.value
        return self
