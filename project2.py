"""
    Find interesting information in real time flight vectors
    using Python 3.8.x or later
"""
# todo add author
import json
from itertools import combinations
from p2_utils import haversine, get_bounding_box, get_vectors, get_details, aircraft_info, ERAU_Latitude, ERAU_Longitude
import requests  # 3rd party requests module https://docs.python-requests.org/en/latest/


def get_my_geo() -> (float, float):
    """
    Finds the current geo location based on your IP address, using https://ipinfo.io/loc
    In case of a network error or unavailability of the service, an error is shown and embry's lat and lon are returned
    :return: tuple with the current Latitude Longitude, or embry's lat and lon, if the network or api is unavailable.
    """
    # todo ... fetching and returning my geo from https://ipinfo.io/loc
    resp = requests.get('https://ipinfo.io/loc')
    try:
        if resp.status_code == 200:
            s = resp.status_code
        else:
            s = {}
            resp.close()
    except (Exception, IOError) as ioe:
        print("Please note, there were problems calling the open-sky-network api" + str(ioe))
    return s


def cleanup(airplanes: [dict]) -> [dict]:
    """
    Cleaning up the list of dictionaries, keeping only the needed key/value pairs in the dictionaries.
    Only the following seven attributes are needed:
    "icao24", "callsign", "longitude", "latitude", "velocity", "vertical_rate", "geo_altitude"
    Secondly, any plane that has a None value for any of those seven keys is filtered out.
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: cleaned up list of dicts
    """
    lst = ["icao24", "callsign", "longitude", "latitude", "velocity", "vertical_rate", "geo_altitude"]
    # todo: remove unnecessary key value pairs
    clean_lst = list(map(lambda d: {k: d[k] for k in lst},airplanes))
    # todo: remove planes that have None value(s) for unnecessary keys.
    super_clean_lst = list(filter(lambda d:None not in d.values(), clean_lst ))
    return super_clean_lst


def enhance(airplanes: [dict]) -> [dict]:
    """
    Using the aircraft_info() function from p2_utils, this function adds important information, if available,
    about a plane into each dictionary of the given list of dicts.
    For each plane, the following three attributes are added: "Manufacturer", "Type", "RegisteredOwners"
    Should this information be unavailable, "unknown" is inserted as a value for all three keys.
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: list of airplanes with 3 additional key/value pairs
    """
    default = {"Manufacturer": "unknown", "Type": "unknown", "RegisteredOwners": "unknown"}
    add_key = ["Manufacturer", "Type", "RegisteredOwners"]
    # todo: add new Key/Value pairs into each dictionary

    for p in airplanes:
        add_info = aircraft_info(p['icao24'])
        if add_info != None and add_info != {}:
            add_info = {x: add_info[x] for x in add_key}
            p.update(add_info)
        else:
            p.update(default)

    return airplanes


def customize(lat: float, lon: float, airplanes: [dict]) -> [dict]:
    """
    Adds its center from "my geo location", the center of the bounding box to each dictionary.
    For each plane, its current distance to the given center geo location, i.e. approx. distance "my geo location",
    is inserted as a value for the key "center_distance".
    :param lat: latitude of the center of the bounding box
    :param lon: longitude of the center of the bounding box
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: list of airplanes with one additional key/value pairs
    """
    # todo: add center_distance into each dictionary

    return airplanes


def highest_plane(airplanes: [dict]) -> dict:
    """
    Finds the highest flying plane based on the 'geo_altitude'
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: the highest flying airplane
    """
    # todo: find add return the highest flying plane
    return max(airplanes, key = lambda d: d['geo_altitude'])


def lowest_plane(airplanes: [dict]) -> dict:
    """
    Finds the lowest flying plane based on the 'geo_altitude'
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: the lowest flying airplane
    """
    # todo: find add return the lowest flying plane
    return min(airplanes, key = lambda d: d['geo_altitude'])


def fastest_climber(airplanes: [dict]) -> dict:
    """
    Finds the fastest climbing plane based on the 'vertical_rate'
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: the lowest flying airplane
    """
    # todo: find add return the fastest climbing plane
    return max(airplanes, key = lambda d: d['vertical_rate'])


def fastest_descender(airplanes: [dict]) -> dict:
    """
       Finds the fastest descending plane based on the 'vertical_rate'
       :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
       :return: the lowest flying airplane
       """
    # todo: find add return the fastest descending plane
    return min(airplanes, key = lambda d: d['vertical_rate'])


def dump_raw(airplanes: [dict]) -> None:
    """
    Utility function to save the current value of the airplanes, i.e., list of dicts to the 'raw.json' file
    in the current work directory.
    :param airplanes: list of dicts, each dict has the coordinates, speed, etc of a plane
    :return: None
    """
    # todo: writes the given dict as json file to disk


user_name = "teashas"  # opensky username   # todo: use your opensky username
password = "boeing777"  # opensky password  # todo: use your opensky password
radius = 100  # radius around current center geo location
my_pos = get_my_geo()  # current geo location
bounding_box = get_bounding_box(my_pos[0], my_pos[1], radius)  # box around circle(radius) around current location
vectors = get_vectors(bounding_box, user_name, password)  # list of planes currently flying in the box
# dump_raw(vectors)  # save origin to raw.json for manual observation

if vectors is None or 0 == len(vectors):
    my_pos = (ERAU_Latitude, ERAU_Longitude)
    try:
        with open("vectors.json") as fh:
            vectors = json.load(fh)
    except IOError as ioe:
        print("Sorry, something went terribly wrong, " + str(ioe))
        exit(1)

vectors = customize(my_pos[0], my_pos[1], enhance(cleanup(vectors)))  # removes unnecessary and adds useful attributes
# dump_raw(vectors)  # save origin to raw.json for manual observation

print(f"A real time fight vector analysis for the {radius} km area around me found {len(vectors)} planes:")

x = lowest_plane(vectors)
print(f"Lowest plane, {get_details(x)} at {x.get('geo_altitude')} meters")

x = highest_plane(vectors)
print(f"Highest plane, {get_details(x)} at {x.get('geo_altitude')} meters")

x = fastest_descender(vectors)
print(f"Faster descender, {get_details(x)} at a rate of {x.get('vertical_rate')} meters per second")

x = fastest_climber(vectors)
print(f"Faster climber, {get_details(x)} at a rate of {x.get('vertical_rate')} meters per second")

