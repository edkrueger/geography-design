import pandas as pd
from _distance import euclidean, haversine

aid_df = pd.read_csv("data/aid.csv").rename(
    columns={"ids": "aid_id", "latitude": "aid_lat", "longitude": "aid_lon"}
)

poll_df = pd.read_csv("data/polling_stations.csv").rename(
    columns={"local_id": "poll_id", "lat": "poll_lat", "lon": "poll_lon"}
)

df = (
    pd.merge(poll_df, aid_df, how="cross")
    .assign(
        haversine=lambda df_: haversine(
            p1_lon=df_["poll_lon"],
            p1_lat=df_["poll_lat"],
            p2_lon=df_["aid_lon"],
            p2_lat=df_["aid_lat"],
        )
    )
    .assign(
        euclidean=lambda df_: euclidean(
            p1_lon=df_["poll_lon"],
            p1_lat=df_["poll_lat"],
            p2_lon=df_["aid_lon"],
            p2_lat=df_["aid_lat"],
        )
    )
)

df.to_csv("data/distance.csv", index=False)
