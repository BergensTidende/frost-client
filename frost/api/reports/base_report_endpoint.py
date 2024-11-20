from frost.api import BaseEndpoint


class BaseReportEndpoint(BaseEndpoint):
    report_type: str  # Each report will specify its type

    def get_data(self, **kwargs):
        # The request model is expected to be the settings for the report
        params = self.validate_request(**kwargs)
        # For reports, the 'settings' parameter is a JSON string
        settings_json = params.get("settings", "{}")

        request_params = {
            "type": self.report_type,
            "settings": settings_json,
        }

        response_json = self.client.make_request("reports", request_params)
        return self.validate_response(response_json)
