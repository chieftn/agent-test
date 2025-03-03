from .test_series import TestSeries

class TestSuite:
    def __init__(self, name: str):
        self.name = name
        self.series = []

    def add_series(self, series: TestSeries):
        self.series.append(series)
