import numpy as np
from arcrouting.util import BoundingBox, Polygon


class QuadTree:
    def __init__(self, bbox: BoundingBox, sizeLimit: float):
        self.root = QuadTreeNode(bbox, sizeLimit)

    def add(self, polygon: Polygon):
        self.root.split(polygon)

    def free(self, point: np.ndarray):
        self.root.free(point)
    
    def query(self, bbox: BoundingBox, free:bool=True):
        return self.root.query(bbox, free)

    def __iter__(self):
        items = [self.root]
        i = 0
        while i < len(items):
            for child in items[i].children:
                items.append(child)
            i += 1
        return iter(items)


class QuadTreeNode:
    def __init__(self, bbox: BoundingBox, minSize: float):
        self.bbox = bbox
        self.center = np.array([
            (bbox.xMin + bbox.xMax) * .5,
            (bbox.yMin + bbox.yMax) * .5
        ])
        self.length = bbox.xMax - bbox.xMin
        self.children = []
        self.isFree = True
        self.minSize = minSize

    def split(self, polygon: Polygon):
        # recursion stop
        if self.length < self.minSize:
            return
        # quadrants of cartisean plane
        if len(self.children) <= 0:
            self.children = [
                QuadTreeNode(BoundingBox(self.center[0], self.center[0] + self.length / 2,
                                         self.center[1], self.center[1] + self.length / 2), self.minSize),
                QuadTreeNode(BoundingBox(self.center[0] - self.length / 2, self.center[0],
                                         self.center[1], self.center[1] + self.length / 2), self.minSize),
                QuadTreeNode(BoundingBox(self.center[0] - self.length / 2, self.center[0],
                                         self.center[1] - self.length / 2, self.center[1]), self.minSize),
                QuadTreeNode(BoundingBox(self.center[0], self.center[0] + self.length / 2,
                                         self.center[1] - self.length / 2, self.center[1]), self.minSize)
            ]
        for child in self.children:
            if polygon.intersects(child.bbox):
                child.isFree = False
                child.split(polygon)

        if self.isFree:
            return

        join = True
        for child in self.children:
            if child.isFree or len(child.children) > 0:
                join = False

        if join:
            self.children = []

    def free(self, point: np.ndarray):
        if not self.bbox.contains(point):
            return True
        if len(self.children) <= 0:
            return self.isFree
        return (self.children[0].free(point)
                and self.children[1].free(point)
                and self.children[2].free(point)
                and self.children[3].free(point))

    def intersects(self, polygon: Polygon):
        if isinstance(polygon, BoundingBox):
            return not (polygon.xMin > self.bbox.xMax
                        or polygon.xMax < self.bbox.xMin
                        or polygon.yMax > self.bbox.yMin
                        or polygon.yMin < self.bbox.yMax)
        return self.bbox.intersects(self.bbox)

    def query(self, bbox: BoundingBox, free: bool):
        if len(self.children) <= 0:
            if self.isFree == free:
                return [self.bbox]
            else:
                return []
        
        r = []
        for child in self.children:
            r += child.query(bbox, free)
        return r
