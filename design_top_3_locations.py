import pandas as pd

df = pd.read_csv("data/distance.csv")

grouped = df.groupby(["poll_id", "poll_lat", "poll_lon"])

num_aid_locations_to_include = 3

design_data = []

for name_tuple, group_df in grouped:

    design_row = {}

    nsmallest_df = group_df.nsmallest(
        n=num_aid_locations_to_include, columns="haversine"
    )

    design_row["poll_id"] = name_tuple[0]
    design_row["poll_lat"] = name_tuple[1]
    design_row["poll_lat"] = name_tuple[2]

    for idx, (_, row) in enumerate(nsmallest_df.iterrows()):
        design_row[f"{idx}_closest_aid_id_"] = row["aid_id"]
        design_row[f"{idx}_closest_dist"] = row["haversine"]

    design_data.append(design_row)

design_df = pd.DataFrame(design_data)
design_df.to_csv("data/design_top_3_locations.csv", index=False)
