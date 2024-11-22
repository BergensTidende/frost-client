from frost import Frost

frost = Frost()
obs = frost.get_lightning(reference_time="latest", format="ualf")

if obs is None:
    print("No observations")
    exit()

df = obs.to_df()
print(df.head())

print(obs.to_list())
