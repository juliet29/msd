import matplotlib.pyplot as plt
import polars as pl
import shapely as sp
from shapely import plotting as shapely_plt

from msd1.geometry import rotate_multipolygon
from msd1.main import MSDSchema


def rotate_areas_in_unit(unit_df: pl.DataFrame, plot=False):
    df = MSDSchema.validate(unit_df)
    polygons = [sp.from_wkt(row["geom"]) for row in df.iter_rows(named=True)]

    multpol = sp.MultiPolygon(polygons)
    bound_rect: sp.Polygon = multpol.minimum_rotated_rectangle.normalize()  # type: ignore

    angle = rotate_multipolygon(multpol)

    rotated_bound_rect = sp.affinity.rotate(bound_rect, angle, use_radians=True)
    rotated_multpol = sp.affinity.rotate(multpol, angle, use_radians=True)

    if plot:
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        shapely_plt.plot_polygon(multpol, ax=ax[0])
        shapely_plt.plot_polygon(bound_rect, ax=ax[0])

        shapely_plt.plot_polygon(rotated_bound_rect, ax=ax[1])
        shapely_plt.plot_polygon(rotated_multpol, ax=ax[1])

        plt.show()

    return list(rotated_multpol.geoms)
