from typing import Type

from pydantic import BaseModel, ValidationError

from frost.client.exceptions import APIError


class BaseEndpoint:
    request_model: Type[BaseModel]
    response_model: Type[BaseModel]
    endpoint: str

    def __init__(self, client):
        self.client = client

    def validate_request(self, **kwargs):
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

    def validate_response(self, response_json):
        try:
            return self.response_model(**response_json)
        except ValidationError as e:
            raise APIError(
                {
                    "code": "Response validation error",
                    "message": e.json(),
                }
            ) from e

    def get_data(self, **kwargs):
        params = self.validate_request(**kwargs)
        response_json = self.client.make_request(self.endpoint, params)
        return self.validate_response(response_json)
