"""Creates a design matrix with, for each polling station, for each aid program, 
the minimum distance from the polling station to the closest location for the aid program
and the count of aid location with in a 60km radius of the polling station."""

import pandas as pd
import numpy as np

df = pd.read_csv("data/distance.csv").assign(
    aid_id=lambda df_: df_["aid_id"].str.split("_", expand=True)[0]
)

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

agg_df.to_csv("data/design_program_level.csv")
