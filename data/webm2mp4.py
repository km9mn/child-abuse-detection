import os
import glob
import ffmpeg

path = 'C:/Users/Seogki/GoogleDrive/데이터청년캠퍼스_고려대과정/youtube_data'

for path_in in glob.glob(path+'/**/*.webm', recursive=True):
    path_out = path_in.split('.webm')[0] + '.mp4'
    print(path_in)
    print(path_out)
    cmd = 'ffmpeg -i "'+path_in+'" "'+path_out+'"'
    os.system(cmd)