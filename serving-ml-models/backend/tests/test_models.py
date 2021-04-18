import unittest
import cv2
from ppgan.apps import Photo2CartoonPredictor
from detection.RetinaFaceAntiCov.retinaface_cov import RetinaFaceCoV

import sys
import numpy as np
import datetime
import os
import glob


class TestModels(unittest.TestCase):
    """Model test cases."""
    @unittest.skip("Tested successful!")
    def test_photo2cartoon(self):
        p2c = Photo2CartoonPredictor()
        nd_arr = p2c.run('test_images/photo3.jpg')
        image = cv2.cvtColor(nd_arr, cv2.COLOR_RGB2BGR)
        print(type(image))

    def test_retinaface_anti_cov_face_detector(self):
        thresh = 0.8
        mask_thresh = 0.2
        scales = [640, 1080]
        count = 1
        gpuid = -1
        detector = RetinaFaceCoV('backend/model/pre-trained/mnet_cov2', 0,
                                 gpuid, 'net3l')


if __name__ == '__main__':
    unittest.main()
