import time
import cv2
import numpy as np
import os
import math
from numpy import linalg as LA

from tf_pose.estimator import TfPoseEstimator
from collections import Counter


model = './tf-pose-estimation/models/graph/mobilenet_v2_small/graph_opt.pb'
args = {'video': 'output.avi', 'model': model, 'resolution': '320x176', 'show_process': False, 'showBG': True}
point = {"Nose":0, "Neck":1, "RShoulder":2,"RElbow":3,"RWrist":4,
            "LShoulder":5, "LElbow":6, "LWrist":7, "MidHip":8, "RHip":9,
            "RKnee":10, "RAnkle":11,"LHip":12, "LKnee":13, "LAnkle":14,
            "REye":15, "LEye":16, "REar":17, "LEar":18, "LBigToe":19,
            "LSmallToe":20, "LHeel":21, "RBigToe":22, "RSmallToe":23, "RHeel":24,
            "Background":25}

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='tf-pose-estimation Video')
    # parser.add_argument('--video', type=str, default='')
    # parser.add_argument('--resolution', type=str, default='432x368', help='network input resolution. default=432x368')
    # parser.add_argument('--model', type=str, default='mobilenet_thin', help='cmu / mobilenet_thin / mobilenet_v2_large / mobilenet_v2_small')
    # parser.add_argument('--show-process', type=bool, default=False,
    #                     help='for debug purpose, if enabled, speed for inference is dropped.')
    # parser.add_argument('--showBG', type=bool, default=True, help='False to show skeleton only.')

    w, h = map(int, args['resolution'].split('x'))
    e = TfPoseEstimator(args['model'], target_size=(w, h))
    cap = cv2.VideoCapture(args['video'])

    if cap.isOpened() is False:
        print("Error opening video stream or file")
    while cap.isOpened():
        ret_val, image = cap.read()
        if not ret_val:
            break
        humans = e.inference(image)
        if not args['showBG']:
            image = np.zeros(image.shape)
        image, center = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

        # cv2.putText(image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()