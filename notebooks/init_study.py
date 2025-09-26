import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():

    import numpy as np
    from msd.main import filter_to_rect_units
    from msd.case import add_rotated_geom_column
    import polars as pl 
    import shapely 
    import math 
    from shapely import plotting
    return filter_to_rect_units, plotting, shapely


@app.cell
def _(filter_to_rect_units):
    rp = filter_to_rect_units().collect()
    rp
    return (rp,)


@app.cell
def _(rp, shapely):
    gdict = {}
    for name, data in rp.sort("unit_id").group_by("unit_id"):
        polys = shapely.MultiPolygon([shapely.from_wkt(geom) for geom in data["geom"]])
        n = str(int(name[0]))
        gdict[n] = polys

    gdict
    return (gdict,)


@app.cell
def _(gdict, plotting):
    plotting.plot_polygon(gdict["11883"])
    return


@app.cell
def _(gdict, plotting):
    plotting.plot_polygon(gdict["147600"])
    return


@app.cell
def _(gdict, plotting):
    plotting.plot_polygon(gdict["148501"])
    return


if __name__ == "__main__":
    app.run()
