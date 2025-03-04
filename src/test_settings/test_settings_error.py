class TestSettingsError(Exception):
    def __init__(self, filename, error):
        self.filename = filename
        self.error = error
        self.message = f"A problem occurred with settings file: {filename}"
        super().__init__(f"{self.message}. {error}")