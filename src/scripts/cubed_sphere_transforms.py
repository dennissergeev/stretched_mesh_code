"""Coordinate transformations and cubed-sphere mesh visualisation."""
# Author: Thomas Melvin (Met Office)
# Co-author: Denis Sergeev (University of Exeter)

import numpy as np


def XYZ2llr(X, Y, Z):
    """Transform (X,Y,Z) to (lon,lat,radius) with lat within -pi/2 and pi/2."""
    radius = np.sqrt(X**2 + Y**2 + Z**2)
    lat = np.arcsin(Z / radius)
    lon = np.mod(np.arctan2(Y, X), 2 * np.pi)
    return np.array([lon, lat, radius])


def llr2XYZ(lon, lat, radius=1, radians=False):
    """Transform Cartesian (lon, lat, radius) position to (x,y,z)."""
    if not radians:
        lon = np.deg2rad(lon)
        lat = np.deg2rad(lat)
    x = radius * np.cos(lon) * np.cos(lat)
    y = radius * np.sin(lon) * np.cos(lat)
    z = radius * np.sin(lat)
    return np.array([x, y, z])


def alphabetaR2XYZ(alpha, beta, R, panel):
    """
    Transform (alpha,beta,R,panel) coordinates to (X,Y,Z).

    For use with equiangular meshes defined by alpha and beta.
    """
    x = R * np.tan(alpha)
    y = R * np.tan(beta)
    # r = np.sqrt(R**2 + x**2 + y**2)
    [X, Y, Z] = xyR2XYZ(x, y, R, panel)

    return [X, Y, Z]


def xyR2XYZ(x, y, R, panel):
    """
    Transform (x,y,R) to (x,y,z) for panels of an equidistant cubed sphere.

    Note: the rotations are applied analytically.
    """
    r = np.sqrt(R**2 + x**2 + y**2)
    if panel == 0:
        XYZ = [R * R / r, R * x / r, R * y / r]
    if panel == 1:
        XYZ = [-R * x / r, R * R / r, R * y / r]
    if panel == 2:
        XYZ = [-R * R / r, -R * x / r, R * y / r]
    if panel == 3:
        XYZ = [R * x / r, -R * R / r, R * y / r]
    if panel == 4:
        XYZ = [R * y / r, R * x / r, -R * R / r]
    if panel == 5:
        XYZ = [-R * y / r, R * x / r, R * R / r]
    return np.array(XYZ)


def alphabetaR2llr(alpha, beta, radius, panel):
    """Transform (alpha,beta,R,panel) maps to lat,lon,radius."""
    [X, Y, Z] = alphabetaR2XYZ(alpha, beta, radius, panel)
    [lon, lat, radius] = XYZ2llr(X, Y, Z)
    return [lon, lat, radius]


def rotate_latlon(lon, lat, lon_pole, lat_pole):
    """Rotate lat/lon coordinates to a new North Pole."""
    # Equations 8 and 9 of Nair + Jablonowski
    # See also Varkley 1984 for the original source.
    num = np.cos(lat) * np.sin(lon - lon_pole)
    denom = np.cos(lat) * np.sin(lat_pole) * np.cos(lon - lon_pole) - np.cos(
        lat_pole
    ) * np.sin(lat)
    lon_rotated = np.arctan2(num, denom)

    num = np.sin(lat) * np.sin(lat_pole) + np.cos(lat) * np.cos(
        lat_pole
    ) * np.cos(lon - lon_pole)
    lat_rotated = np.arcsin(num)
    return [lon_rotated, lat_rotated]


def alpha_constant_lines(alpha, panel, internal_res=30):
    """Get constant lines of the alpha coordinate."""
    beta_points = np.linspace(
        -np.pi / 4.0, np.pi / 4.0, num=internal_res, endpoint=True
    )
    lat_radians = np.empty(len(beta_points))
    lon_radians = np.empty(len(beta_points))
    for ii, beta in enumerate(beta_points):
        [lon_radians[ii], lat_radians[ii], height] = alphabetaR2llr(
            alpha, beta, 1.0, panel
        )

    return [lon_radians, lat_radians]


def beta_constant_lines(beta, panel, internal_res=30):
    """Get constant lines of the beta coordinate."""
    points = np.linspace(
        -np.pi / 4.0, np.pi / 4.0, num=internal_res, endpoint=True
    )
    lat_radians = np.empty(len(points))
    lon_radians = np.empty(len(points))
    for ii, alpha in enumerate(points):
        [lon_radians[ii], lat_radians[ii], height] = alphabetaR2llr(
            alpha, beta, 1.0, panel
        )

    return [lon_radians, lat_radians]


def rodrigues(v, k, alpha):
    """Rotate a vector v through an angle alpha (radians) around an axis k."""
    # normalize k
    k = k / np.sqrt(np.dot(k, k))
    vnew = (
        v * np.cos(alpha)
        + np.cross(k, v) * np.sin(alpha)
        + k * np.dot(v, k) * (1.0 - np.cos(alpha))
    )
    return vnew


def set_rotation(N, Nold=(0, 0, 1)):
    """
    Set up the rotation axis such that new north is N.

    If not specified then old North axis is z axis.
    """
    alpha = np.arccos(np.dot(N, Nold) / np.dot(N, N) / np.dot(Nold, Nold))
    k = np.cross(N, Nold)
    return k, alpha


def rotate_points(v, lonN, latN, beta):
    """
    Rotate Cartesian points on sphere.

    The new North axis passes through (lonN,latN),
    and then rotate through an angle beta(degrees) about this new North.
    """
    N = llr2XYZ(lonN, latN)
    k, alpha = set_rotation(N)
    vnew = np.zeros_like(v)
    for vi in range(len(v[0, :])):
        vt = rodrigues(v[:, vi], k, alpha)
        vnew[:, vi] = rodrigues(vt, N, np.deg2rad(beta))
    return vnew


def rotate_ll(lon, lat, lonN, latN, beta, radians=True):
    """
    Rotate lon/lat points on sphere.

    The new North axis passes through (lonN,latN),
    and then rotate through an angle beta(degrees) about this new North.
    """
    if radians:
        _lon = np.unwrap(lon, discont=np.pi)
        _lat = np.unwrap(lat, discont=np.pi)
    else:
        _lon = lon
        _lat = lat
    v = llr2XYZ(_lon, _lat, radians=radians)
    vnew = rotate_points(v, lonN, latN, beta)
    ll = XYZ2llr(vnew[0, :], vnew[1, :], vnew[2, :])
    return ll


def stretch(lat0, stretch_factor):
    """Transform latitude according to the Schmidt (1977) transform."""
    s = (1.0 - stretch_factor**2) / (1.0 + stretch_factor**2)
    lat = np.arcsin((s + np.sin(lat0)) / (1.0 + s * np.sin(lat0)))
    return lat


def add_panels_cart(
    ax, n=1, pole_lon=0.0, pole_lat=90.0, stretch_factor=1.0, **kwargs
):
    """
    Draw a cubed sphere mesh.

    The mesh is a Cn (with n = 1 the default, i.e just the panel boundaries)
    with the North Pole at (lonN, latN) and stetching factor
    using the Schmidt transform.
    """
    equi_ang_points = np.linspace(-np.pi / 4, np.pi / 4, n + 1)

    panel_corners = np.linspace(-np.pi / 4.0, np.pi / 4, 2)
    # panel_centers_lon = {0: 0, 1: 90, 2: 180, 3: 270, 4: 180, 5: 180}
    # panel_centers_lat = {0: 0, 1: 0, 2: 0, 3: 0, 4: 90, 5: -90}
    # panel_names = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5/N", 5: "6/S"}

    lon_pole = np.deg2rad(0)
    lat_pole = np.deg2rad(0)

    # For rotation
    theta = 0

    for panel in [0, 1, 2, 3, 4, 5]:
        for alpha in equi_ang_points:
            [radians_lon, radians_lat] = alpha_constant_lines(alpha, panel)
            [rotated_radians_lon, rotated_radians_lat0] = rotate_latlon(
                radians_lon, radians_lat, lon_pole, lat_pole
            )
            rotated_radians_lat = stretch(rotated_radians_lat0, stretch_factor)

            # rotated mesh ('post processed')
            ll = rotate_ll(
                rotated_radians_lon,
                rotated_radians_lat,
                pole_lon,
                pole_lat,
                theta,
                radians=True,
            )
            degrees_lon = np.rad2deg(np.unwrap(ll[0], discont=np.pi))
            degrees_lat = np.rad2deg(np.unwrap(ll[1], discont=np.pi))
            ax.plot(degrees_lon, degrees_lat, linewidth=0.25, **kwargs)

        for beta in equi_ang_points:
            [radians_lon, radians_lat] = beta_constant_lines(beta, panel)
            [rotated_radians_lon, rotated_radians_lat0] = rotate_latlon(
                radians_lon, radians_lat, lon_pole, lat_pole
            )
            rotated_radians_lat = stretch(rotated_radians_lat0, stretch_factor)

            # rotated mesh ('post processed')
            ll = rotate_ll(
                rotated_radians_lon,
                rotated_radians_lat,
                pole_lon,
                pole_lat,
                theta,
                radians=True,
            )
            degrees_lon = np.rad2deg(np.unwrap(ll[0], discont=np.pi))
            degrees_lat = np.rad2deg(np.unwrap(ll[1], discont=np.pi))
            ax.plot(degrees_lon, degrees_lat, linewidth=0.25, **kwargs)

        for alpha in panel_corners:
            [radians_lon, radians_lat] = alpha_constant_lines(alpha, panel)
            [rotated_radians_lon, rotated_radians_lat0] = rotate_latlon(
                radians_lon, radians_lat, lon_pole, lat_pole
            )
            rotated_radians_lat = stretch(rotated_radians_lat0, stretch_factor)

            # rotated mesh ('post processed')
            ll = rotate_ll(
                rotated_radians_lon,
                rotated_radians_lat,
                pole_lon,
                pole_lat,
                theta,
                radians=True,
            )
            degrees_lon = np.rad2deg(np.unwrap(ll[0], discont=np.pi))
            degrees_lat = np.rad2deg(np.unwrap(ll[1], discont=np.pi))
            ax.plot(degrees_lon, degrees_lat, linewidth=1.0, **kwargs)

        for beta in panel_corners:
            [radians_lon, radians_lat] = beta_constant_lines(beta, panel)
            [rotated_radians_lon, rotated_radians_lat0] = rotate_latlon(
                radians_lon, radians_lat, lon_pole, lat_pole
            )
            rotated_radians_lat = stretch(rotated_radians_lat0, stretch_factor)

            # rotated mesh ('post processed')
            ll = rotate_ll(
                rotated_radians_lon,
                rotated_radians_lat,
                pole_lon,
                pole_lat,
                theta,
                radians=True,
            )
            degrees_lon = np.rad2deg(np.unwrap(ll[0], discont=np.pi))
            degrees_lat = np.rad2deg(np.unwrap(ll[1], discont=np.pi))
            ax.plot(degrees_lon, degrees_lat, linewidth=1.0, **kwargs)
