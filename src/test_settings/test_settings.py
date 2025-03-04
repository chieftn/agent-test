import json

from pathlib import Path
from test_secrets import Secrets

from .test_settings_error import TestSettingsError
from .settings import Settings
from .settings_model import ModelSettings

def get_test_settings(directory: str, secrets: Secrets) -> Settings:
    path = Path(directory, ".settings.json")

    if (not path.exists):
        raise TestSettingsError(path.name)

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        model_settings = get_model_settings(secrets, data["azureOpenAI"])
        return Settings(model_settings)

    except Exception as e:
        raise TestSettingsError(path.name, e)

def get_model_settings(secrets: Secrets, settings: any) -> ModelSettings:
    return ModelSettings(
        key=get_setting(secrets, settings["key"]),
        endpoint=get_setting(secrets, settings["endpoint"]),
        model=get_setting(secrets, settings["model"]),
        deployment=get_setting(secrets, settings["deployment"]),
        version=get_setting(secrets, settings["version"])
    )

def get_setting(secrets: Secrets, entry: any) -> str:
    secretName = entry.get("secretName")
    if (secretName != None):
        return secrets.values[secretName]

    return entry["value"]
