from __future__ import annotations

from os import getenv
from typing import List, Optional, Union, cast, Any
from pydantic import ValidationError
from urllib.parse import urljoin

import requests
from dotenv import load_dotenv
import json

from frost.api.models import ObsMetNoFilterParams
from frost.models import ObservationsResponse

load_dotenv()


class APIError(Exception):
    """Raised when the API responds with a 400 or 404"""

    code: Optional[str]
    message: Optional[str]
    reason: Optional[str]

    def __init__(self, e) -> None:
        self.code = e.get("code")
        self.message = e.get("message")
        self.reason = e.get("reason")


class Frost(object):

    """Interface to frost.met.no API

    The Frost API key should be exposed as a environment variable called

    `FROST_API_KEY`

    or passed as a username parameter when creating and instance of the class.

    >>>  frost = Frost(username="myapikey")
    """

    def __init__(
        self, client_id: Optional[str] = None, client_secret: Optional[str] = None
    ) -> None:
        """
        :param str username: your own frost.met.no username/key.
        """
        self.base_url = "https://frost-beta.met.no"
        self.api_version = "v1"
        self.session = requests.Session()
        self.client_id = client_id or getenv("FROST_CLIENT_ID", None)
        self.client_secret = client_secret or getenv("FROST_CLIENT_SECRET", None)

        if self.client_id is None:
            raise ValueError(
                """
                You must provide a client_id parameter
                or set the FROST_CLIENT_ID environment variable to
                use the Frost class
                """
            )
        if self.client_secret is None:
            raise ValueError(
                """
                You must provide a client_secret parameter
                or set the FROST_CLIENT_SECRET environment variable to
                use the Frost class
                """
            )

        self.session.auth = (self.client_id, self.client_secret)

    def let_it_go(self) -> str:
        return """
        Let it go, let it go
        Can't hold it back anymore
        Let it go, let it go
        Turn away and slam the door
        I don't care what they're going to say
        Let the storm rage on
        The cold never bothered me anyway
        """

    def make_request(
        self,
        endpoint: str,
        **kwargs,
    ) -> Any:
        url = urljoin(self.base_url, f"api/{self.api_version}/{endpoint}/get?")

        try:
            # Validate the arguments
            params = ObsMetNoFilterParams(**kwargs)
        except ValidationError as e:
            # Handle the validation error
            print("Validation error:", e.json())
            return None

        # Convert the validated parameters to a dictionary
        parameters_dict = params.dict(exclude_unset=True)

        if "incobs" in parameters_dict:
            parameters_dict["incobs"] = str(parameters_dict["incobs"]).lower()

        # Make the request with the validated and structured parameters
        try:
            response = self.session.get(url, params=parameters_dict, timeout=60)
            response.raise_for_status()

            # If we got the status code for success
            if response.status_code == 200:
                json = response.json()
                if "data" in json:
                    return json["data"]
                if "error" in json:
                    raise APIError(json["error"])

            # If we got an error type status code (request failed)
            else:
                print("Error:")
                print("\tstatus code: {}".format(response.status_code))

        except requests.RequestException as e:
            # Handle exceptions related to the request
            print("Request error:", str(e))
            return None

        # json = response.json()

        # print(json)

        # if "data" in json:
        #     return json["data"]
        # if "error" in json:
        #     raise APIError(json["error"])
        # else:
        #     raise APIError(
        #         {
        #             "code": "no data",
        #             "message": "no data field in json",
        #         }
        #     )

    def get_observations(
        self,
        incobs: bool = True,
        time: str = "latest",
        location: Optional[str] = None,
        stationids: Optional[str | List[str]] = None,
        elementids: Optional[str | List[str]] = None,
        nearest: Optional[str] = None,
        polygon: Optional[str] = None,
    ) -> Any:
        # Convert stationids and elementids to comma separated strings if they are lists
        if type(stationids) == list:
            stationids = ",".join(stationids)
        if type(elementids) == list:
            elementids = ",".join(elementids)

        parameters = {
            "stationids": stationids,
            "incobs": incobs,
            "time": time,
        }

        if location != None:
            parameters["location"] = time

        if elementids != None:
            parameters["elementids"] = elementids

        if nearest != None:
            parameters["nearest"] = nearest

        if polygon != None:
            parameters["polygon"] = polygon

        data = self.make_request("obs/met.no/filter", **parameters)
        o = ObservationsResponse(data)

        if o.data:
            return o
        else:
            return None
