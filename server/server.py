from twisted.internet import protocol, reactor, endpoints
import threading
import subprocess
import os

class Echo(protocol.Protocol):
    playing = False
    stopped = False
    queue = []
    
    conf = {}
    config = open('./wcserver.conf')
    configlines = config.readlines()
    for i in configlines:
        print i.split(':')
        conf [i.split(':')[0].strip()] = i.split(':')[1].strip()
    
    def popenAndCall(self, onExit, popenArgs):
        def runInThread(onExit, popenArgs):
            print 'gothere'
            print popenArgs
            proc = subprocess.Popen(popenArgs,shell=True)
            proc.wait()
            onExit()
            return
        thread = threading.Thread(target=runInThread, args=(onExit, popenArgs))
        print 'thread started?'
        thread.start()
        # returns immediately after the thread starts
        return thread
        
    def stopSong(self):
		print 'stopping'
		os.system('tmux send-keys -t werecat q')
		self.stopped = True
    
    def playSong(self, song):
        self.current = song
        d = dict(os.environ)
        if self.playing:
            os.system('tmux send-keys -t werecat q')
        songspath = '/home/krc/legionwidemusic/'
        self.popenAndCall(self.playNext,('gst-play-1.0 '+songspath+'*'+song.replace(' ','\ ')+'*'))
        self.playing = True
	
    def dataReceived(self, data):
        print 'received'+data
        if data == 'stop':
			self.stop()
			pass
        if data.split(':')[0] == 'now':
            print 'RECEIVED: playing song now'
            self.playSong(data.split(':')[1])
            pass
        
        if data.split(':')[0] == 'queue':
            print 'RECEIVED: adding to queue'
            self.addQueue(data.split(':')[1])
            pass
        
        if data.split(':')[0] == 'insert':
			print 'RECEIVED: inserting to queue'
			self.addQueue(data.split(':')[1],int(data.split(':')[2]))
			pass
		
        if data.split(':')[0] == 'stop':
            self.stopSong()
		
        if data.split(':')[0] == 'start':
            self.stopped = False
            self.playNext()
        
        if data.split(':')[0] == 'skip':
            self.skipSong()
            
        if data.split(':')[0] == 'wants queue':
            self.queuestr = 'queue:'
            for i in self.queue:
                self.queuestr = self.queuestr + i + ':'
            print self.queuestr
            self.transport.write(self.queuestr)
        
        if data.split(':')[0] == 'clear queue':
            print 'clearing queue'
            self.queue = []

        if data.split(':')[0] == 'wants current':
            print 'sending current'
            self.transport.write('current:'+current)
        
        if data.split(':')[0] == 'reindex':
            print 'starting indexer in second tmux'
            os.system('tmux new-session -dt wc-indexer')
     #       os.system('tmux send-keys -t wc-indexer g
     
        if data.split(':')[0] == 'volume':
            if data.split(':')[1] == 'up':
                os.system('tmux send-keys -t werecat Up')
            if data.split(':')[1] == 'down':
                os.system('tmux send-keys -t werecat Down')

            
    def playNext(self):
        print 'playing next song'
        if self.stopped:
            return None
            self.queuestr = 'queue:'
            for i in self.queue:
                self.queuestr = self.queuestr + i + ':'
            print self.queuestr
            self.transport.write(self.queuestr)
        if len(self.queue) == 0:
            print 'cannot play next song as there is no such thing'
            self.stopSong()
            pass
        else:
            self.playSong(self.queue.pop(0))
            
    def skipSong(self):
        print 'skipping song'
        os.system('tmux send-keys -t werecat ^C')
	
    def addQueue(self, song, where=-1):
		if where == -1:
			print 'adding '+song+' to end of queue'
			self.queue.append(song)
			pass
		else:
			print 'inserting '+song+' to queue at position '+str(where)
			self.queue.insert(where, song)
			
    def getIndex(self):
        if len(os.listdir(conf['New Song Directory'])) == 0:
            self.transport.write('INDEX:generating
			
			
class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()
        
endpoints.serverFromString(reactor, "tcp:1234").listen(EchoFactory())
reactor.run()
