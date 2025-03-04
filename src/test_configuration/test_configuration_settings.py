class TestConfigurationSettings:
    def __init__(self, allowed_domains: list[str], test_settings: dict):
        self.allowed_domains = allowed_domains
        self.test_settings = test_settings