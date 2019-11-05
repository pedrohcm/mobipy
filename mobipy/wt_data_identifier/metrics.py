import math
from ..helpers import utils

def calculateRadiusOfGyration(points, midPoint=None):
    sum = 0
    if midPoint is None:
        midPoint = utils.calculateMidPoint(points)
    for i in range(len(points)):
        base = utils.calculateDistance(points[i][0], points[i][1], midPoint[0], midPoint[1])
        sum += math.pow(base, 2)
    sum = math.sqrt(sum / len(points))
    return sum

def user_displacement_distance(points):
    sum_user_distances = 0
    for i in range(0, len(points), 2):
        latitude_a = points[i][0]
        longitude_a = points[i][1]
        latitude_b = points[i+1][0]
        longitude_b = points[i+1][1]
        sum_user_distances += utils.calculateDistance(latitude_a, longitude_a, latitude_b, longitude_b)
    return sum_user_distances