import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from msd.main import access_dataset, sample_dataset,get_sample_dataset_with_rectangular_units
    import polars as pl 
    import shapely 
    import math 
    return get_sample_dataset_with_rectangular_units, pl, shapely


@app.cell
def _(get_sample_dataset_with_rectangular_units):
    kf = get_sample_dataset_with_rectangular_units()
    kf
    return (kf,)


@app.cell
def _():
 
    return


@app.cell
def _(kf, pl, shapely):
    plans = []
    plan_lists = []
    names = []
    for name, data in kf.sort(by="unit_id").group_by("unit_id"):
        data = data.filter((pl.col("entity_type")== "area") & (pl.col("entity_subtype")!= "BALCONY") )
        geom_list = data["geom"].to_list()
        polys = [shapely.from_wkt(i) for i in geom_list]
        res = shapely.MultiPolygon(polys)
        plans.append(res)
        plan_lists.append(polys)
        names.append(name)
    
    
    return names, plan_lists, plans


@app.cell
def _(names):
    print(names)
    return


@app.cell
def _(plan_lists):
    plan_lists[0]
    return


@app.cell
def _(plans):
    plan = plans[0]
    plan
    return (plan,)


@app.cell
def _(plan, shapely):
    union = shapely.unary_union(plan)
    union
    return


@app.cell
def _():
    return


@app.cell
def _(plans):
    plans[1]
    return


@app.cell
def _(plans):
    plans[2]
    return


@app.cell
def _(plans):
    plans[11]
    return


if __name__ == "__main__":
    app.run()
