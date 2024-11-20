import requests
from os import getenv
from urllib.parse import urljoin

from frost.client.exceptions import APIError

class BaseClient:
    def __init__(self, client_id=None, client_secret=None):
        self.base_url = "https://frost-beta.met.no/api/v1/"
        self.session = requests.Session()
        self.client_id = client_id or getenv("FROST_CLIENT_ID")
        self.client_secret = client_secret or getenv("FROST_CLIENT_SECRET")

        if not self.client_id or not self.client_secret:
            raise ValueError("Client ID and client secret must be provided.")

        self.session.auth = (self.client_id, self.client_secret)

    def make_request(self, endpoint, params):
        url = urljoin(self.base_url, f"{endpoint}/get")
        try:
            response = self.session.get(url, params=params, timeout=60)
            response.raise_for_status()
            data = response.json()
            if "error" in data:
                raise APIError(data["error"])
            return data.get("data")
        except requests.RequestException as e:
            raise APIError({"message": str(e)}) from e
