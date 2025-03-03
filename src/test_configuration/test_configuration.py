from pathlib import Path
import json

from test_configuration_error import TestConfigurationError

def get_test_suite_configuration(directory: str) -> dict:
    path = Path(directory, ".config.json")
    if (not path.exists):
        return {}

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        return data
    except Exception as e:
        raise TestConfigurationError(path.name, e)