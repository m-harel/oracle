import cv2 
import numpy as np 

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_7X7_1000)

aruco_id = 0
page_num = 0
while aruco_id<200:
    page_num+=1
    aruco_page = []
    for i in range(4):
        aruco_line=[]
        for j in range(3): 
            aruco_id += 1
            marker = cv2.aruco.drawMarker(aruco_dict,aruco_id, 140, borderBits=1)
            marker = np.pad(marker,(35,5),'constant', constant_values=255)
            cv2.putText(marker, str(aruco_id), (1,100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 0)
            aruco_line.append(marker)
        aruco_page.append(np.concatenate(aruco_line, axis=1))
    aruco_page = np.concatenate(aruco_page, axis=0)
    cv2.imwrite("aruco_page%2d.png" % page_num, aruco_page)
