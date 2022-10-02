import cv2
import time
import pandas
from datetime import datetime

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status = 0
status_list = []
times = []
df = pandas.DataFrame(columns=["Start", "End"])

while True:

    check, frame = video.read()

    # print(check)
    # print(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

    delta_frame = cv2.absdiff(first_frame, gray)

    thresh_delta = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_delta = cv2.dilate(thresh_delta, None, iterations=2)


    # print(delta_frame - gray)

    (cnts, _) = cv2.findContours(thresh_delta.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    status = 0
    for contour in cnts:
        if cv2.contourArea(contour) < 5000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    status_list.append(status)
    if len(status_list) >= 2 and status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if len(status_list) >= 2 and status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())
    # time.sleep(3)

    cv2.imshow("Thresh Delta", thresh_delta)
    cv2.imshow("Capturing", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    print(status)
    if key == ord("q"):
        if status == 1:
            times.append(datetime.now())
        break

print(times)
video.release()

for i in range(0, len(times), 2):
    df = df.append({"Start": times[i], "End": times[i+1]}, ignore_index=True)

df.to_csv("Times.csv")

cv2.destroyAllWindows()
