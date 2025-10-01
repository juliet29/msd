import kagglehub
from kagglehub import KaggleDatasetAdapter
import polars as pl
from msd.geometry import is_rectangle
from msd.rectangular_calc import rect_unit_ids
from msd.paths import (
    THROWAWAY_PATH,
)
import dataframely as dy
# TODO use patito to verify schema!
# Set the path to the file you'd like to load


class MSDSchema(dy.Schema):
    apartment_id = dy.String(nullable=False)
    site_id = dy.Int64(nullable=False)
    building_id = dy.Int64(nullable=False)
    plan_id = dy.Int64(nullable=False)
    floor_id = dy.Int64(nullable=False)
    unit_id = dy.Float64(nullable=False)
    area_id = dy.Float64(nullable=False)
    unit_usage = dy.String(nullable=False)
    entity_type = dy.String(nullable=False)
    entity_subtype = dy.String(nullable=False)
    geom = dy.String(nullable=False)
    elevation = dy.Float64(nullable=False)
    height = dy.Float64(nullable=False)
    zoning = dy.String(nullable=False)
    roomtype = dy.String(nullable=False)



def access_dataset() -> pl.LazyFrame:
    file_path = "mds_V2_5.372k.csv"

    # Load the latest version
    lf = kagglehub.dataset_load(
        KaggleDatasetAdapter.POLARS, "caspervanengelenburg/modified-swiss-dwellings",
        file_path,
    )

    return lf


def filter_to_areas(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.filter(pl.col("entity_type") == "area")


def filter_to_nonbalconies(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.filter(pl.col("entity_subtype") != "BALCONY")


def filter_to_units_with_more_than_one_area(lf: pl.LazyFrame) -> pl.LazyFrame:
    def get_unit_ids(lf: pl.LazyFrame) -> pl.Series:
        return (
            lf.pipe(filter_to_areas)  # break this out separetely..
            .group_by("unit_id")
            .agg(pl.col("geom").len().alias("num_of_area"))
            .filter(pl.col("num_of_area") > 1)
            .collect()
            .cast(pl.Int32)
            .to_series()
        )

    unit_ids = get_unit_ids(lf)
    return lf.filter(pl.col("unit_id").is_in(unit_ids))


def add_is_rectangle_column(lf: pl.LazyFrame) -> pl.LazyFrame:
    return lf.with_columns(
        pl.col("geom")
        .map_elements(is_rectangle, return_dtype=pl.Boolean)
        .alias("is_rectangle")
    )


def filter_to_units_where_all_geom_rectangular(lf: pl.LazyFrame) -> pl.LazyFrame:
    def get_unit_ids(lf: pl.LazyFrame) -> pl.Series:
        return (
            lf.pipe(add_is_rectangle_column)
            .group_by("unit_id")
            .agg(["is_rectangle"])
            .filter(pl.col("is_rectangle").list.all())
            .select("unit_id")
            .cast(pl.Int32)
            .collect()
            .to_series()
        )

    unit_ids = get_unit_ids(lf)
    print(f"Found {len(unit_ids)} units with all rectangular rooms")
    return lf.filter(pl.col("unit_id").is_in(unit_ids))


# SAMPLING


def sample_dataset():
    lf = access_dataset()
    return lf.filter(
        (pl.col("unit_usage") == "RESIDENTIAL")
        & (
            pl.col("unit_id").is_between(48000, 49000)
        )  # filter by areas that are not balconies -> may have better luck..
    )  # TODO remove collect here


def get_sample_dataset_with_rectangular_units():
    return (
        (
            sample_dataset()
            .pipe(filter_to_areas)
            .pipe(filter_to_units_where_all_geom_rectangular)
        )
        .collect()
        .head(1)
    )


def get_rectangular_units_excluding_balconies() -> pl.DataFrame:
    lf = access_dataset()
    return (
        lf.pipe(filter_to_units_with_more_than_one_area)
        .pipe(filter_to_nonbalconies)
        .pipe(filter_to_units_where_all_geom_rectangular)
        .unique(subset=["unit_id"])
        .collect()
    )


def compare():
    lf = access_dataset()
    possible_units = len(lf.pipe(filter_to_areas).unique(subset=["unit_id"]).collect())

    interesting_units = len(
        lf.pipe(filter_to_units_with_more_than_one_area)
        .unique(subset=["unit_id"])
        .collect()
    )

    rectangular_units = len(
        lf.pipe(filter_to_units_with_more_than_one_area)
        .pipe(filter_to_units_where_all_geom_rectangular)
        .unique(subset=["unit_id"])
        .collect()
    )

    rectangular_units_exclude_balconies = len(
        get_rectangular_units_excluding_balconies()
    )
    print(
        f"num possible units: {possible_units}. num interesting units: {
            interesting_units
        }. num  all_rect units: {rectangular_units}. num all_rect units no boundaries: {
            rectangular_units_exclude_balconies
        } "
    )


def filter_to_rect_units():
    lf = access_dataset()
    return lf.pipe(filter_to_areas).filter(pl.col("unit_id").is_in(rect_unit_ids))


# filter to where all rooms are rectangles..
# case.save_and_run_case(THROWAWAY_PATH)

if __name__ == "__main__":
    dd = get_rectangular_units_excluding_balconies()
    dd.select(pl.col("unit_id"))
