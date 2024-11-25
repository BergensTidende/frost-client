from frost import Frost

frost = Frost()
if report := frost.get_reports_available(type="windrose"):
    print("Got report!")
    print(report.to_list())
