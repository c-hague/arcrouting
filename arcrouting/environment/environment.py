def environmentFactory(polygons, repersentation):
    if repersentation == 'RTree':
        pass
    elif repersentation == 'Quadtree':
        pass
    else:
        pass


class Environment:
    def __init__(self, polygons, query):
        self.polygons = polygons
        self.query = query