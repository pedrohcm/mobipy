import pandas as pd
import dao
import sys
sys.path.append('../mobipy')
#from classes.identifier import Identifier
#from ..classes.selector import Selector
#from ..helpers import dataset_filter, get_sample_df
#from ..metrics import metrics

dataframe = []
dataIdentifier = []
selector = []

def radius_of_gyration_test(dataframe, dataIdentifier):
    #metrics.radius_of_gyration(dataframe, dataIdentifier)
    print("Todo")

def group_by_closeness_test(dataframe_a, dataframe_b, dataIdentifier):
    #metrics.group_by_closeness(dataframe_a, dataframe_b, dataIdentifier)
    print("Todo")

def home_detection_test(dataframe, dataIdentifier):
    #metrics.home_detection(dataframe_a, dataIdentifier)
    print("Todo")

def user_displacement_distance_test():
    print("Todo")

def activity_center_test():
    print("Todo")

if __name__ == "__main__":
    all_srs = pd.concat(dao.load_user_stop_regions("5958"), axis=0)
    print(all_srs)