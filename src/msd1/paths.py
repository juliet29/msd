from pathlib import Path
from utils4plans.paths import StaticPaths
import pyprojroot

STATIC_PATH = Path(
    "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/fpopt/replan2eplus/static/_01_inputs"
)

PATH_TO_WINDOW_GAS_IDF = STATIC_PATH / "constructions/WindowGasMaterials.idf"
PATH_TO_WINDOW_GLASS_IDF = STATIC_PATH / "constructions/WindowGlassMaterials.idf"
PATH_TO_MAT_AND_CONST_IDF = STATIC_PATH / "constructions/ASHRAE_2005_HOF_Materials.idf"

material_idfs = [
    PATH_TO_MAT_AND_CONST_IDF,
    PATH_TO_WINDOW_GLASS_IDF,
    PATH_TO_WINDOW_GAS_IDF,
]
PATH_TO_WINDOW_CONST_IDF = STATIC_PATH / "constructions/WindowConstructs.idf"
PATH_TO_WEATHER_FILE = STATIC_PATH / "weather/PALO_ALTO/CA_PALO-ALTO-AP_724937_23.EPW"
PATH_TO_MINIMAL_IDF = STATIC_PATH / "base/01example/Minimal_AP.idf"


# external paths -> TODO put this in a config file??
ENERGY_PLUS_LOCATION = Path.home().parent.parent / "Applications/EnergyPlus-22-2-0"
PATH_TO_IDD = ENERGY_PLUS_LOCATION / "Energy+.idd"

BASE_PATH = pyprojroot.find_root(pyprojroot.has_dir(".git"))
static_paths = StaticPaths("", BASE_PATH)  # TODO can extend static paths if like..



THROWAWAY_PATH  = static_paths.models / "throwaway"

TEST_CASE = "msd_48475"
TEST_CASE_PATH = static_paths.plans / TEST_CASE
TEST_MODEL_PATH = static_paths.models / TEST_CASE
