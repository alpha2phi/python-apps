import cv2
import numpy as np
from PIL import Image
from detection.RetinaFaceAntiCov.retinaface_cov import RetinaFaceCoV

THRESH = 0.8
MASK_THRES = 0.2
SCALES = [640, 1080]
COUNT = 1
GPU_ID = -1

detector = RetinaFaceCoV('model/pre-trained/mnet_cov2', 0, GPU_ID, 'net3l')


def retinaface_anticov(input_image):
    img = cv2.imdecode(np.fromstring(input_image.read(), np.uint8), 1)
    # print(img.shape)
    im_shape = img.shape
    target_size = SCALES[0]
    max_size = SCALES[1]
    im_size_min = np.min(im_shape[0:2])
    im_size_max = np.max(im_shape[0:2])
    im_scale = float(target_size) / float(im_size_min)

    # prevent bigger axis from being more than max_size:
    if np.round(im_scale * im_size_max) > max_size:
        im_scale = float(max_size) / float(im_size_max)

    # print('im_scale', im_scale)

    scales = [im_scale]
    flip = False

    faces = None
    for c in range(COUNT):
        faces, landmarks = detector.detect(img,
                                           THRESH,
                                           scales=scales,
                                           do_flip=flip)

    if faces is not None:
        print('Found - ', faces.shape[0], 'faces')
        for i in range(faces.shape[0]):
            face = faces[i]
            box = face[0:4].astype(np.int)
            mask = face[5]
            # print(i, box, mask)
            if mask >= MASK_THRES:
                color = (255, 255, 255)
            else:
                color = (0, 255, 0)
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 2)
            landmark5 = landmarks[i].astype(np.int)
            for l in range(landmark5.shape[0]):
                color = (255, 0, 0)
                cv2.circle(img, (landmark5[l][0], landmark5[l][1]), 1, color,
                           2)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return Image.fromarray(img)
    # cv2.imwrite(filename, img)
