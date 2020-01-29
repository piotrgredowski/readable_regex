# readable_regex

Write regex as (nearly) natural language.

## Idea

For now this is only a simple proof of concept which shows how can it work.
I am still not convinced that this is a good idea - I have to adapt it to handle
more complicated regex tools like lookarounds. Then I can see if it's much more
readable than usual regex.

In the future it could validate your regex. For example could say that range `b-a` has no sense
because it won't get you any matches.

Feel free to write about your feelings in GH issues or directly to me via email: piotrgredowski@gmail.com

```python
import re

from readable_regex import ReadableRegex as RR

rr = RR()

# Want to get regex that validates hex value:
# /^#?([a-f0-9]{6}|[a-f0-9]{3}|[A-F0-9]{6}|[A-F0-9]{3})$/

rr.start_of_string().once_or_none("#").group(
    RR().alt(
        RR().one_from(RR().range("a", "f").range("0", "9")).times(6),
        RR().one_from(RR().range("a", "f").range("0", "9")).times(3),
        RR().one_from(RR().range("A", "F").range("0", "9")).times(6),
        RR().one_from(RR().range("A", "F").range("0", "9")).times(3),
    )
).end_of_string()

expected = "^#?([a-f0-9]{6}|[a-f0-9]{3}|[A-F0-9]{6}|[A-F0-9]{3})$"

assert rr.as_string() == expected

ok_hexs = [
    "fafafa",
    "#abcdef",
    "000000",
    "#fea",
    "111",
    "FFFFFF",
    "#FA1209",
    "#F12",
]
for ok_hex in ok_hexs:
    res = re.match(rr.as_string(), ok_hex).groups()
    assert res[0] == ok_hex.strip("#")

not_ok_hexs = ["gaa", "0909", "##ffffaa", "#FfFFFF", "a9E"]
for not_ok_hex in not_ok_hexs:
    res = re.match(rr.as_string(), not_ok_hex)
    assert res is None
```

## Development

Prepare virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

To run tests:

```bash
pytest tests/test_setup.py tests/*
```
