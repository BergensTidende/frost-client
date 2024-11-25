from __future__ import annotations

from os import getenv
from typing import Any, Optional

import requests

from frost.errors.exceptions import APIError


class BaseClient:
    base_url: str
    session: requests.Session
    client_id: str
    client_secret: str

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ) -> None:
        self.base_url = "https://frost-beta.met.no/api/v1/"
        self.session = requests.Session()
        self.client_id = client_id or getenv("FROST_CLIENT_ID") or ""
        self.client_secret = client_secret or getenv("FROST_CLIENT_SECRET") or ""

        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and client secret must be provided.")

        self.client_id = str(self.client_id)
        self.client_secret = str(self.client_secret)

        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and client secret must be provided.")

        self.session.auth = (self.client_id, self.client_secret)

    def make_request(self, endpoint: str, params: dict[str, Any]) -> Any:
        # make sure that params are viable for the request
        # transform boolean values to string
        for key, value in params.items():
            if isinstance(value, bool):
                params[key] = str(value).lower()
            if value is None:
                del params[key]

        url = f"{self.base_url}{endpoint}/get"

        try:
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()

            # Detect content type or format
            if params.get("format") == "ualf" or response.headers.get(
                "Content-Type", ""
            ).startswith("text/"):
                return response.text

            # Handle JSON responses
            if response.headers.get("Content-Type", "").startswith("application/json"):
                try:
                    data = response.json()

                except ValueError:
                    # JSON decoding failed (likely an empty page)
                    return None

                return data["data"] if "data" in data else data

            # For unsupported content types, raise an error
            raise APIError(
                {
                    "message": f"""Unsupported response format:
                    {response.headers.get('Content-Type')}""",
                }
            )

        except requests.RequestException as e:
            raise APIError({"message": str(e)}) from e
