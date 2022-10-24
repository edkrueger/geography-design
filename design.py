import pandas as pd

df = pd.read_csv("data/distance.csv")

agg_df = df.pivot_table(
    index=["poll_id", "poll_lat", "poll_lon"], columns="aid_id", values="haversine"
).reset_index()

agg_df.to_csv("data/design.csv", index=False)