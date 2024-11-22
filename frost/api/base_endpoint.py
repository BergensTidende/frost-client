from __future__ import annotations

from typing import Any, Dict, Generic, Type, TypeVar, Union

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

    def get_data(self, **kwargs: Any) -> Union[ResponseType, str]:
        # Map kwargs to aliases
        model = self.request_model
        aliased_kwargs = {
            model.model_fields[field].alias or field: value
            for field, value in kwargs.items()
            if field in model.model_fields
        }

        params = self.validate_request(**aliased_kwargs)
        response_data = self.client.make_request(self.endpoint, params)

        # Return raw text if UALF format is requested
        if params.get("format") == "ualf":
            if not isinstance(response_data, str):
                raise ValueError("Expected raw string for UALF format")
            return response_data

        return self.validate_response(response_data)
