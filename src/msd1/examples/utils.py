import polars as pl
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range
from replan2eplus.zones.interfaces import Room
from svg2plan.domains.domain import Domain as SVDomain
from svg2plan.domains.range import Range as SVRange
from svg2plan.helpers.layout import DomainsDict
from utils4plans.io import read_pickle, write_pickle

from msd1.main import access_dataset
from msd1.paths import TEST_CASE_PATH

UNIT_ID = 48475


def get_areas_for_unit(unit_id=UNIT_ID):
    return (
        access_dataset().filter(
            (pl.col("unit_id") == unit_id) & (pl.col("entity_type") == "area")
        )
    ).collect()


def save_unit_data():
    df = get_areas_for_unit()
    df.write_csv(TEST_CASE_PATH / "data.csv")


def read_unit_data():
    return pl.read_csv(TEST_CASE_PATH / "data.csv")


def pickle_unit_rooms(rooms: list[Room]):
    write_pickle(rooms, TEST_CASE_PATH, "rooms", OVERWRITE=True)


def read_unit_rooms():
    return read_pickle(TEST_CASE_PATH, "rooms")


def to_svrange(range: Range) -> SVRange:
    return SVRange.create_range(range.min, range.max)


def to_svdomain(domain: Domain, name: str):
    return SVDomain(
        to_svrange(domain.horz_range), to_svrange(domain.vert_range), name=name
    )


def from_svdomain(domain: SVDomain) -> Domain:
    return Domain(
        Range(float(domain.x.min), float(domain.x.max)),
        Range(float(domain.y.min), float(domain.y.max)),
    )


def get_svdomains_from_rooms(rooms: list[Room]):
    domains = [to_svdomain(i.domain, i.name) for i in rooms]
    domains_dict = {i.name: i for i in domains}
    return domains, domains_dict
