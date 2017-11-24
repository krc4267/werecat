#Alright here we go guys, it's an ugly-ass indexing system!
#It.. should work.

import sys
import os
import subprocess

if len(sys.argv) <2:
    print 'missing directory argument!'
    quit()

indexdir = sys.argv[1]+'/'

index = open(sys.argv[2], 'a')

for i in os.listdir(indexdir):
    print i
    title = subprocess.check_output('ffprobe "'+indexdir+i+'" 2>&1 | grep title | sed -e s/^.*://',shell=True)
    artist = subprocess.check_output('ffprobe "'+indexdir+i+'" 2>&1 | grep artist | sed -e s/^.*://',shell=True)
    album = subprocess.check_output('ffprobe "'+indexdir+i+'" 2>&1 | grep album | sed -e s/^.*://',shell=True)
    duration = subprocess.check_output('ffprobe "'+indexdir+i+'" 2>&1 | grep -o "..:..:.."',shell=True)
    metadata = title.strip()+';'+artist.strip()+';'+album.strip()+';'+duration.strip()
    print metadata.split(';')
    index.write(metadata+'\n')
   
