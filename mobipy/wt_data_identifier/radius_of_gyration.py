import math
import helpers

def calculateRadiusOfGyration(points, midPoint=None):
    sum = 0
    if midPoint is None:
        midPoint = helpers.calculateMidPoint(points)
    for i in range(len(points)):
        base = helpers.calculateDistance(points[i][0], points[i][1], midPoint[0], midPoint[1])
        sum += math.pow(base, 2)
    sum = math.sqrt(sum / len(points))
    return sum