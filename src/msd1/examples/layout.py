import polars as pl
from replan2eplus.zones.interfaces import Room
from svg2plan.identify.id_problems import report_problems

from msd1.examples.layout_utils import adjust_domains_and_plot
from msd1.examples.rotation import rotate_areas_in_unit
from msd1.examples.utils import (
    from_svdomain,
    get_svdomains_from_rooms,
)
from msd1.geometry import RoomData
from msd1.main import MSDSchema


def get_room_data_from_unit(unit_df: pl.DataFrame):
    df = MSDSchema.validate(unit_df)
    rotated_polygons = rotate_areas_in_unit(
        df
    )  # only rotation transformation applied here # TODO -> be more explicit!
    rooms = [
        RoomData(
            row["entity_type"], row["entity_subtype"], row["height"], ix, poly
        ).room
        for ix, (row, poly) in enumerate(
            zip(df.iter_rows(named=True), rotated_polygons)
        )
    ]
    return rooms


def adjust_layout_and_update_room_domains(rooms: list[Room]):
    _, domains_dict = get_svdomains_from_rooms(rooms)
    layout = adjust_domains_and_plot(domains_dict)
    problems = report_problems(layout)
    assert len(problems) == 0

    sorted_rooms = sorted(rooms, key=lambda x: x.name)
    sorted_svdomains = sorted(layout.domains.values(), key=lambda x: x.name)

    for room, sv_domain in zip(sorted_rooms, sorted_svdomains):
        assert room.name == sv_domain.name
        room.domain = from_svdomain(sv_domain)

    return rooms
