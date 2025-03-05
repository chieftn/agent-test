from typing import Literal

class TestResult:
    def __init__(self, suite_name: str, series_name: str, name: str, result: Literal['pass', 'fail'], message: str = ""):
        self.suite_name = suite_name
        self.series_name = series_name
        self.name = name
        self.result = result
        self.message = message


