from azure.keyvault.secrets import SecretClient
from azure.identity import AzureCliCredential

def get_secret(subscription, keyVaultName, kv_uri, secretName):
    credential = AzureCliCredential()
    client = SecretClient(vault_url=kv_uri, credential=credential)

    print(f'Clients established.')
    print(f'Getting test user secret {secretName}...')

    password = client.get_secret(secretName)

    if (password):
        return password.value
    else:
        return None
