class TestSecretsError(Exception):
    def __init__(self, filename, error):
        self.filename = filename
        self.error = error
        self.message = f"A problem occurred with secrets file: {filename}"
        super().__init__(f"{self.message}. {error}")