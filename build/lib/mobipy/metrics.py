import math
from . import utils
from .dataset_selector import dataset_selector, select_df
from .selector import Selector

@dataset_selector
def radius_of_gyration(dataframe, dataIdentifier, midPoint=None):
    """Measures how far a user moves from the mid point, in meters.

    If the argument `midPoint` isn't passed in, it will be calculated
    with the data from `dataframe`.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        the dataframe with the data
    dataIdentifier : DataIdentifier
        the identifier of the dataframe to be used
    midPoint : tuple, optional
        the mid point of the displacements, tuple (lat, lon)
    """
    sum = 0
    if midPoint is None:
        midPoint = utils.calculate_mid_point(dataframe, dataIdentifier)
        print(midPoint)
    for row in dataframe.itertuples():
        base = utils.calculate_distance(getattr(row, dataIdentifier.latitude), 
            getattr(row, dataIdentifier.longitude), midPoint[0], midPoint[1])
        sum += math.pow(base, 2)
    sum = math.sqrt(sum / len(dataframe))
    return sum

@dataset_selector
def user_displacement_distance(dataframe, dataIdentifier):
    sum_user_distances = 0
    latitude_a = longitude_a = latitude_b = longitude_b = 0
    for row in dataframe.itertuples():
        if latitude_a == 0:
            latitude_a = getattr(row, dataIdentifier.latitude)
            longitude_a = getattr(row, dataIdentifier.longitude)
        else:
            if latitude_b == 0:
                latitude_b = getattr(row, dataIdentifier.latitude)
                longitude_b = getattr(row, dataIdentifier.longitude)    
            sum_user_distances += utils.calculate_distance(latitude_a, longitude_a, latitude_b, longitude_b)
            latitude_a = longitude_a = latitude_b = longitude_b = 0
    return sum_user_distances

@dataset_selector
def group_by_closeness(dataframe_a, dataframe_b, dataIdentifier, b_distance_tolerance=1, search_tolerance=50):
    result_group = {}
    for row in dataframe_a.itertuples():
        center_lat = round(getattr(row, dataIdentifier.latitude), 6)
        center_lon = round(getattr(row, dataIdentifier.longitude), 6)
        a_id = getattr(row, dataIdentifier.item_id)
        sliced_group_b = utils.slice_geographic_data(dataframe_b, dataIdentifier, center_lat, 
                                               center_lon, search_tolerance)
        for b_item in utils.get_closest_items(sliced_group_b, dataIdentifier, center_lat, center_lon, b_distance_tolerance):
                time_spent_in_minutes = utils.get_time_spent_in_minutes(getattr(row, dataIdentifier.start_time), 
                                                                  getattr(row, dataIdentifier.end_time))
                if b_item in result_group:
                        result_group[b_item][1].append(time_spent_in_minutes)
                        result_group[b_item][2].append(a_id)
                else:
                        result_group[b_item] = [b_item, [time_spent_in_minutes], [a_id]]
        for b_item in result_group:
                result_group[b_item][1] = utils.get_blox_plot_info(result_group[b_item][1])
        return result_group

@dataset_selector
def activity_centers(dataframe, dataIdentifier):
    """Calculates the activity centers by applying the DBSCAn algorithm to the dataframe.

    Returns a list of activity centers, each with [lat, lon] points.

    Parameters
    ----------
    dataframe : pandas.DataFrame
        the dataframe with the data
    dataIdentifier : DataIdentifier
        the identifier of the dataframe to be used
    """
    max_radius = 5
    min_cluster_size = 1
    clusters = utils.cluster_points(utils.get_np_coords_from_df(dataframe, dataIdentifier), 
                                    max_radius,
                                    min_cluster_size)
    return clusters

@dataset_selector
def home_detection(dataframe, dataIdentifier):
    max_radius = 1
    min_cluster_size = 1
    selector = Selector(None, None, "0111110", "111111000000000000001111")
    filtered_df = select_df(dataframe, selector, dataIdentifier)
    print("depois", len(filtered_df))
    filtered_clusters = utils.cluster_points(utils.get_np_coords_from_df(filtered_df, dataIdentifier), 
                                             max_radius,
                                             min_cluster_size)
    print('total de clusters', len(filtered_clusters))
    return filtered_clusters, max(filtered_clusters, key = lambda i: len(i)) 

