from frost.client import Frost, APIError

frost = Frost()
obs = frost.get_report_windrose(
    stationId="50540", fromTime="2023-01-01T00:00:00Z", toTime="2024-12-31T23:59:59Z"
)
df = obs.to_df()
