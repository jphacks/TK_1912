
import time
import cv2
import numpy as np
import os
import math
from numpy import linalg as LA

from tf_pose.estimator import TfPoseEstimator


model = './tf-pose-estimation/models/graph/mobilenet_v2_small/graph_opt.pb'
args = {'camera': 0, 'model': model, 'resize': '320x176', 'resize_out_ratio': 4.0, 'show_process': False}
point = {"Nose":0, "Neck":1, "RShoulder":2,"RElbow":3,"RWrist":4,
            "LShoulder":5, "LElbow":6, "LWrist":7, "MidHip":8, "RHip":9,
            "RKnee":10, "RAnkle":11,"LHip":12, "LKnee":13, "LAnkle":14,
            "REye":15, "LEye":16, "REar":17, "LEar":18, "LBigToe":19,
            "LSmallToe":20, "LHeel":21, "RBigToe":22, "RSmallToe":23, "RHeel":24,
            "Background":25}
def is_included_point(dic, name_list):
    
    for name in name_list:
        if not point[name] in dic:
            ans = False

    return ans
def detect_A(center, image):
    if is_included_point(center, ['Neck', 'RWrist', 'LWrist', 'RElbow', 'LElbow', 'RShoulder', 'LShoulder', 'Nose']):
        angle_center = CalculationAngle(center=center[point['Neck']],
                                    p1=center[point['RWrist']],
                                    p2=center[point['LWrist']])
        angle_right = CalculationAngle(center=center[point['RElbow']],
                                    p1=center[point['RShoulder']],
                                    p2=center[point['RWrist']])
        angle_left = CalculationAngle(center=center[point['LElbow']],
                                    p1=center[point['LShoulder']],
                                    p2=center[point['LWrist']])
        if angle_center > 90 and angle_right > 135 and angle_left > 135 and abs(center[point['RWrist']][1] - center[point['LWrist']][1]) < 30:
            return True

    return False

def detect_B(center, image):
    if is_included_point(center, ['Neck', 'RWrist', 'LWrist', 'RElbow', 'LElbow', 'RShoulder', 'LShoulder', 'Nose']):

            if (center[point['RWrist']][1] <  center[point['Nose']][1]) ^ (center[point['LWrist']][1] < center[point['Nose']][1]):
                if center[point['RWrist']][1] < center[point['LWrist']][1]:
                    angle_elbow = CalculationAngle(center=center[point['RElbow']],
                                        p1=center[point['RWrist']],
                                        p2=center[point['RShoulder']])
                else:
                    angle_elbow = CalculationAngle(center=center[point['LElbow']],
                                        p1=center[point['LWrist']],
                                        p2=center[point['LShoulder']] )
                if angle_elbow > 135:
                    return True

    return False

def detect_C(center, image):
    if is_included_point(center, ['Neck', 'RWrist', 'LWrist', 'RElbow', 'LElbow', 'RShoulder', 'LShoulder', 'Nose']):
        angle_center = CalculationAngle(center=center[point['Neck']],
                                    p1=center[point['RElbow']],
                                    p2=center[point['LElbow']])
        angle_right = CalculationAngle(center=center[point['RElbow']],
                                    p1=center[point['RShoulder']],
                                    p2=center[point['RWrist']])
        angle_left = CalculationAngle(center=center[point['LElbow']],
                                    p1=center[point['LShoulder']],
                                    p2=center[point['LWrist']])
        if 60 < angle_center < 160 and angle_right < 100 and angle_left < 100 and abs(center[point['RWrist']][1] - center[point['LWrist']][1]) < 30:
            return True
    return False

def detect_pose(center, image):
    if detect_A(center, image):
        label = 'A'
    elif detect_B(center, image):
        label = 'B'
    elif detect_C(center, image):
        label = 'C'
    else :
        label = 'NG'
    cv2.putText(image,
                label,
                (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 255, 0), 2)
    # print('angle_center:', angle_center, 'angle_right:', angle_right, 'angle_left:', angle_left)
    return image

def CalculationAngle(p1, p2, center):
    nparr_p1 = np.array([p1[0], p1[1]])
    nparr_p2 = np.array([p2[0], p2[1]])
    nparr_center = np.array([center[0], center[1]])

    vec_p1 = nparr_p1 - nparr_center
    vec_p2 = nparr_p2 - nparr_center
    i = np.inner(vec_p1, vec_p2)
    n = LA.norm(vec_p1) * LA.norm(vec_p2)

    c = i / n
    angle = np.rad2deg(np.arccos(np.clip(c, -1.0, 1.0)))
    return angle


def main():
    fps_time = 0
    w, h = map(int, args['resize'].split('x'))
    if w > 0 and h > 0:
        e = TfPoseEstimator(args['model'], target_size=(w, h))
    else:
        e = TfPoseEstimator(args['model'], target_size=(432, 368))
    cam = cv2.VideoCapture(args['camera'])
    ret_val, image = cam.read()

    while True:
        ret_val, image = cam.read()
        humans = e.inference(image, resize_to_default=(w > 0 and h > 0), upsample_size=args['resize_out_ratio'])

        image, center = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
        image = detect_pose(center=center, image=image)
        print(center)
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        if 0 in center:
            cv2.rectangle(image, center[0], (center[0][0] + 20, center[0][1] + 20), (255, 255, 255) )
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        ##### 今のポーズが出題される３つのポーズに該当しているとき、正解判定するコードを書く

        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
