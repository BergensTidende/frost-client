from frost import Frost

frost = Frost()
if report := frost.get_reports_available():
    print("Got report!")
    print(report.to_list())
