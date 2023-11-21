import numpy as np
import skgeom as sg


APPROX_ZERO = 1e-4


class Polygon:
    def __init__(self, points):
        self.skg = sg.Polygon(points)

    def contains(self, point: np.ndarray):
        p = sg.Point2(point[0], point[1])
        return self.skg.on_side(p) != sg.ON_UNBOUNDED_SIDE

    def intersects(self, other: 'Polygon'):
        return sg.do_intersect(self.skg, other.skg)


class BoundingBox(Polygon):
    def __init__(self, xMin, xMax, yMin, yMax):
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.skg = sg.Polygon([
            (xMin, yMin),
            (xMax, yMin),
            (xMax, yMax),
            (xMin, yMax)
        ])

    def contains(self, point: np.ndarray):
        tx = point[0]
        ty = point[1]
        if (self.xMin - tx) * (self.xMax - tx) > -APPROX_ZERO:
            return False
        if (self.yMin - ty) * (self.yMax - ty) > - APPROX_ZERO:
            return False
        return True
