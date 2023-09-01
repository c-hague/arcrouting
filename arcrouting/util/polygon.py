import numpy as np


class Polygon:
    def __init__(self, points):
        self.coords = points
    
    def contains(self, point: np.ndarray):
        return False

class SimplePolygon(Polygon):
    def contains(self, point):
        s = np.einsum('ij, ij -> i', self.normals(), point - self.coords)
        return not np.any(s > 0)

    def normals(self):
        return (self.coords - np.roll(self.coords, 1, axis=0)) @ np.array([[0, -1], [1, 0]])
