from frost.client import Frost, APIError

frost = Frost()
report = frost.get_reports_available()
if report:
    print("Got report!")
    print(report.to_list())

frost.