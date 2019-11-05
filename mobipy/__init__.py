import math

def calculateMidPoint(points):
    x = 0
    y = 0
    z = 0

    for i in range(len(points)):
        latitude = points[i][0] * (math.pi / 180)
        longitude = points[i][1] * (math.pi / 180)

        x += math.cos(latitude) * math.cos(longitude)
        y += math.cos(latitude) * math.sin(longitude)
        z += math.sin(latitude)

    total = len(points)

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
    
def calculateRadiusOfGyration(points, midPoint=None):
    sum = 0
    if midPoint is None:
        midPoint = calculateMidPoint(points)
    for i in range(len(points)):
        base = calculateDistance(points[i][0], points[i][1], midPoint[0], midPoint[1])
        sum += math.pow(base, 2)
    sum = math.sqrt(sum / len(points))
    return sum