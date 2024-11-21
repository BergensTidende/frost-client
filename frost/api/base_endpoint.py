from __future__ import annotations

from typing import Any, Dict, Generic, Type, TypeVar

from pydantic import BaseModel, ValidationError

from frost.client import BaseClient
from frost.errors import APIError

# Type variables for request and response models
RequestType = TypeVar("RequestType", bound=BaseModel)
ResponseType = TypeVar("ResponseType", bound=BaseModel)


class BaseEndpoint(Generic[RequestType, ResponseType]):
    request_model: Type[RequestType]
    response_model: Type[ResponseType]
    endpoint: str

    def __init__(self, client: BaseClient) -> None:
        self.client = client

    def validate_request(self, **kwargs: Any) -> Dict[str, Any]:
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

    def validate_response(self, response_json: Any) -> ResponseType:
        try:
            return self.response_model(**response_json)
        except ValidationError as e:
            raise APIError(
                {
                    "code": "Response validation error",
                    "message": e.json(),
                }
            ) from e

    def get_data(self, **kwargs: Any) -> ResponseType:
        params = self.validate_request(**kwargs)
        response_json = self.client.make_request(self.endpoint, params)
        return self.validate_response(response_json)
