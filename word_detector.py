import cv2
import numpy as np 
import argparse
from pyexcel_ods import get_data
import json

try:
    words_dict = json.load(open("words.json","r"))
except:
    words_dict = {}

def sortline(pts,limit):
    xs = pts.T[0]
    ys = pts.T[1]
    sort_index = xs.argsort()[::-1]
    l0 = sort_index[ys[sort_index]<limit]
    l1 = sort_index[ys[sort_index]>limit]
    return l0, l1


class WordDetector(object):
    def __init__(self, line_sep=300, vis=False, retries=5, cam=0):
        self.line_sep = line_sep
        self.vis = vis 
        self.retries = retries
        self.cam = cam
        self.cap = cv2.VideoCapture('/dev/video1')
        self.dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_1000)
        self.wdict = words_dict
    

    def words(self, num):
        for word, value in self.wdict.items():
            if num == value['id']:
                return word

        return str(num)

    def detect_in_single_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.dict)
        return corners, ids


    def visulize(self, frame, corners, ids, l0, l1):
        frame = cv2.aruco.drawDetectedMarkers(frame,corners, ids)
        width = frame.shape[1]
        cv2.line(frame, (0, self.line_sep), (width, self.line_sep), (0,200,200))
        cv2.putText(frame, l0, (1,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0)
        cv2.putText(frame, l1, (1,self.line_sep+50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0)

        # Display the resulting frame
        cv2.imshow('frame',frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('u'):
            self.line_sep -= 5
            print("Line sep ", self.line_sep)
        if key == ord('d'):
            self.line_sep += 5
            print("Line sep ", self.line_sep)
        if key == ord('q'):
            import sys
            sys.exit(0)

    def detect(self):
        agg_ids = []
        agg_corners = []
        l0 = ""
        l1 = ""

        for i in range(self.retries):
            ret, frame = self.cap.read()
            corners, ids = self.detect_in_single_frame(frame)

            if ids is None:
                continue
            for c, i in zip(list(corners), list(ids)):
                if i not in agg_ids:
                    agg_ids.append(i[0])
                    agg_corners.append(c)
            
            ids = np.array(agg_ids)
            corners = np.array(agg_corners)

        if len(corners) > 0:
            up_left = np.array([c[0][0] for c in corners])
            l0, l1 = sortline(up_left, self.line_sep)
            l0 = " ".join(self.words(x) for x in ids[l0])
            l1 = " ".join(self.words(x) for x in ids[l1])

        if self.vis:
            self.visulize(frame, corners, ids, l0, l1)

        return l0 + ' ' + l1


def create_words_from_ods():
    data = get_data('words_list.ods')

    output = {}

    for i, line in enumerate(data["Sheet1"]):
        print(line)
        if len(line) < 3:
            continue

        word = line[0].lower()
        id = line[1]
        rank = line[2]
        output[word] = {'rank': rank, 'id':id}

    print(output)
    json.dump(dict(output), open("words.json", "w"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read lines of arucos.')
    parser.add_argument("--line-sep", type=int, help="Position, in pixels on image, of line seperation", default=300)
    parser.add_argument("--retries", type=int, help="how many frames to accumulate for detections", default=5)
    parser.add_argument("--vis", action="store_true")
    parser.add_argument("--cam", type=int, default=0, help="Open CV cam number")

    args = parser.parse_args()

    line_sep = args.line_sep
    vis = args.vis

    wd = WordDetector(args.line_sep,vis=True, retries=args.retries, cam=args.cam)

    while(True):
        # Capture frame-by-frame
        print(wd.detect())
    # create_words_from_ods()

        

