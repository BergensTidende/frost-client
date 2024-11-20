class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, error_data):
        self.code = error_data.get("code")
        self.message = error_data.get("message")
        super().__init__(self.message)
