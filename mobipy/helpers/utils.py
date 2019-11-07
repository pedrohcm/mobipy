import geopy as gp
import pandas as pd
import numpy as np
import math
import operator
from sklearn.cluster import DBSCAN
from shapely.geometry import MultiPoint



def calculateDistance(lat1, lon1, lat2, lon2):
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)
    distance = gp(coords1, coords2).m
    return distance


def calculateMidPoint(dataframe, dataIdentifier):
    x = 0
    y = 0
    z = 0

    for row in dataframe.itertuples():
        latitude = getattr(row, dataIdentifier.latitude) * (math.pi / 180)
        longitude = getattr(row, dataIdentifier.longitude) * (math.pi / 180)

        x += math.cos(latitude) * math.cos(longitude)
        y += math.cos(latitude) * math.sin(longitude)
        z += math.sin(latitude)

    total = len(dataframe)

    x = x / total
    y = y / total
    z = z / total

    centralLongitude = math.atan2(y, x)
    centralSquareRoot = math.sqrt(x * x + y * y)
    centralLatitude = math.atan2(z, centralSquareRoot)

    midPointLat = centralLatitude * (180 / math.pi)
    midPointLon = centralLongitude * (180 / math.pi)

    midPoint = (midPointLat, midPointLon)

    return midPoint

def get_time_spent_in_minutes(timestamp_start_time, timestamp_end_time):
    return int(timestamp_end_time-timestamp_start_time) / 60

def get_blox_plot_info(data):
    df = pd.DataFrame(data) 
    quantiles = df.quantile([0.25,0.5,0.75])
    return quantiles

def cluster_points(points, max_radius, min_samples):
    kms_per_radian = 6371.0088
    epsilon = max_radius / kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=min_samples, algorithm='ball_tree', metric='haversine').fit(np.radians(points))
    cluster_labels = db.labels_
    print(cluster_labels)
    num_clusters = len(set(cluster_labels))
    clusters = pd.Series([points[cluster_labels == n] for n in range(num_clusters)])
    print('Number of clusters: {}'.format(num_clusters))
    print(clusters)
    return clusters

def get_np_coords_from_df(dataframe, data_identifier):
    coords = dataframe.as_matrix(columns=[data_identifier.lat_name, data_identifier.lon_name])
    return coords

def get_centermost_point(cluster):
    centroid = (MultiPoint(cluster).centroid.x, MultiPoint(cluster).centroid.y)
    centermost_point = min(cluster, key=lambda point: gp.distance.great_circle(point, centroid).m)
    return tuple(centermost_point)

def slice_geographic_data(dataframe, dataIdentifier, center_lat, center_lon, tolerance):
    min_lats,max_lats,min_lons,max_lons = get_search_boundaries(center_lat, center_lon, tolerance)
    return dataframe[(dataframe[dataIdentifier.lat_name] >= min_lats) & (dataframe[dataIdentifier.lat_name] <= max_lats) &
                (dataframe[dataIdentifier.lon_name] >= min_lons) & (dataframe[dataIdentifier.lon_name] <= max_lons)]

def get_search_boundaries(center_lat, center_lon, 
                          tolerance, threshold=1):
    upper_limit = tolerance + threshold
    lower_limit = tolerance - threshold
    min_lats,max_lats,min_lons,max_lons = get_lat_long_with_tolerance(center_lat, 
                                                                        center_lon, 
                                                                        tolerance, 
                                                                        upper_limit, 
                                                                        lower_limit,
                                                                        True)
    #distance = calculateDistance(min_lats, min_lons, center_lat, center_lon)
    return round(min_lats, 6),round(max_lats, 6),round(min_lons, 6),round(max_lons, 6)
    
def get_lat_long_with_tolerance(center_lat, center_lon, 
                                tolerance, 
                                upper_limit, lower_limit, adjust=False):
    km_per_degree = 111.32
    meter_degree = (1 / km_per_degree) / 1000
    coef = tolerance * meter_degree
    min_lats = center_lat - coef
    min_lons = center_lon - coef
    max_lats = center_lat + coef
    max_lons = center_lon + coef
    distance = calculateDistance(max_lats, max_lons, center_lat, center_lon)
    if(adjust == True):
        if(distance > upper_limit):
            new_tolerance = tolerance - ((distance - upper_limit) / 1.4)
            return get_lat_long_with_tolerance(center_lat, center_lon, 
                                           new_tolerance, 
                                           upper_limit, lower_limit) 
        if(distance < lower_limit):
            new_tolerance = tolerance + ((lower_limit - distance) / 1.4)
            return get_lat_long_with_tolerance(center_lat, center_lon, 
                                           new_tolerance, 
                                           upper_limit, lower_limit) 
    else:
        if(distance > upper_limit):
            return get_lat_long_with_tolerance(center_lat, center_lon, 
                                           tolerance - 1, 
                                           upper_limit, lower_limit) 
        if(distance < lower_limit):
            return get_lat_long_with_tolerance(center_lat, center_lon, 
                                           tolerance + 1, 
                                           upper_limit, lower_limit) 
    return min_lats, max_lats, min_lons, max_lons

def get_closest_items(dataframe, dataIdentifier, center_lat, center_lon, 
                distance_tolerance):
    distances = {}
    items_ids = []
    if(len(dataframe) > 0):
        for row in dataframe.itertuples():
            distances[getattr(row, dataIdentifier.item_id)] = calculateDistance(center_lat, center_lon, 
                         getattr(row, dataIdentifier.latitude), getattr(row, dataIdentifier.longitude))
        ordered_distances = sorted(distances.items(), key=operator.itemgetter(1))
        closest_distance = ordered_distances[0][1]
        for item, distance in distances.items():
            if(distance <= closest_distance + distance_tolerance):
                items_ids.append(item)    
    return items_ids