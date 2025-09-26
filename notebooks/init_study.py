import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from msd.main import get_sample_unit
    from msd.angle_between import angle_between_vectors, rotate_rectangular_polygon
    import numpy as np
    import polars as pl 
    import shapely 
    import math 
    return (
        angle_between_vectors,
        get_sample_unit,
        np,
        rotate_rectangular_polygon,
        shapely,
    )


@app.cell
def _(get_sample_unit):
    df = get_sample_unit().collect() 
    df
    return (df,)


@app.cell
def _(df, rotate_rectangular_polygon, shapely):
    geom2 = df[3]["geom"][0]
    poly2 = shapely.from_wkt(geom2)
    rotate_rectangular_polygon(poly2)
    return


@app.cell
def _(df, shapely):
    geom = df[0]["geom"][0]
    poly = shapely.from_wkt(geom)
    poly
    return (poly,)


@app.cell
def _(poly, shapely):
    shapely.affinity.rotate(poly, 45)
    return


@app.cell
def _(poly):
    list(poly.exterior.coords)
    return


@app.cell
def _(poly, shapely):
    coords = list(poly.normalize().exterior.coords)
    right_line = shapely.LineString(coords[2:4])
    centroid = poly.centroid
    return centroid, right_line


@app.cell
def _(centroid, right_line):
    right_line.centroid.x > centroid.x
    return


@app.cell
def _(centroid, right_line, shapely):
    shapely.GeometryCollection([right_line, centroid]) # TODO -> some assertions.. 
    return


@app.cell
def _(centroid, right_line):
    dist_along = right_line.project(centroid)
    dist_along
    return (dist_along,)


@app.cell
def _(centroid, dist_along, right_line, shapely):
    ptb = right_line.line_interpolate_point(dist_along)
    vector_line = shapely.LineString([centroid, ptb])
    shapely.GeometryCollection([ptb, right_line, centroid, vector_line])

    return ptb, vector_line


@app.cell
def _(vector_line):
    print(vector_line)
    return


@app.cell
def _(centroid):
    centroid.x
    return


@app.cell
def _(centroid, shapely, vector_line):
    translated_line = shapely.affinity.translate(vector_line, xoff=-1*centroid.x, yoff=-1*centroid.y) # TODO assert that its 0,0
    print(translated_line)
    return (translated_line,)


@app.cell
def _(centroid, vector_line):
    centroid.touches(vector_line)
    return


@app.cell
def _(centroid, ptb, right_line, shapely, translated_line, vector_line):
    shapely.GeometryCollection([ptb, right_line, centroid, vector_line, translated_line])
    return


@app.cell
def _(angle_between_vectors, np, translated_line):
    non_zero_pt = list(translated_line.coords)[1]
    v1 = np.array(non_zero_pt)
    e0 = np.array([1,0])

    angle = angle_between_vectors(e0, v1)
    angle
    return (angle,)


@app.cell
def _(angle, poly, shapely):
    shapely.affinity.rotate(poly, angle, use_radians=True)
    return


if __name__ == "__main__":
    app.run()
