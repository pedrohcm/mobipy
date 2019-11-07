import math
from ..helpers import utils
from ..helpers import dataset_selector
from ..classes.selector import Selector

def radius_of_gyration(dataframe, dataIdentifier, midPoint=None):
    sum = 0
    if midPoint is None:
        midPoint = utils.calculateMidPoint(dataframe, dataIdentifier)
    for row in dataframe.itertuples():
        base = utils.calculateDistance(getattr(row, dataIdentifier.latitude), 
            getattr(row, dataIdentifier.longitude), midPoint[0], midPoint[1])
        sum += math.pow(base, 2)
    sum = math.sqrt(sum / len(dataframe))
    return sum

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
            sum_user_distances += utils.calculateDistance(latitude_a, longitude_a, latitude_b, longitude_b)
            latitude_a = longitude_a = latitude_b = longitude_b = 0
    return sum_user_distances

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

def home_detection(dataframe, dataIdentifier):
    selector = Selector("", "", "0111110", "111111000000000000001111")
    filtered_df = dataset_selector.select_df(dataframe, selector, dataIdentifier)
    filtered_clusters = utils.cluster_points(utils.get_np_coords_from_df(filtered_df, dataIdentifier))
    for cluster in filtered_clusters:
        print(cluster) ##check if it has something to indicate its length
        ##use its length to ordenate
        ##get the most intense cluster
    return top_cluster

