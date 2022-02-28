from math import acos
import numpy as np
from ReturnClass import ReturnClass

class MyConvexHull():

    def __new__(self, bucket):
        self.__convexHull = []
        self.__convexHullIndex = []
        self.__pointIndexMapping = {}

        i = 0
        for element in bucket:
            self.__pointIndexMapping[repr(element)] = i
            i += 1

        p1 = bucket[0]
        p2 = bucket[0]

        for i in range(1, len(bucket)):
            if (bucket[i][0] < p1[0]):
                p1 = bucket[i]
            elif (bucket[i][0] == p1[0] and bucket[i][1] < p1[1]):
                p1 = bucket[i]
            
            if (bucket[i][0] > p2[0]):
                p2 = bucket[i]
            elif (bucket[i][0] == p2[0] and bucket[i][1] > p2[1]):
                p2 = bucket[i]

        up, down = self.__divide(p1, p2, bucket)

        del bucket

        self.__convexHullSolver(self, p1, p2, up, True)
        self.__convexHullSolver(self, p1, p2, down, False)

        for element in self.__convexHull:
            self.__convexHullIndex.append([self.__pointIndexMapping[repr(element[0])], self.__pointIndexMapping[repr(element[1])]])
    
        ret = ReturnClass()
        ret.simplices = self.__convexHullIndex

        return ret

    def __convexHullSolver(self, p1, p2, points, upSide):
        if (len(points) == 0):
            self.__convexHull.append([p1, p2])

        elif (len(points) == 1):
            self.__convexHull.append([p1, points[0]])
            self.__convexHull.append([points[0], p2])

        else:
            maxPoints = [points[0]]
            maxDistance = self.__distanceOfPointToLine(self, points[0], p1, p2)

            for i in range(1, len(points)):
                distance = self.__distanceOfPointToLine(self, points[i], p1, p2)

                if (distance > maxDistance):
                    maxPoints = [points[i]]
                    maxDistance = distance

                elif (distance == maxDistance):
                    maxPoints.append(points[i])

            maxPoint = []
            if (len(maxPoints) == 1):
                maxPoint = maxPoints[0]

            else: # Sudah dipastikan len(maxPoints) > 1
                maxAngle = self.__angleOfThreePoints(self, maxPoints[0], p2, p1)
                maxPointIndex = 0

                for i in range(1, len(maxPoints) - 1):
                    currentAngle = self.__angleOfThreePoints(self, maxPoints[i], p1, p2)

                    if (currentAngle > maxAngle):
                        maxAngle = currentAngle
                        maxPointIndex = i

                maxPoint = maxPoints[maxPointIndex]

            if (upSide):
                self.__convexHullSolver(self, p1, maxPoint, self.__getPointsAbove(p1, maxPoint, points), upSide)
                self.__convexHullSolver(self, maxPoint, p2, self.__getPointsAbove(maxPoint, p2, points), upSide)

            else:
                self.__convexHullSolver(self, p1, maxPoint, self.__getPointsBelow(p1, maxPoint, points), upSide)
                self.__convexHullSolver(self, maxPoint, p2, self.__getPointsBelow(maxPoint, p2, points), upSide)

        return

    def __divide(p1, p2, points):
        up = []
        down = []

        for point in points:
            determinan = p1[0] * p2[1] + point[0] * p1[1] + p2[0] * point[1] - point[0] * p2[1] - p2[0] * p1[1] - p1[0] * point[1]

            if (determinan > 0.00001):
                up.append(point)

            elif (determinan < -0.00001):
                down.append(point)

        return up, down

    def __getPointsAbove(p1, p2, points):
        ret = []

        for point in points:
            determinan = p1[0] * p2[1] + point[0] * p1[1] + p2[0] * point[1] - point[0] * p2[1] - p2[0] * p1[1] - p1[0] * point[1]

            if (determinan > 0.00001):
                ret.append(point)

        return ret

    def __getPointsBelow(p1, p2, points):
        ret = []
        
        for point in points:
            determinan = p1[0] * p2[1] + point[0] * p1[1] + p2[0] * point[1] - point[0] * p2[1] - p2[0] * p1[1] - p1[0] * point[1]

            if (determinan < -0.00001):
                ret.append(point)

        return ret

    def __lengthBetweenPoints(p1, p2):
        return ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5

    def __distanceOfPointToLine(self, point, p1, p2):
        # Menguunakan Shoelace Algorithm
        # x1 y2 + x2 y3 + x3 y1 - x2 y1 - x3 y2 - x1 y3
        area = 0.5 * abs(p1[0] * p2[1] + p2[0] * point[1] + point[0] * p1[1] - p2[0] * p1[1] - point[0] * p2[1] - p1[0] * point[1])

        return 2 * area / self.__lengthBetweenPoints(p1, p2)

    def __angleOfThreePoints(self, p1, p2, corner):
        a = self.__lengthBetweenPoints(p1, corner)
        b = self.__lengthBetweenPoints(p2, corner)
        c = self.__lengthBetweenPoints(p1, p2)
        
        # Rumus Cosinus
        cosOfAngle = ((a * a) + (b * b) - (c * c)) / (2 * a * b)

        return acos(cosOfAngle)