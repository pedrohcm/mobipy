import geopy as gp
import pandas as pd

def calculateDistance(lat1, lon1, lat2, lon2):
    coords1 = (lat1, lon1)
    coords2 = (lat2, lon2)
    distance = gp.distance(coords1, coords2).m #utiliza o modelo WGS-84
    return distance

def get_time_spent_in_minutes(timestamp_start_time, timestamp_end_time):
    return int(timestamp_end_time-timestamp_start_time) / 60

def get_blox_plot_info(data):
    df = pd.DataFrame(data) 
    quantiles = df.quantile([0.25,0.5,0.75])
    return quantiles