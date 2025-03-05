import json
import os

from pathlib import Path
from azure.keyvault.secrets import SecretClient
from azure.identity import AzureCliCredential

from .secrets import Secrets
from .secret_schema import SecretSchema
from .secret_source_schema import SecretSourceSchema
from .test_secrets_error import TestSecretsError

def get_test_secrets(directory: str) -> Secrets:
    path = Path(directory, ".secrets.json")

    if (not path.exists):
        return Secrets({}, [])

    try:
        with open(path, 'r') as f:
            data = json.load(f)

        sources = dict[SecretSourceSchema]()

        for key, value in data["sources"].items():
            sources[key] = SecretSourceSchema(name=key, type=value["type"], key_vault_name=value.get("keyVaultName"))

        secrets = dict[str]()
        for key, value in data["secrets"].items():
            secret_schema = SecretSchema(name=key, source_name=value["sourceName"], source_key=value["sourceKey"])
            source_schema = sources[secret_schema.source_name]
            secrets[key] = get_secret_value(secret_schema, source_schema)

        return Secrets(values=secrets, sensitive_data_fields=data["sensitiveData"])

    except Exception as e:
        raise TestSecretsError(path.name, e)

def get_secret_value(secret_schema: SecretSchema, source_schema: SecretSourceSchema) -> str:
    if (source_schema.type == 'os'):
        return get_secret_value_os(secret_schema, source_schema)

    if (source_schema.type == 'keyVault'):
        return get_secret_value_keyVault(secret_schema, source_schema)

    return ""

def get_secret_value_keyVault(secret_schema: SecretSchema, source_schema: SecretSourceSchema) -> str:
    kv_uri = f"https://{source_schema.key_vault_name}.vault.azure.net"
    credential = AzureCliCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    secret = client.get_secret(secret_schema.source_key)

    if (secret):
        return secret.value

    return ""

def get_secret_value_os(secret_schema: SecretSchema, source_schema: SecretSourceSchema) -> str:
    return os.environ.get(secret_schema.source_key) or ""
