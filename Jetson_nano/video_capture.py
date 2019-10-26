# coding: utf-8

import time
import cv2
def resize(frame):
    orgHeight, orgWidth = frame.shape[:2]
    size = (orgHeight/2, orgWidth/2)
    # to 432x368
    newframe = cv2.resize(frame, (432, 368) )
    return newframe
def main():
    cam = cv2.VideoCapture(0)
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 432)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 368)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH) )
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT) )
    print(width)
    print(height)
    fps = cam.get(cv2.CAP_PROP_FPS)

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    width = 432
    height = 368
    writer = cv2.VideoWriter('output.avi', fourcc, fps, (width, height))
    time.sleep(3)
    t1 = time.time()
    while True:
        ret, frame = cam.read()

        # resize
        frame = resize(frame)
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



    # cam.release()
    # cv2.destroyAllWindows()

if __name__ == '__main__':
    main()