import math
import json


def haversine(lat1, lon1, lat2, lon2):
    """
    Haversine Formula - Distance between two GPS points)
    :param lat1: latitude of the 1st point
    :param lon1: longitude of the 2nd point
    :param lat2: latitudes of the 2nd point
    :param lon2: longitude of the 2nd point
    :return: distance between latitudes and longitudes in kilometers
    """
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0

    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


def highest_plane(vectors):
    """
    Finds the highest flying plane based on the 'geo_altitude'
    :param vectors: list of dictionaries (flight vectors of planes)
    :return: dictionary containing the largest 'geo_altitude
    """
    high_fly = vectors[0] # store the first set of data into the variable high_fly
    for plane in vectors:
        if plane ['geo_altitude'] > high_fly['geo_altitude'] : #checks to see if the next plane's
                                                               #altitude is greater than the first plane.
            high_fly = plane # update 'high_fly' varible if 'plane' has a higher altitude.
    return high_fly


def lowest_plane(vectors):
    """
    Finds the lowest flying plane based on the 'geo_altitude'
    :param vectors: list of dictionaries (flight vectors of planes)
    :return: dictionary containing the smallest 'geo_altitude
    """
    
    low_fly = vectors[0] # store the first set of data into the variable high_fly
    for plane in vectors: 
        if plane ['geo_altitude'] < low_fly['geo_altitude'] : #checks to see if the next plane's  
                                                              #altitude is less than the 'low_fly'.
            low_fly = plane # update 'low_fly' varible if 'plane' has a lower altitude.
    return low_fly


def fastest_climber(vectors):
    fastest = vectors[0] # store the first set of data into the variable 'fastest'
    for plane in vectors:
        if plane ['vertical_rate'] > fastest['vertical_rate'] : #checks to see if the next plane's vertical
                                                                #rate is higher than the current fastest plane.
            fastest = plane # update 'fastest' varible if 'plane' has a higher 'vertical_rate'.
    return fastest


def fastest_descender(vectors):
    decend = vectors[0] # store the first set of data into the variable 'decend'
    for plane in vectors:
        if plane ['vertical_rate'] < decend['vertical_rate']: #checks to see if the next plane's vertical
                                                              #rate is lower than the current plane.
            decend = plane # update 'decend' varible if 'plane' has a lower 'vertical_rate'
    return decend


def closest_to_ERAU(vectors):
    """
    Finds the plane closest to the ERAU campus in Prescott
    :param vectors: list of dictionaries (flight vectors of planes)
    :return: a tuple containing the closest plane and the distance to ERAU
    """
    
    ERAU_lat = 34.61449 #collected ERAU data online.
    ERAU_lon = -112.44597 #collected ERAU data online.
    
    cp  = vectors[0] # store the first set of data into the variable 'cp'
    
    #calculate the distance from ERAU to the first plane using the haversine() function
    #and store that value as the min_distance. 
    min_distance = haversine(ERAU_lat, ERAU_lon, cp['latitude'], cp['longitude']) 
    for plane in vectors:
        #checks to see if the next plane's distance from ERAU is lower than the current plane.
        if min_distance > haversine(ERAU_lat, ERAU_lon, plane['latitude'], plane['longitude']):
            #update 'min_distance' varible if 'plane' has a lower distance from ERAU. 
            min_distance = haversine(ERAU_lat, ERAU_lon, plane['latitude'], plane['longitude'])
            #update 'cp' varible of 'plane' so that it is corresponding with 'min_distance' variable.
            cp = plane 
    return cp, round(min_distance) 


with open('./vectors.json', 'r') as fh:
    vectors = json.load(fh)

print("Flight Vector Analysis:")

lowest = lowest_plane(vectors)
print(f"Lowest flying plane: {lowest['callsign']} at {lowest['geo_altitude']} meters")

highest = highest_plane(vectors)
print(f"Highest flying plane: {highest['callsign']} at {highest['geo_altitude']} meters")

fastest = fastest_descender(vectors)
print(f"Highest flying plane: {fastest['callsign']} at {fastest['vertical_rate']} meters")

climber = fastest_climber(vectors)
print(f"Faster descender is {climber['callsign']} at a rate of {climber['vertical_rate']} meters")

closest = closest_to_ERAU(vectors)
print(f"Closest to ERAU is {closest[0]['callsign']} about {closest[1]} meters away")
