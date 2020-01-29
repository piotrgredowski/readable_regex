import re

from readable_regex import ReadableRegex as RR


class TestStringClass:
    def test_range(self):
        assert RR().range("A", "Z").as_string() == "A-Z"

    def test_times(self):
        assert RR().times(5).as_string() == "{5}"

    def test_once_or_none(self):
        assert RR().once_or_none(RR().range("A", "Z")).as_string() == "A-Z?"

    def test_hex(self):
        """Want to get regex that validates hex value as output:
        /^#?([a-f0-9]{6}|[a-f0-9]{3}|[A-F0-9]{6}|[A-F0-9]{3})$/
        """

        rr = RR()

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
