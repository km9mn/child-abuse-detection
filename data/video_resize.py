import os
import sys
import cv2
import glob
import time
import imutils
import numpy as np

def video_resize(target, out, out_width=720, frame_rate=24):
    cap = cv2.VideoCapture(target)
    # width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) # 영상의 넓이(가로) 프레임
    # height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) # 영상의 높이(세로) 프레임
    # frameRate = int(cap.get(cv2.CAP_PROP_FPS)) 
    # print(width, height, frameRate)
    
    # 비디오 저장 변수
    writer = None
    prev_time = 0
    
    while True:
        # ret : 성공적으로 불러왔는지 확인
        # frame : 읽어온 frame 정보    
        ret, frame = cap.read()
        
        cur_time = time.time() - prev_time
        # 읽은 Frame이 없는 경우 종료
        if (not ret) and (cur_time > 1./frame_rate):
            prev_time = time.time()
            break

        # Frame Resize
        frame = imutils.resize(frame, width=out_width)
        # cv2.imshow('frame', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        # 저장할 video 설정
        if writer is None:
            fourcc = cv2.VideoWriter_fourcc(*"XVID")  # MJPG
            writer = cv2.VideoWriter(out, fourcc, frame_rate, (frame.shape[1], frame.shape[0]), True)
        
        # 비디오 저장
        if writer is not None:
            writer.write(frame)
    
    cap.release()

def main():
    path = sys.argv[1] # "D:/AIHub/이상행동 CCTV 영상/01.폭행(assult)" 
    width = int(sys.argv[2])
    fps = int(sys.argv[3])

    for filepath in glob.glob(path +'/**/*', recursive=True):
        #print('FILE PATH : ', filepath)
        filename = filepath.split('\\')[-1].split('.')[0]
        file_format = filepath.split('.')[-1]
        file_path = filepath.split(filename)[0]
        #print(filename,file_format,file_path)

        if file_format == 'mp4' or file_format == 'avi':
            start_time = time.time()
            out_path = file_path + filename + '_resized_' + str(width) + '_' + str(fps) + '.' + file_format

            print('**** working on " '+ filename +' " ****')
            video_resize(filepath, out_path, out_width=width, frame_rate=fps)
            print('time took : ', round(time.time() - start_time,3) , ' sec')

if __name__=='__main__':
    main()