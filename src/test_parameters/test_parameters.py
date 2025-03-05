from pathlib import Path
import json

from .test_parameters_error import TestParametersError

def get_test_parameters(directory: str) -> dict[str]:
    path = Path(directory, ".parameters.json")

    if (not path.exists):
        return {}

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        return data
    except Exception as e:
        raise TestParametersError(path.name, e)