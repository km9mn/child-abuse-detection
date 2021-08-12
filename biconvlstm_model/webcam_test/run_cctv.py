import cv2
import numpy as np
import time
import requests
import json

url = 'https://4f9793ad14d0.ngrok.io/predict'
step_size = 5

def main():
    cap = cv2.VideoCapture(0)
    idx = 1
    total = 0
    frames = list()
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    fps = cap.get(cv2.CAP_PROP_FPS) # 30
    width  = cap.get(cv2.CAP_PROP_FRAME_WIDTH)   # float
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float
    out = cv2.VideoWriter('test'+str(idx)+'.mp4', fourcc,fps, (int(width), int(height)))
    model_ret = 1

    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = np.array(frame)
        if model_ret == 0:
            frame[-20:,-20:,0] = 0
            frame[-20:,-20:,1] = 0
            frame[-20:,-20:,2] = 255
        else:
            frame[-20:,-20:,0] = 255
            frame[-20:,-20:,1] = 0
            frame[-20:,-20:,2] = 0
        cv2.imshow('frame',frame)

        if not ret:
            break
        out.write(frame)
        
        total += 1
        frames.append(frame)

        if (total%60==0):
            print(idx,total)
            idx +=1
            filename = 'test'+str(idx)+'.mp4'
            out = cv2.VideoWriter(filename, fourcc,fps, (int(width), int(height)))

            # frames 보내기
            st_time = time.time()
            print(np.array(frames).shape)
            flatten_vid = np.array(frames)[::step_size,:,:,:].flatten()
            print(flatten_vid.shape)
            data = {
                'frames':np.array(frames).shape[0]/step_size,
                'width':width,
                'height':height,
                'flatten_vid':flatten_vid.tolist()
            }
            print(type(data))
            with open("testing.json", "w") as json_file:
                json.dump(data, json_file)

            model_ret = requests.post(url, data=json.dumps(data))
            print('model ret : ', model_ret)
            print('model took : ',round(time.time()-st_time, 3),' sec')
            

            #model_ret = 1
            ##############################################33
            frames = list()

        if idx>10:
            break
            
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return

main()