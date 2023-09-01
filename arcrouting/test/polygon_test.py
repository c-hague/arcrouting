from arcrouting.util import SimplePolygon
import numpy as np

def test_polygon_contains():
    p = SimplePolygon(np.array([[0, 0], [1, 0], [0, 1]]))
    assert p.contains(np.array([.25, .25]))
    assert not p.contains(np.array([1, 1]))
    assert p.contains(np.array([0, 0]))