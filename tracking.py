import cv2
import numpy as np
from matplotlib import pyplot as plt

available_trackers = {
    'KCF': cv2.TrackerKCF_create(),
    'CSRT': cv2.TrackerCSRT_create(),
    'MIL': cv2.TrackerMIL_create(),
}
tracker_type = 'KCF'
if tracker_type in available_trackers:
    tracker = available_trackers[tracker_type]
source  = 0
cap = cv2.VideoCapture(source)
ret, frame = cap.read()
if not ret:
    print("无法读取视频源")
while True:
    x = input("请输入x坐标: ")
    print(x)
    print(type(x))
    if x == 'q':
        break
    y = input("请输入y坐标: ")
    width = input("请输入宽度: ")
    height = input("请输入高度: ")
    bbox = (int(x), int(y), int(width), int(height))
    frame_copy = frame.copy()
    cv2.rectangle(frame_copy, bbox, (0, 255, 0), 2)
    frame_rgb = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
    plt.imshow(frame_rgb)
    plt.title('Tracking Box')
    plt.show()
    #根据输入确认跟踪框
    if input("确认跟踪框吗? (y/n): ") == 'y':
        break
    else:
        continue
tracker.init(frame, bbox)
while True:
    ret, frame = cap.read()
    if not ret:
        print("无法读取视频源")
        break
    success, bbox = tracker.update(frame)
    if success:
        (x, y, w, h) = [int(v) for v in bbox]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows() 
