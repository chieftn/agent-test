import toml
from pathlib import Path
from typing import List

from test_configuration import TestConfigurationSettings

from .test_suite import TestSuite
from .test_series import TestSeries
from .test import Test
from .test_suite_parse_error import TestSuiteParseError


def get_test_suite_paths(directory: str) -> List[Path]:
    path = Path(directory)
    file_extension = '.toml'

    path_list = path.rglob(f'*{file_extension}')
    return path_list

def get_test_suite(path: Path, configuration: TestConfigurationSettings) -> TestSuite:
    test_suite = TestSuite(path.name)

    try:
        with open(path, 'r') as f:
            config = toml.load(f)

        for index in range(len(config['describe'])):
            series_content = config['describe'][index]
            series_name = series_content['name']

            test_series = TestSeries(series_name)

            for index in range(len(series_content['it'])):
                test_content = series_content['it'][index]

                test_name = str(test_content['name'])
                test_act = str(test_content['act']).format_map(configuration.test_settings)
                test_expect = str(test_content['expect']).format_map(configuration.test_settings)
                test = Test(test_name, test_act, test_expect)

                test_series.add_test(test)

            test_suite.add_series(test_series)

    except Exception as e:
        raise TestSuiteParseError(path.name, e)

    return test_suite