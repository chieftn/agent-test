from typing import Literal

class SecretSourceSchema:
     def __init__(self, name: str, type: Literal['os', 'keyVault'], key_vault_name=""):
        self.name = name
        self.type = type
        self.key_vault_name = key_vault_name

