from arcrouting.util import Polygon
import numpy as np


def test_polygon_contains():
    p = Polygon(np.array([[0, 0], [1, 0], [0, 1]]))
    assert p.containsPoint(np.array([.25, .25]))
    assert not p.containsPoint(np.array([1, 1]))
    assert p.containsPoint(np.array([0, 0]))
