import sys
import cv2
import numpy as np
import time
import requests
import os
import json
from threading import Thread

from requests.models import Response

#code = 'c2630900a041'
url = sys.argv[1]
step_size = 5

class ThreadWithResult(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

def send_frame(video_path, url):
    print(os.path.basename(video_path)+ ' video sent!!')
    resp = requests.post(url + '/predict', files={'file': open(video_path,'rb')})
    print(os.path.basename(video_path)+ ' video got answer------------')
    return resp.json()

def main():
    cap = cv2.VideoCapture(0)
    idx = 1
    total = 0
    frames = list()
    video_path = 'C:/Users/Seogki/GoogleDrive/데이터청년캠퍼스_고려대과정/child-abuse-detection/biconvlstm_model/webcam_test/'

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS) 
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  
    filename = 'temp' + str(idx) + '.mp4'
    out = cv2.VideoWriter(filename, fourcc,fps, (int(width), int(height)))
    model_ret = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        frame = np.array(frame)

        if not ret:
            print('video capture failed')
            break

        out.write(frame)
        
        total += 1
        frames.append(frame)

        if total%60==0:
            out.release()

            request_thread = ThreadWithResult(target=send_frame, args=(video_path+filename, url))
            request_thread.start()

            idx = (idx + 1)%5

            filename = 'temp' + str(idx) + '.mp4'  
            out = cv2.VideoWriter(filename, fourcc,fps, (int(width), int(height)))
        
        try:
            model_ret = float(request_thread.result)
        except:
            pass

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if model_ret > 50:
            frame[::height-1,:,0] = frame[:,::width-1,0] = 0
            frame[::height-1,:,1] = frame[:,::width-1,1] = 0
            frame[::height-1,:,2] = frame[:,::width-1,2] = 255
        else:
            frame[::height-1,:,0] = frame[:,::width-1,0] = 255
            frame[::height-1,:,1] = frame[:,::width-1,1] = 0
            frame[::height-1,:,2] = frame[:,::width-1,2] = 0

        cv2.imshow('frame',frame)

    cap.release()
    cv2.destroyAllWindows()

    return

main()