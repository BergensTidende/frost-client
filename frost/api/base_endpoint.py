from __future__ import annotations

from typing import Any, Dict, Type

from pydantic import BaseModel, ValidationError

from frost.client import APIError, BaseClient


class BaseEndpoint:
    request_model: Type[BaseModel]
    response_model: Type[BaseModel]
    endpoint: str

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def validate_request(self, **kwargs) -> Dict[str, Any]:
        try:
            request_data = self.request_model(**kwargs)
            return request_data.dict(exclude_unset=True, by_alias=True)
        except ValidationError as e:
            raise APIError(
                {
                    "code": "Arguments validation error",
                    "message": e.json(),
                }
            ) from e

    def validate_response(self, response_json) -> BaseModel:
        try:
            return self.response_model(**response_json)
        except ValidationError as e:
            raise APIError(
                {
                    "code": "Response validation error",
                    "message": e.json(),
                }
            ) from e

    def get_data(self, **kwargs: Any) -> BaseModel:
        params = self.validate_request(**kwargs)
        response_json = self.client.make_request(self.endpoint, params)
        return self.validate_response(response_json)
