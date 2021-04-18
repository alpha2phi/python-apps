import unittest
import cv2
from ppgan.apps import Photo2CartoonPredictor
from retinaface_cov import RetinaFaceCoV


class TestModels(unittest.TestCase):
    """Model test cases."""
    @unittest.skip("Tested successful!")
    def test_photo2cartoon(self):
        p2c = Photo2CartoonPredictor()
        nd_arr = p2c.run('test_images/photo3.jpg')
        image = cv2.cvtColor(nd_arr, cv2.COLOR_RGB2BGR)
        print(type(image))

    def test_retinaface_anti_cov_face_detector(self):
        pass


if __name__ == '__main__':
    unittest.main()
