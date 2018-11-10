import cv2
import numpy as np 
import argparse
import os
import json

def sortline(pts,limit):
    xs = pts.T[0]
    ys = pts.T[1]
    sort_index = xs.argsort()
    l0 = sort_index[ys[sort_index]<limit]
    l1 = sort_index[ys[sort_index]>limit]
    return l0, l1


parser = argparse.ArgumentParser(description='Read lines of arucos.')
parser.add_argument("--line-sep", type=int, help="Position, in pixels on image, of line seperation", default=300)
parser.add_argument("--retries", type=int, help="how many frames to accumulate for detections", default=5)
parser.add_argument("--words", type=str, help="Load number-to-word json")
parser.add_argument("--vis", action="store_true")

args = parser.parse_args()

line_sep = args.line_sep 
vis = args.vis 

words =  dict([(i,str(i)) for i in range(1000)])
if args.words and os.path.isfile(args.words):
    words = json.load(open(args.words,"r"))

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_1000)

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    
    agg_ids = []
    agg_corners = []

    for k in range(5):
        ret, frame = cap.read()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        corners, ids, foo = cv2.aruco.detectMarkers(gray, aruco_dict)
        if ids is None:
            continue
        for c, i in zip(list(corners), list(ids)):
            if i not in agg_ids:
                agg_ids.append(i[0])
                agg_corners.append(c)

    ids = np.array(agg_ids)
    corners = np.array(agg_corners)
    l0 = ""
    l1 = ""
    if len(corners) > 0:
        up_left = np.array([c[0][0] for c in corners])
        l0, l1 = sortline(up_left, line_sep)
        l0 = " ".join(words[str(x)] for x in ids[l0])
        l1 = " ".join(words[str(x)] for x in ids[l1])
        print("Line 1:\t\t", l0)
        print("Line 2:\t\t", l1)
        

    if vis:
        frame = cv2.aruco.drawDetectedMarkers(frame,corners, ids)
        width = frame.shape[1]
        cv2.line(frame, (0, line_sep), (width, line_sep), (0,200,200))
        cv2.putText(frame, l0, (1,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0)
        cv2.putText(frame, l1, (1,line_sep+50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('u'):
            line_sep -= 5
            print("Line sep ", line_sep)
        if key == ord('d'):
            line_sep += 5
            print("Line sep ", line_sep)
        if key == ord('q'):
            break

# When everything done, release the capture
cap.release()