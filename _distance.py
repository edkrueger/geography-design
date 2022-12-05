import numpy as np

def haversine(p1_lon, p1_lat, p2_lon, p2_lat):

    p1_lon_r, p1_lat_r, p2_lon_r, p2_lat_r = map(
        np.radians, [p1_lon, p1_lat, p2_lon, p2_lat]
    )

    d_lon_r = p2_lon_r - p1_lon_r
    d_lat_r = p2_lat_r - p1_lat_r

    partial = (
        np.sin(d_lat_r / 2) ** 2
        + np.cos(p1_lat_r) * np.cos(p2_lat_r) * np.sin(d_lon_r / 2) ** 2
    )
    d_r = 2 * np.arcsin(np.sqrt(partial))

    # note: the Earth is not perfectly spherical,
    # so there isn't one right number,
    # so, I picked one
    radius_of_earth_km = 6367

    return radius_of_earth_km * d_r


def euclidean(p1_lon, p1_lat, p2_lon, p2_lat):

    p1_lon_r, p1_lat_r, p2_lon_r, p2_lat_r = map(
        np.radians, [p1_lon, p1_lat, p2_lon, p2_lat]
    )

    d_lon_r = p2_lon_r - p1_lon_r
    d_lat_r = p2_lat_r - p1_lat_r

    d_r = np.sqrt(d_lon_r**2 + d_lat_r**2)

    # note: the Earth is not perfectly spherical,
    # so there isn't one right number,
    # so, I picked one
    radius_of_earth_km = 6367

    return radius_of_earth_km * d_r