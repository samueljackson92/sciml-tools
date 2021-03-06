import pytest
import numpy as np
from sciml_tools import image
from PIL import Image

@pytest.fixture()
def tiff_path(tmpdir):
    path = tmpdir / 'test.tiff'

    data = np.random.randint(0, 255, (10,10)).astype(np.uint8)
    im = Image.fromarray(data)
    im.save(str(path), format='TIFF')
    return str(path)

def test_load_tiff(tiff_path):
    img = image.load_tiff(tiff_path)
    assert img.shape == (10, 10)

def test_crop_center():
    img = np.random.random((100, 100))
    img = image.crop_center(img, .8)
    assert img.shape == (80, 80)

    img = np.random.random((100, 100, 3))
    img = image.crop_center(img, .8)
    assert img.shape == (80, 80, 3)
