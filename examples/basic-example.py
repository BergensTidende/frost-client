from frost.client import Frost, APIError

frost = Frost()
obs = frost.get_observations(
    station_ids="18700,50540", element_ids="air_temperature, wind_speed"
)

if obs is None:
    print("No observations")
    exit()

df = obs.to_df()
print(df.head())
