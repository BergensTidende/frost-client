from frost.client import Frost, APIError

frost = Frost()
report = frost.get_report_windrose(
    station_id=50540, from_time="2023-01-01T00:00:00Z", to_time="2024-12-31T23:59:59Z"
)
if report:
    print("Got report!")
    print(report.get_winddirections())
