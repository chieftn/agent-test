from .test import Test

class TestSeries:
    def __init__(self, name):
        self.name = name
        self.tests = []

    def add_test(self, test: Test):
        self.tests.append(test)
