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
    time.sleep(3)
    t1 = time.time()
    while True:
        ret, frame = cam.read()

        t2 = time.time()
        if (t2 - t1) > 5:
            writer.write(frame)
        else:
            cv2.putText(frame,
                "%d sec" % (5 - (t2 - t1) ),
                (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                (0, 0, 0), 2)

        if cv2.waitKey(1) & 0xFF == ord('q') or t2 - t1 > 10:
            break
        
        cv2.imshow('frame', frame)



    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()