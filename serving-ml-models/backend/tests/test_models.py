import unittest
from ppgan.apps import Photo2CartoonPredictor
import cv2


class TestModels(unittest.TestCase):
    def test_photo2cartoon(self):
        p2c = Photo2CartoonPredictor()
        nd_arr = p2c.run('test_images/photo3.jpg')
        image = cv2.cvtColor(nd_arr, cv2.COLOR_RGB2BGR)
        print(type(image))

    def test_retinaface_anti_cov_face_detector():
        pass


if __name__ == '__main__':
    unittest.main()
