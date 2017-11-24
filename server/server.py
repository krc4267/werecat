from twisted.internet import protocol, reactor, endpoints
import threading
import subprocess
import os

class Echo(protocol.Protocol):
    playing = False
    stopped = False
    queue = []
	
    def popenAndCall(self, onExit, popenArgs):
        def runInThread(onExit, popenArgs):
            print 'gothere'
            print popenArgs
            proc = subprocess.Popen(popenArgs, shell=True, env=dict(os.environ))
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
		subprocess.call(('pkill', '-9','vlc')) #HACKY SHIT, DON'T DO THIS
		self.stopped = True
    
    def playSong(self, song):
		d = dict(os.environ)
		if self.playing:
			subprocess.call(('pkill','-9','vlc')) #HACKY SHIT, DON'T DO THIS
		songspath = '/home/krc/Projects/werecat/client/songs/'
		self.popenAndCall(self.playNext,('cvlc','-v', '--play-and-exit', songspath+song+'.mp3'))
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
            self.playNext()
            
    def playNext(self):
		print 'playing next song'
		if self.stopped:
			pass
			
		if len(self.queue) == 0:
			print 'cannot play next song as there is no such thing'
			self.stopSong()
			pass
		else:
			self.playSong(self.queue.pop(0))
		
	
    def addQueue(self, song, where=-1):
		if where == -1:
			print 'adding '+song+' to end of queue'
			self.queue.append(song)
			pass
		else:
			print 'inserting '+song+' to queue at position '+str(where)
			self.queue.insert(where, song)
			
			
			
			
			
class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Echo()
        
endpoints.serverFromString(reactor, "tcp:1234").listen(EchoFactory())
reactor.run()
