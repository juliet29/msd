from pathlib import Path
from rich import print
from msd1.examples.layout import get_room_data_from_unit
from msd1.examples.layout import (
    adjust_layout_and_update_room_domains,
)
from msd1.case import create_case_for_unit

from msd1.examples.utils import read_unit_data
from msd1.paths import TEST_MODEL_PATH, PATH_TO_IDD, PATH_TO_WEATHER_FILE

from replan2eplus.visuals.base_plot import BasePlot
from replan2eplus.visuals.data_plot import DataPlot, temperature_colorbar
from replan2eplus.ezcase.read import ExistCase
from replan2eplus.results.sql import create_result_for_qoi, get_sql_results
from replan2eplus.idfobjects.variables import OutputVariables


def create_example_case(run=False):
    df = read_unit_data()
    rooms0 = get_room_data_from_unit(df)
    rooms = adjust_layout_and_update_room_domains(rooms0)
    case = create_case_for_unit(rooms)
    if run:
        case.save_and_run_case(TEST_MODEL_PATH)
    return case


def read_case(path_to_case: Path):
    return ExistCase(PATH_TO_IDD, path_to_case / "out.idf", PATH_TO_WEATHER_FILE)


def plot_base_case(case: ExistCase):
    bp = (
        BasePlot(case.zones, cardinal_expansion_factor=1.8)
        .plot_zones()
        .plot_zone_names()
        .plot_cardinal_names()
    )
    bp.show()


def get_qoi(qoi: OutputVariables, path: Path):
    sql = get_sql_results(path)
    return create_result_for_qoi(sql, qoi)


def plot_temperature_on_zones_at_time(case: ExistCase, hour: int = 12):
    qoi = get_qoi("Zone Mean Air Temperature", case.folder_path)

    data_at_noon = qoi.select_time(hour)

    dp = DataPlot(case.zones)
    dp.plot_zones_with_data(data_at_noon, temperature_colorbar)
    dp.plot_zone_names()
    dp.plot_cardinal_names()
    dp.show()


if __name__ == "__main__":
    case = read_case(TEST_MODEL_PATH)
    plot_temperature_on_zones_at_time(case)
    # TODO -> should assert that the problems are 0..
    # df = read_unit_data()
    # rooms = get_room_data_from_unit(df)
    # pickle_unit_rooms(rooms)
    # res = get_areas_for_unit() # TODO pickle this.. / save as csv
    # print(res)

    # p1.show(renderer="browser")
