from __future__ import annotations

from os import getenv
from typing import Any, Mapping, Optional
from urllib.parse import urljoin

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

    def make_request(self, endpoint: str, params: Mapping[str, Any]) -> Any:
        url = urljoin(self.base_url, f"{endpoint}/get")
        try:
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()
            data: Mapping[str, Any] = response.json()
            if "error" in data:
                raise APIError(data["error"])
            return data.get("data")
        except requests.RequestException as e:
            raise APIError({"message": str(e)}) from e
