from arcrouting.environment import QuadTree
from arcrouting.util import BoundingBox, Polygon
import json
import matplotlib.pyplot as plt
import matplotlib.patches as pch


def test_quadtree():
    with open('data/tunnels.json') as f:
        env = json.load(f)

    tree = QuadTree(
        bbox=BoundingBox(*env['bounds']),
        sizeLimit=5
    )
    for polygon in env['polygons']:
        tree.add(Polygon(polygon))

        fig = plt.figure()
        ax = fig.add_subplot()
        for node in tree:
            if len(node.children) > 0:
                continue
            ax.add_patch(pch.Polygon(
                node.bbox.skg.coords,
                fc=('blue' if not node.isFree else 'white'),
                ec='k'
            ))
        ax.set_xlim([tree.root.bbox.xMin, tree.root.bbox.xMax])
        ax.set_ylim([tree.root.bbox.yMin, tree.root.bbox.yMax])
        plt.show()
