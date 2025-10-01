from replan2eplus.examples.mat_and_const import SAMPLE_CONSTRUCTION_SET
from replan2eplus.ezcase.main import EZCase
from replan2eplus.idfobjects.variables import default_variables
from msd.geometry import RoomData, rotate_rectangular_polygon
from replan2eplus.zones.interfaces import Room


from msd.paths import (
    PATH_TO_IDD,
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_MINIMAL_IDF,
    PATH_TO_WEATHER_FILE,
    PATH_TO_WINDOW_CONST_IDF,
    material_idfs,
)



def create_case_for_unit(rooms: list[Room]):
    case = EZCase(PATH_TO_IDD, PATH_TO_MINIMAL_IDF, PATH_TO_WEATHER_FILE)
    case.initialize_idf()
    case.add_zones(rooms)

    case.add_constructions_from_other_idf(
        [PATH_TO_WINDOW_CONST_IDF, PATH_TO_MAT_AND_CONST_IDF],
        material_idfs,
        SAMPLE_CONSTRUCTION_SET,
    )
    # case.add_airflownetwork()
    case.idf.add_output_variables(default_variables)
    return case


if __name__ == "__main__":
    pass
