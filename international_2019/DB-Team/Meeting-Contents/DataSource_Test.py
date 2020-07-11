import cv2, time, math


if __name__ == "__main__":
    cam0 = cv2.VideoCapture(0)
    cam1 = cv2.VideoCapture(1)
    count = 0
    total_count = 0
    start = time.time()
    while True:
        for i in range(1000000):
            math.gcd(i, i + 3)
        for i in range(1000000):
            math.gcd(i, i + 3)
        ret, frame = cam0.read()
        ret, frame = cam1.read()
        count += 1
        now = time.time()

        if now - start > 10:
            start = now
            print("Count of CAM: %d" % (count))
            total_count += count
            count = 0

        if total_count > 1000:
            print("Terminate CAM")
            break
    
    cam0.release()
    cam1.release()
    cv2.destroyAllWindows()