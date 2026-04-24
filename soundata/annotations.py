"""soundata annotation data types"""

import numpy as np

#: Time units
TIME_UNITS = {"seconds": "seconds", "milliseconds": "milliseconds"}

#: Label units
LABEL_UNITS = {"open": "no strict schema or units"}

#: Azimuth units
AZIMUTH_UNITS = {
    "radians": "values in the interval [-2*pi, 2*pi]",
    "degrees": "values in the interval [-360, 360]",
}

#: Distance units
DISTANCE_UNITS = {
    "meters": "meters",
    "centimeters": "centimeters",
    "millimeters": "millimeters",
}


class Annotation(object):
    """Annotation base class"""

    def __repr__(self):
        raise NotImplementedError


class Tags(Annotation):
    """Tags class

    Attributes:
        labels (list): list of string tags
        confidence (np.ndarray or None): array of confidence values, float in [0, 1]
        labels_unit (str): labels unit, one of LABELS_UNITS
    """

    def __init__(self, labels, labels_unit, confidence=None) -> None:
        raise NotImplementedError


class Events(Annotation):
    """Events class

    Attributes:
        intervals (np.ndarray): (n x 2) array of intervals
            (as floats) in seconds in the form [start_time, end_time]
            with positive time stamps and end_time >= start_time.
        labels (list): list of event labels (as strings)
        confidence (np.ndarray or None): array of confidence values, float in [0, 1]
        labels_unit (str): labels unit, one of LABELS_UNITS
        intervals_unit (str): intervals unit, one of TIME_UNITS
        azimuth (np.ndarray or None): list of size n with np.ndarrays with dtype float,
            indicating the azimuth of the sound event. Values between -360 and 360 for degrees
            and between -2*pi, 2*pi for radians or None.
        azimuth_unit (str): azimuth unit, one of AZIMUTH_UNITS
        elevation (np.ndarray or None): list of size n with np.ndarrays with dtype float,
            indicating the elevation of the sound event. Values between -90 and 90 or None.
        elevation_unit (str): elevation unit, one of AZIMUTH_UNITS
        distance (np.ndarray or None):list of size n with np.ndarrays with dtype float,
            indicating the distance of the sound event. Values must be positive or None.
        distance_unit (str): distance unit, one of DISTANCE_UNITS
        cartesian_coord (np.ndarray or None):
        cartesian_coord_unit (str): cartesian_coord unit, one of DISTANCE_UNITS


    """

    def __init__(
        self,
        intervals,
        intervals_unit,
        labels,
        labels_unit,
        confidence=None,
        azimuth=None,
        azimuth_unit=None,
        elevation=None,
        elevation_unit=None,
        distance=None,
        distance_unit=None,
        cartesian_coord=None,
        cartesian_coord_unit=None,
    ) -> None:
        raise NotImplementedError


#: position units
ELEVATIONS_UNITS = {
    "degrees": "degrees",
}
AZIMUTHS_UNITS = {
    "degrees": "degrees",
}
DISTANCES_UNITS = {
    "meters": "meters",
}

#: Time units
TIME_UNITS = {
    "seconds": "seconds",
    "milliseconds": "milliseconds",
}

#: Label units
LABEL_UNITS = {"open": "no strict schema or units"}


class SpatialEvents:
    """SpatialEvents class

    Attributes:
        intervals (list): list of size n np.ndarrays of shape (m, 2), with intervals
            (as floats) in TIME_UNITS in the form [start_time, end_time]
            with positive time stamps and end_time >= start_time.
            n is the number of sound events.
            m is the number of sounding instances for each sound event.
        intervals_unit (str): intervals unit, one of TIME_UNITS
        time_step (int, float, or None): the time-step between events
            over time in intervals_unit
        elevations (list): list of size n with np.ndarrays with dtype int,
            indicating the elevation of the sound event per time_step if moving
            or a single value if static. Values between -90 and 90
        elevations_unit (str): elevations unit, one of ELEVATIONS_UNITS
        azimuths (list): list of size n with np.ndarrays with dtype int,
            indicating the azimuth of the sound event per time_step if moving
            or a single value if static. Values between -180 and 180
        azimuths_unit (str): azimuths unit, one of AZIMUTHS_UNITS
        distances (list): list of size n with np.ndarrays with dtype int,
            indicating the distance of the sound event per time_step if moving
            or a single value if static. Values must be positive or None
        distances_unit (str): distances unit, one of DISTANCES_UNITS
        labels (list): list of event labels (as strings)
        labels_unit (str): labels unit, one of LABELS_UNITS
        clip_number_indices (list): list of clip number indices (as strings)
        confidence (np.ndarray or None): array of confidence values, float in [0, 1]
    """

    def __init__(
        self,
        intervals,
        intervals_unit,
        elevations,
        elevations_unit,
        azimuths,
        azimuths_unit,
        distances,
        distances_unit,
        labels,
        labels_unit,
        clip_number_index=None,
        time_step=None,
        confidence=None,
    ):
        raise NotImplementedError


def validate_time_steps(time_step, locations, interval):
    """Validate if timesteps are well-formed.

    If locations is None, validation passes automatically

    Args:
        time_step (float): spacing between location steps
        locations (np.ndarray): (n x 3) array
        interval (np.ndarray): (n x 2) expected start and end time
            for the locations
    Raises:
        ValueError: if the number of locations does not match
            the number of time_steps that fit in the interval
    """
    pass


def validate_locations(locations):
    """Validate if locations are well-formed.
    If locations is None, validation passes automatically
    Args:
        locations (np.ndarray): (n x 3) array
    Raises:
        ValueError: if locations have an invalid shape or
                have cartesian coordinate values outside the expected ranges.
    """
    pass


class MultiAnnotator(Annotation):
    """Multiple annotator class.
    This class should be used for datasets with multiple annotators (e.g. multiple annotators per clip).

    Attributes:
        annotators (list): list with annotator ids
        annotations (list): list of annotations (e.g. [annotations.Tags, annotations.Tags]
    """

    def __init__(self, annotators, annotations) -> None:
        raise NotImplementedError


def validate_array_like(
    array_like, expected_type, expected_dtype, check_child=False, none_allowed=False
):
    """Validate that array-like object is well formed

    If array_like is None, validation passes automatically.

    Args:
        array_like (array-like): object to validate
        expected_type (type): expected type, either list or np.ndarray
        expected_dtype (type): expected dtype
        check_child (bool): if True, checks if all elements of array are children of expected_dtype
        none_allowed (bool): if True, allows array to be None
    Raises:
        TypeError: if type/dtype does not match expected_type/expected_dtype
        ValueError: if array
    """
    pass


def validate_lengths_equal(array_list):
    """Validate that arrays in list are equal in length

    Some arrays may be None, and the validation for these are skipped.

    Args:
        array_list (list): list of array-like objects

    Raises:
        ValueError: if arrays are not equal in length

    """
    pass


def validate_confidence(confidence):
    """Validate if confidence is well-formed.

    If confidence is None, validation passes automatically

    Args:
        confidence (np.ndarray): an array of confidence values

    Raises:
        ValueError: if confidence are not between 0 and 1

    """
    pass


def validate_times(times):
    """Validate if times are well-formed.

    If times is None, validation passes automatically

    Args:
        times (np.ndarray): an array of time stamps

    Raises:
        ValueError: if times have negative values or are non-increasing

    """
    pass


def validate_intervals(intervals):
    """Validate if intervals are well-formed.

    If intervals is None, validation passes automatically

    Args:
        intervals (np.ndarray): (n x 2) array

    Raises:
        ValueError: if intervals have an invalid shape, have negative values
        or if end times are smaller than start times.

    """
    pass


def validate_unit(unit, unit_values, allow_none=False):
    """Validate that the given unit is one of the allowed unit values.

    Args:
        unit (str): the unit name
        unit_values (dict): dictionary of possible unit values
        allow_none (bool): if true, allows unit=None to pass validation
    Raises:
        ValueError: If the given unit is not one of the allowed unit values
    """
    pass


def validate_azimuth(azimuth, azimuth_unit=None, allow_none=False):
    pass


def validate_elevation(elevation, elevation_unit=None, allow_none=False):
    pass


def validate_distance(distance, allow_none=False):
    pass


def validate_cartesian_coord(cartesian_coord, allow_none=False):
    # print(np.shape(cartesian_coord))
    pass
