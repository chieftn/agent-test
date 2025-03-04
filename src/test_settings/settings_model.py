class ModelSettings:
     def __init__(self, key: str, endpoint: str, model: str, deployment: str, version: str):
        self.key = key
        self.endpoint = endpoint
        self.model = model
        self.deployment = deployment
        self.version = version