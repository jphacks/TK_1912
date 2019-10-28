import cv2
import time
import numpy as np
import os
import math
from numpy import linalg as LA
from collections import Counter
import glob
import sys
sys.path.append('./lib')
from tf_pose.estimator import TfPoseEstimator

# tf-openposeを用いたポーズ推定
class tfOpenpose:

    def __init__(self):
        # openposeが返却するポーズ番号
        self.point = {"Nose":0, "Neck":1, "RShoulder":2,"RElbow":3,"RWrist":4,
                "LShoulder":5, "LElbow":6, "LWrist":7, "MidHip":8, "RHip":9,
                "RKnee":10, "RAnkle":11,"LHip":12, "LKnee":13, "LAnkle":14,
                "REye":15, "LEye":16, "REar":17, "LEar":18, "LBigToe":19,
                "LSmallToe":20, "LHeel":21, "RBigToe":22, "RSmallToe":23, "RHeel":24,
                "Background":25}
        self.width = 320
        self.height = 176
    
    # モデルデータの読み込み
    def setting(self):
        model = './lib/tf-pose-estimation/models/graph/mobilenet_v2_small/graph_opt.pb'
        self.e = TfPoseEstimator(model, target_size=(self.width, self.height))
    
    # 動画の撮影に伴う設定。
    def captureSetting(self, filename, user, area):
        self.user = user
        self.area = area
        self.root = './static/data/'+self.user+'/'+self.area
        os.makedirs(self.root, exist_ok=True)
        self.cam = cv2.VideoCapture(0)
        # CamWidth = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH) )
        # CamHeight = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        fps = self.cam.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.save_video = self.root+'/'+filename+'.avi'
        self.writer = cv2.VideoWriter(self.save_video, fourcc, fps, (self.width, self.height))
    
    # 撮影した動画を指定したフレームごとに画像に変更してポーズ推定を行う
    def MovieToImage(self):
        save_root = './static/data/'+self.user+'/'+self.area
        os.makedirs(save_root, exist_ok=True)
        for i in ['A', 'B', 'C', 'NG']:
            os.makedirs(save_root + '/' + i, exist_ok=True)
        # 動画を読み取る
        cap = cv2.VideoCapture(self.save_video)
        num = 0
        labels = []
        print('~~~~~~~~~~~~スタート~~~~~~~~~~~~~~')
        while cap.isOpened():
            ret, ori_image = cap.read()
            if ret == True:
                # openposeによる骨格推定
                humans = self.e.inference(ori_image, resize_to_default=(self.width > 0 and self.height > 0), upsample_size=4.0)
                image, center = TfPoseEstimator.draw_humans(ori_image, humans, imgcopy=False)
                # 自作アルゴリズムによるポーズ推定
                image, label = self.detect_pose(center=center, image=image)
                labels.append(label)
                cv2.imwrite(save_root+'/'+label+"/picture{:0=3}".format(num)+".jpg", ori_image)
                num += 1
            else:
                break
        counter = Counter(np.array(labels))
        print(counter)
        print(counter.keys())
        # 最も多いかった予測結果を出力
        acc_label = counter.most_common()[0][0]
        # 最も多いラベルがNGであり、次に多いラベルがNG以外の場合は次に多いラベルに更新
        if (acc_label == 'NG') and (len(counter.keys()) != 1):
            acc_label = counter.most_common()[1][0]
        filename = sorted(glob.glob(save_root+'/'+acc_label+'/*'))
        return acc_label, filename[0]
    
    # openposeによるリアルタイム骨格推定と動画の撮影を行う。
    def takeMovie(self):
        fps_time = 0
        start = time.time()
        while True:
            ret_val, image = self.cam.read()
            reImage = cv2.resize(image, (self.width, self.height))
            end = time.time()
            # 7秒後に撮影とリアルタイム骨格推定を実施
            if (end - start) > 7:
                self.writer.write(reImage)
                # openposeによる骨格推定
                humans = self.e.inference(image, resize_to_default=(self.width > 0 and self.height > 0), upsample_size=4.0)
                image, center = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)
                # 自作アルゴリズムによるポーズ推定
                image, label = self.detect_pose(center=center, image=image)
                # fpsの埋め込み
                cv2.putText(image,
                            "FPS: %f" % (1.0 / (time.time() - fps_time)),
                            (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 1)
            else:
                # 7秒未満はカウントダウン
                image = self.TextComposition(text=int((7 - (end - start) )), bg=image)
            cv2.imshow('tf-pose-estimation result', image)
            fps_time = time.time()
            ##### 今のポーズが出題される３つのポーズに該当しているとき、正解判定するコードを書く

            if cv2.waitKey(1) & 0xFF == ord('q') or end - start > 15:
                break
        self.cam.release()
        self.writer.release()
        cv2.destroyAllWindows()

    # 画像の埋め込み
    def ImageComposition(self, fg, bg, cX=0, cY=0):
        hImg, wImg = fg.shape[:2]
        hBack, wBack = bg.shape[:2]
        if (cX == 0) and (cY == 0):
            cX, cY = int(wBack/2), int(hBack/2)
        halfX, halfY = int(wImg/2), int(hImg/2)
        yUp, xLeft = (cY-halfY), (cX-halfX)
        yDown, xRight = (cY+halfY), (cX+halfX)
        bg[yUp:yDown, xLeft:xRight] = fg
        return bg
    # カウントダウン表示にともなう文字の埋め込み
    def TextComposition(self, text, bg, cX=0, cY=0):
        hBack, wBack = bg.shape[:2]
        if (cX == 0) and (cY == 0):
            cX, cY = int(wBack/2), int(hBack/2)
        cv2.putText(bg,
            "%d" % text,
            (cX-100, cY+100),  cv2.FONT_HERSHEY_SIMPLEX, 10,
            (255,255,255), 8)
        return bg

    # 各自作アルゴリズムによるポーズ推定の結果を統合
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
                    (10, 120),  cv2.FONT_HERSHEY_SIMPLEX, 4,
                    (255, 0, 0), 3)
        # print('angle_center:', angle_center, 'angle_right:', angle_right, 'angle_left:', angle_left)
        return image, label
    # 両手を広げるポーズ
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
    # 片手を上げるポーズ
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
    # 脇を絞めて、肘を下に、手は上にするポーズ
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
    # openposeが推定した骨格に指定した骨格位置が存在するか確認
    def is_included_point(self, dic, name_list):
        ans = True
        for name in name_list:
            if not self.point[name] in dic:
                ans = False
        return ans
    # 3点間の角度を求める
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
        