import pandas as pd
import geopandas as gpd

pd.options.display.max_columns = None

CRS = "EPSG:4326"

shape_gdf = gpd.read_file("data/BRA_adm2.shp").rename(
    columns={"NAME_2": "muni_name", "ID_2": "muni_id"}
)[["muni_id", "muni_name", "geometry"]]

aid_df = (
    pd.read_csv("data/aid.csv").rename(
        columns={"ids": "aid_id", "latitude": "aid_lat", "longitude": "aid_lon"}
    )
    # take only the program level of aid_id
    .assign(aid_id=lambda df_: df_["aid_id"].str.split("_", expand=True)[0])
)

poll_df = pd.read_csv("data/polling_stations.csv").rename(
    columns={"local_id": "poll_id", "lat": "poll_lat", "lon": "poll_lon"}
)

assert poll_df["poll_id"].is_unique

aid_gdf = gpd.GeoDataFrame(
    aid_df, geometry=gpd.points_from_xy(aid_df["aid_lon"], aid_df["aid_lat"], crs=CRS)
)

poll_gdf = gpd.GeoDataFrame(
    poll_df,
    geometry=gpd.points_from_xy(poll_df["poll_lon"], poll_df["poll_lat"], crs=CRS),
)

# There are some polling and aid locations
# that are very slightly outside of the shape.

# The strategy is to find the nearest municipality.
# Since the distance is so slight,
# I don't bother to reproject onto a geometric CRS.

# I use an inner join and then check the number of rows,
# in order to confirm there are no locations outside
# of the shapes by more than the distance.

# roughly 5 km
max_distance = 0.05

aid_muni_gdf = gpd.sjoin_nearest(
    aid_gdf, shape_gdf, how="inner", max_distance=max_distance
)[["aid_id", "aid_lat", "aid_lon", "geometry", "muni_id", "muni_name"]]

poll_muni_gdf = gpd.sjoin_nearest(
    poll_gdf, shape_gdf, how="inner", max_distance=max_distance
)[["poll_id", "poll_lat", "poll_lon", "geometry", "muni_id", "muni_name"]]

assert len(aid_muni_gdf) == len(aid_df)
assert len(poll_muni_gdf) == len(poll_df)

# Naive method causes the kernel to crash.
# Passing `dropna=False` to `.pivot_table` causes the kernel to crash.

# The strategy is to calculate the design matrix in two parts:
# * where polling locations that have aid locations in their municipality
# * where they don't
# I then concatenate the results and verify that no rows are missing.

inner_df = pd.merge(poll_muni_gdf, aid_muni_gdf, on="muni_id", how="inner")

inner_design_df = (
    inner_df.loc[:, ["poll_id", "poll_lat", "poll_lon", "aid_id"]]
    .assign(aid_id_copy=lambda df_: df_["aid_id"])
    .pivot_table(
        index=["poll_id", "poll_lat", "poll_lon"],
        columns="aid_id",
        values="aid_id_copy",
        aggfunc=len,
    )
)

left_only_design_df = (
    pd.merge(poll_muni_gdf, aid_muni_gdf, on="muni_id", how="left")
    .loc[lambda df_: df_["aid_id"].isna(), ["poll_id", "poll_lat", "poll_lon"]]
    .set_index(["poll_id", "poll_lat", "poll_lon"])
)

# a NaN value indicates there are no (0)
# locations for the aid program
# in the same municipality as the polling station
poll_design_df = (
    pd.concat([inner_design_df, left_only_design_df])
    .fillna(0)
    .rename(columns=lambda col: f"{col}_muni_count")
)

assert len(poll_design_df) == len(poll_df)

poll_design_df.to_csv("data/design_hybrid_muni_level.csv", index=True)