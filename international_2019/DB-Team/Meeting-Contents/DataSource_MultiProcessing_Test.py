import cv2, time
from multiprocessing import Pool
import math


def BroadCasting(num):
    capture = cv2.VideoCapture(num)
    count = 0
    total_count = 0
    start = time.time()
    while True:
        ret, frame = capture.read()
        count += 1
        now = time.time()
        for i in range(1000000):
            math.gcd(i, i + 3)
        if now - start > 10:
            start = now
            print("Count of CAM [%d]: %d" % (num, count))
            total_count += count
            count = 0

        if total_count > 90:
            print("Terminate CAM [%d]" % num)
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    pool = Pool(2)
    pool.map(BroadCasting, [0, 1])