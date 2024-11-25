from frost import Frost

frost = Frost()
obs = frost.get_lightning(
    reference_time="latest", format="json"
)

if obs is None:
    print("No observations")
    exit()
print ("obs")

df = obs.to_df()
print(df.head())
