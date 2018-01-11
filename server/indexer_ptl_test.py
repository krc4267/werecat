import pytaglib

index = open('indexfile', a)
for i in os.listdir('/mnt/archives/music/'):
    song = taglib.File(i)
    
