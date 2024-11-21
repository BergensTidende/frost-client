from typing import Any, Mapping, Optional


class APIError(Exception):
    code: Optional[str]
    message: Optional[str]

    def __init__(self, error_data: Mapping[str, Any]) -> None:
        self.code = error_data.get("code")
        self.message = error_data.get("message")
        super().__init__(self.message)
