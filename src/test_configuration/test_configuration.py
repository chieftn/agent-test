from pathlib import Path
import json

from .test_configuration_error import TestConfigurationError
from .test_configuration_settings import TestConfigurationSettings

def get_test_configuration(directory: str) -> TestConfigurationSettings:
    path = Path(directory, ".config.json")

    if (not path.exists):
        return TestConfigurationError(allowed_domains=[], test_settings={})

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        return TestConfigurationSettings(
            allowed_domains=data["allowedDomains"],
            test_settings=data["testSettings"],
        )
    except Exception as e:
        raise TestConfigurationError(path.name, e)