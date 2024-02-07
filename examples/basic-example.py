from frost.client import Frost, APIError

frost = Frost()
obs = frost.get_observations(stationids="18700,50540", elementids="air_temperature, wind_speed")
df = obs.to_df()
df.to_csv("observations.csv", index=False)
list = obs.to_list()
f = open("observations.json", "w")
f.write(str(list))
f.close()


