import pytest

import numpy as np

from pyntcloud import PyntCloud


def assert_points_xyz(data):
    assert np.isclose(data.points['x'][0], 0.5)
    assert np.isclose(data.points['y'][0], 0)
    assert np.isclose(data.points['z'][0], 0.5)

    assert str(data.points["x"].dtype) == 'float32'
    assert str(data.points["y"].dtype) == 'float32'
    assert str(data.points["z"].dtype) == 'float32'


def assert_points_color(data):
    assert data.points['red'][0] == 255
    assert data.points['green'][0] == 0
    assert data.points['blue'][0] == 0

    assert str(data.points['red'].dtype) == 'uint8'
    assert str(data.points['green'].dtype) == 'uint8'
    assert str(data.points['blue'].dtype) == 'uint8'


def assert_mesh(data):
    assert data.mesh["v1"][0] == 0
    assert data.mesh["v2"][0] == 1
    assert data.mesh["v3"][0] == 2

    assert str(data.mesh['v1'].dtype) == 'int32'
    assert str(data.mesh['v2'].dtype) == 'int32'
    assert str(data.mesh['v3'].dtype) == 'int32'


@pytest.mark.parametrize("extension,color,mesh,comments", [
    (".ply", True, True, False),
    ("_ascii.ply", True, True, True),
    ("_ascii_vertex_index.ply", True, True, True),
    (".npz", True, True, False),
    (".obj", False, True, False),
    (".off", False, False, False),
    ("_color.off", True, False, False),
    (".bin", False, False, False),
    (".las", True, False, False),
    (".laz", True, False, False)
])
def test_from_file(data_path, extension, color, mesh, comments):
    cloud = PyntCloud.from_file(str(data_path / "diamond{}".format(extension)))
    assert_points_xyz(cloud)
    if color:
        assert_points_color(cloud)
    if mesh:
        assert_mesh(cloud)
    if comments:
        assert cloud.comments == ["PyntCloud is cool"]


def test_obj_issue_221(data_path):
    """ Regression test https://github.com/daavoo/pyntcloud/issues/221
    """
    cloud = PyntCloud.from_file(str(data_path / "obj_issue_221.obj"))

    assert (len(cloud.xyz)) == 42
    assert (len(cloud.mesh)) == 88


def test_obj_issue_226(data_path):
    """ Regression test https://github.com/daavoo/pyntcloud/issues/226
    """
    cloud = PyntCloud.from_file(str(data_path / "obj_issue_226.obj"))

    assert "w" in cloud.points.columns

def test_obj_issue_vn(data_path):
    """
    Fix type issue in pyntcloud/io/obj.py.
    A float is passed to range() instead of an integer.
    for i in range(f[0].count("/") / 2):
    TypeError: 'float' object cannot be interpreted as an integer
    """
    cloud = PyntCloud.from_file(str(data_path / "obj_issue_vn.obj"))

    assert len(cloud.xyz) == 3
    assert len(cloud.mesh) == 1
