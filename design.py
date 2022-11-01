import pandas as pd
import numpy as np

df = pd.read_csv("data/distance.csv")

min_dist_df = df.pivot_table(
    index=["poll_id", "poll_lat", "poll_lon"],
    columns="aid_id",
    values="haversine",
    aggfunc=np.min,
).rename(columns=lambda col: f"{col}_min_dist")

count_df = (
    df.loc[lambda df_: df_["haversine"] <= 60]
    .pivot_table(
        index=["poll_id", "poll_lat", "poll_lon"],
        columns="aid_id",
        values="haversine",
        aggfunc=len,
    )
    .rename(columns=lambda col: f"{col}_count")
    # polling locations are generally not close enough to all aid locations
    .fillna(0)
)


agg_df = (
    pd.concat([min_dist_df, count_df], axis="columns")
    # some polling stations are not close enough to any aid locations
    .fillna(0)
)

agg_df.to_csv("data/design.csv")
