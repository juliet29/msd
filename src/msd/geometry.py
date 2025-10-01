import numpy as np
import shapely as sp
from replan2eplus.geometry.domain import Domain
from replan2eplus.geometry.range import Range
from replan2eplus.zones.interfaces import Room
from typing import NamedTuple
import math


def is_rectangle(geom: str):
    try:
        poly = sp.from_wkt(geom)
    except:
        print("bad wkt")
        return False

    try:
        assert poly.is_valid, "Invalid polygon"
    except:
        return False

    if poly.area == 0:
        print("Polygon area is 0")
        return False

    try:
        min_rotated_rect = poly.minimum_rotated_rectangle
    except:
        print("could not get rotated rect for this poly ")
        return False

    min_rotated_rect_area = min_rotated_rect.area
    true_area = poly.area
    if min_rotated_rect_area == 0 or true_area == 0:
        print("one of the areas is 0")
        return False

    try:
        if math.isclose(min_rotated_rect_area, true_area):
            return True
    except:
        print("Could not get close")
        return False

    return False


def angle_between_vectors(v1: np.ndarray, v2: np.ndarray):
    dot_product = np.dot(v1, v2)
    magnitude_v1 = np.linalg.norm(v1)
    magnitude_v2 = np.linalg.norm(v2)

    # Handle cases where one or both vectors are zero vectors to avoid division by zero
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0  # Or raise an error, depending on desired behavior

    cosine_theta = dot_product / (magnitude_v1 * magnitude_v2)

    # Ensure cosine_theta is within [-1, 1] to prevent issues with arccos due to floating point inaccuracies
    cosine_theta = np.clip(cosine_theta, -1.0, 1.0)

    angle_radians = np.arccos(cosine_theta)
    return angle_radians


def get_line_between_point_and_line(line: sp.LineString, pt: sp.Point):
    dist_along = line.project(pt)
    ptb = line.line_interpolate_point(dist_along)
    return sp.LineString([pt, ptb])


def translate_line_to_origin(line: sp.LineString, pt: sp.Point):
    assert pt.touches(line)
    return sp.affinity.translate(line, xoff=-1 * pt.x, yoff=-1 * pt.y)


def get_rotation_angle(poly: sp.Polygon):
    # TOD check is rectangular
    coords = list(poly.exterior.normalize().coords)
    right_line = sp.LineString(coords[2:4])
    centroid = poly.centroid
    assert right_line.centroid.x > centroid.x

    vector_line = get_line_between_point_and_line(right_line, centroid)
    translated_line = translate_line_to_origin(vector_line, centroid)
    non_zero_pt = list(translated_line.coords)[1]
    v1 = np.array(non_zero_pt)
    e0 = np.array([1, 0])

    return angle_between_vectors(e0, v1)
    # return sp.affinity.rotate(poly, angle, use_radians=True).wkt


def rotate_multipolygon(multpol: sp.MultiPolygon):
    bound_rect: sp.Polygon = multpol.minimum_rotated_rectangle.normalize()  # type: ignore
    angle = get_rotation_angle(bound_rect)
    print(f"angle: {angle}")
    return angle


def rotate_rectangular_polygon(poly_: sp.Polygon | str):
    if isinstance(poly_, str):
        poly = sp.from_wkt(poly_)
    else:
        poly = poly_
    assert isinstance(poly, sp.Polygon)
    # TOD check is rectangular
    coords = list(poly.exterior.normalize().coords)
    right_line = sp.LineString(coords[2:4])
    centroid = poly.centroid
    assert right_line.centroid.x > centroid.x

    vector_line = get_line_between_point_and_line(right_line, centroid)
    translated_line = translate_line_to_origin(vector_line, centroid)
    non_zero_pt = list(translated_line.coords)[1]
    v1 = np.array(non_zero_pt)
    e0 = np.array([1, 0])

    angle = angle_between_vectors(
        e0, v1
    )  # TODO this is important for the environmental analysis... => should be put into E+
    return sp.affinity.rotate(poly, angle, use_radians=True).wkt


class ShapelyBounds(NamedTuple):
    minx: float
    miny: float
    maxx: float
    maxy: float

    @property
    def domain(self):
        horz_range = Range(self.minx, self.maxx)
        vert_range = Range(self.miny, self.maxy)
        return Domain(horz_range, vert_range)


class RoomData(NamedTuple):
    entity_type: str
    entity_subtype: str
    height: int
    id: int
    poly: sp.Polygon

    def __post_init__(self):
        assert self.entity_type == "area"

    @property
    def name(self):
        return f"{self.entity_subtype.lower()}_{self.id}"  # TODO do the names have to be independent? -> maybe have also a type?

    @property
    def domain(self):
        # TODO assert is a rectangle!
        return ShapelyBounds(*self.poly.bounds).domain

    @property
    def room(self):
        return Room(self.id, self.name, self.domain, self.height)

    # TODO -> should check that all the heights are the same..
