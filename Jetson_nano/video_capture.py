# coding: utf-8

import time
import cv2

def main():
    cam = cv2.VideoCapture(0)   
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) )
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) )
    fps = cam.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    writer = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))
    pressed_key = False
    t1 = 0
    while True:
        ret, frame = cam.read()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            pressed_key = True
            t1 = time.time()

        if pressed_key:
            t2 = time.time()
            if (t2 - t1) > 10:
                writer.write(frame)
            else:
                cv2.putText(frame,
                    "残り: %f 秒" % (10 - (t2 - t1) ),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)

        if pressed_key and t2 - t1 > 15:
            break
        
        cv2.imshow('frame', frame)



    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()