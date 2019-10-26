import time
import cv2
import numpy as np
import os

from tf_pose.estimator import TfPoseEstimator


model = './mobilenet_v2_small/graph_opt.pb'
args = {'camera': 0, 'model': model, 'resize': '320x176', 'resize_out_ratio': 4.0, 'show_process': False}

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
        print(center)
        cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
        cv2.imshow('tf-pose-estimation result', image)
        fps_time = time.time()
        ##### 今のポーズが出題される３つのポーズに該当しているとき、正解判定するコードを書く
        
        if cv2.waitKey(1) == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
