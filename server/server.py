import os
from time import sleep

prefix='/home/krc/Downloads/'
location = '/home/krc/Projects/werecat/server/'

def play(song):
    os.system("cvlc --play-and-exit "+'"'+prefix+song+'"'+"*")

while True:
    playlist = open(location+'playlist')
    trackList = playlist.readlines()
    print trackList
    if len(trackList) == 0:
        sleep(2)
        playlist.close()
        continue
    os.system('sed -i -e "1d" '+location+'playlist')
    play(trackList[0])
