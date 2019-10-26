import cv2
import time
import numpy as np
import os
import math
from numpy import linalg as LA
import sys
# sys.path.append('./lib')
from tf_pose.estimator import TfPoseEstimator

class tfOpenpose:

    def __init__(self):
        self.point = {"Nose":0, "Neck":1, "RShoulder":2,"RElbow":3,"RWrist":4,
                "LShoulder":5, "LElbow":6, "LWrist":7, "MidHip":8, "RHip":9,
                "RKnee":10, "RAnkle":11,"LHip":12, "LKnee":13, "LAnkle":14,
                "REye":15, "LEye":16, "REar":17, "LEar":18, "LBigToe":19,
                "LSmallToe":20, "LHeel":21, "RBigToe":22, "RSmallToe":23, "RHeel":24,
                "Background":25}
        self.width = 320
        self.height = 176

    def setting(self):
        model = './tf-pose-estimation/models/graph/mobilenet_v2_small/graph_opt.pb'
        self.e = TfPoseEstimator(model, target_size=(self.width, self.height))
        self.cam = cv2.VideoCapture(0)

    def main(self):
        fps_time = 0
        while True:
            ret_val, image = self.cam.read()
            humans = self.e.inference(image, resize_to_default=(self.width > 0 and self.height > 0), upsample_size=4.0)

            image, center = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
            image = self.detect_pose(center=center, image=image)
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

    def detect_pose(self, center, image):
        if self.detect_A(center, image):
            label = 'A'
        elif self.detect_B(center, image):
            label = 'B'
        elif self.detect_C(center, image):
            label = 'C'
        else :
            label = 'NG'
        cv2.putText(image,
                    label,
                    (10, 30),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        # print('angle_center:', angle_center, 'angle_right:', angle_right, 'angle_left:', angle_left)
        return image

    def detect_A(self, center, image):
        if self.is_included_point(center, ['Neck', 'RWrist', 'LWrist', 'RElbow', 'LElbow', 'RShoulder', 'LShoulder', 'Nose']):
            angle_center = self.CalculationAngle(center=center[self.point['Neck']],
                                        p1=center[self.point['RWrist']],
                                        p2=center[self.point['LWrist']])
            angle_right = self.CalculationAngle(center=center[self.point['RElbow']],
                                        p1=center[self.point['RShoulder']],
                                        p2=center[self.point['RWrist']])
            angle_left = self.CalculationAngle(center=center[self.point['LElbow']],
                                        p1=center[self.point['LShoulder']],
                                        p2=center[self.point['LWrist']])
            if angle_center > 90 and angle_right > 135 and angle_left > 135 and abs(center[self.point['RWrist']][1] - center[self.point['LWrist']][1]) < 30:
                return True

        return False

    def detect_B(self, center, image):
        if self.is_included_point(center, ['Neck', 'RWrist', 'LWrist', 'RElbow', 'LElbow', 'RShoulder', 'LShoulder', 'Nose']):

                if (center[self.point['RWrist']][1] <  center[self.point['Nose']][1]) ^ (center[self.point['LWrist']][1] < center[self.point['Nose']][1]):
                    if center[self.point['RWrist']][1] < center[self.point['LWrist']][1]:
                        angle_elbow = self.CalculationAngle(center=center[self.point['RElbow']],
                                            p1=center[self.point['RWrist']],
                                            p2=center[self.point['RShoulder']])
                    else:
                        angle_elbow = self.CalculationAngle(center=center[self.point['LElbow']],
                                            p1=center[self.point['LWrist']],
                                            p2=center[self.point['LShoulder']] )
                    if angle_elbow > 135:
                        return True

        return False

    def detect_C(self, center, image):
        if self.is_included_point(center, ['Neck', 'RWrist', 'LWrist', 'RElbow', 'LElbow', 'RShoulder', 'LShoulder', 'Nose']):
            angle_center = self.CalculationAngle(center=center[self.point['Neck']],
                                        p1=center[self.point['RElbow']],
                                        p2=center[self.point['LElbow']])
            angle_right = self.CalculationAngle(center=center[self.point['RElbow']],
                                        p1=center[self.point['RShoulder']],
                                        p2=center[self.point['RWrist']])
            angle_left = self.CalculationAngle(center=center[self.point['LElbow']],
                                        p1=center[self.point['LShoulder']],
                                        p2=center[self.point['LWrist']])
            if 60 < angle_center < 160 and angle_right < 100 and angle_left < 100 and abs(center[self.point['RWrist']][1] - center[self.point['LWrist']][1]) < 30:
                return True
        return False

    def is_included_point(self, dic, name_list):
        ans = True
        for name in name_list:
            if not self.point[name] in dic:
                ans = False
        return ans

    def CalculationAngle(self, p1, p2, center):
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

if __name__ == "__main__":
    tf = tfOpenpose()
    print('初期化完了')
    tf.setting()
    print('設定完了')
    tf.main()