import pandas as pd
import numpy as np

df = pd.read_csv("data/distance.csv")

agg_df = df.pivot_table(
    index=["poll_id", "poll_lat", "poll_lon"],
    columns="aid_id",
    values="haversine",
    aggfunc=np.min,
).reset_index()

agg_df.to_csv("data/design.csv", index=False)
