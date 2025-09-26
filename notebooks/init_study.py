import marimo

__generated_with = "0.16.2"
app = marimo.App(width="medium")


@app.cell
def _():
    from msd.main import access_dataset, sample_dataset,get_sample_dataset_with_rectangular_units
    import polars as pl 
    import shapely as sh
    import math 
    return (get_sample_dataset_with_rectangular_units,)


@app.cell
def _(get_sample_dataset_with_rectangular_units):
    kf = get_sample_dataset_with_rectangular_units()
    kf
    return


if __name__ == "__main__":
    app.run()
