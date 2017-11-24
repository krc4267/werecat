#from __future__ import unicode_literals
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor, protocol




		
import kivy
import os
import time

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock

#index = open('index', 'r')

class WerecatBase(App):
    wcconf={}
    connection = None
   
    def build(self):
        #self.read_config()
        return self.connectdialog()
        #return self.setup_gui()
        
    def connectdialog(self):
		
		#FOR LATER IMPLEMENTATION
		#FOR NOW SET THE SERVER IN THE CONFIG FILE
		
		#self.recentservers = open(self.wcconf["Recent Servers File Location"])
		
		#self.default = 'default'
		#self.baselayout = BoxLayout(orientation='vertical')
		#self.ipbox = TextInput(text=self.default, multiline=False, size_hint=(20, None))
		#for i in self.recentservers.readlines():
		#	print i
		#	self.baselayout.add_widget(Button(text='thing', size_hint=(20, None)))
			
		#self.baselayout.add_widget(self.ipbox)
		
		#return self.baselayout
		
		return self.setup_gui()
		
#    def read_config(self):
    wcconf = {'test': 603}
    config = open('./wcconf')
    configlines = config.readlines()
    for i in configlines:
        print i.split(':')
        wcconf [i.split(':')[0].strip()] = i.split(':')[1].strip()
    print 'loaded configuration'
    print wcconf

    def setup_gui(self):
        self.baselayout = BoxLayout(orientation='vertical',padding=10)
        self.controlbuttonbox = BoxLayout(orientation='horizontal',size=(1,60),size_hint=(1,None))
        self.songscroll = ScrollView(size_hint=(.6,1))
        self.listscroll = ScrollView(size_hint=(.2,1))
        self.queuescroll = ScrollView(size_hint=(.2,1))
        self.songbox = BoxLayout(orientation='vertical',size_hint=(1,None))
        self.listbox = BoxLayout(orientation='vertical',size_hint=(1,None))
        self.queuebox = BoxLayout(orientation='vertical',size_hint=(1,None))
        self.songslists = BoxLayout(orientation='horizontal')
        self.setup_controls()
        
        self.listbox.bind(minimum_height=self.listbox.setter('height'))
        self.songbox.bind(minimum_height=self.songbox.setter('height'))
        self.queuebox.bind(minimum_height=self.queuebox.setter('height'))
        print self.queuebox
        
        self.baselayout.add_widget(self.controlbuttonbox)
        self.baselayout.add_widget(self.songslists)
        self.songslists.add_widget(self.listscroll)
        self.songslists.add_widget(self.songscroll)
        self.songslists.add_widget(self.queuescroll)
        
        self.songscroll.add_widget(self.songbox)
        self.listscroll.add_widget(self.listbox)
        self.queuescroll.add_widget(self.queuebox)
        
        self.queueupdatebutton = Button(text='Update Queue', size=(1,40),size_hint=(1,None))
        self.queueupdatebutton.bind(on_press=self.get_queue)
        self.queuebox.add_widget(self.queueupdatebutton)
        
        self.render_queuelist('test:test:thing:test')
        
        self.render_listlist()
        
        #TESTING
        self.connectbutton = Button(text='connect', on_press=self.connect_server,size=(0,20),size_hint=(.4,None))
        self.controlbuttonbox.add_widget(self.connectbutton)
        
        return self.baselayout
    
    def sort_by_album(self, instance, *args):
		self.songbox.clear_widgets()
		self.songindex = open(self.wcconf['Playlist Directory']+'All Music', 'r')
		self.songlist = self.songindex.readlines()
		for i in self.songlist:
			if i.split(';')[2] == instance.id.split(':')[1]:
				self.songbox.add_widget(self.create_songdisplay(i))
				
    def sort_by_artist(self, instance, *args):
		self.songbox.clear_widgets()
		self.songindex = open(self.wcconf['Playlist Directory']+'All Music', 'r')
		self.songlist = self.songindex.readlines()
		for i in self.songlist:
			if i.split(';')[1] == instance.id.split(':')[1]:
				self.songbox.add_widget(self.create_songdisplay(i))
    
    def openlist(self, instance, *args):
        self.currentlist = instance.id
        self.playbutton.text = 'current list: '+instance.id
    
    def addlist(self, instance, *args):
        print 'ADDLIST'
        print instance.id
        print self.currentlist
        print '//ADDLIST'
        self.outlist = open('newlists/'+self.currentlist, 'a')
        self.outlist.write(str(instance.id))
        self.outlist.close()

    def create_songdisplay(self, song):
        self.songdata = song.split(';')
        self.songdisplay = BoxLayout(orientation='horizontal',size=(1,40),size_hint=(1,None))
#        print song
#        print self.songdata
        self.playnext = Button(text='Add to current playlist', id=str(song), size=(300,1), size_hint=(None,1),on_press=self.addlist)
        self.songdisplay.add_widget(self.playnext)
        self.songtitle = Button(text=self.songdata[0], id='now:'+self.songdata[0], on_press=self.playsong)
        self.songdisplay.add_widget(self.songtitle)
        self.artist = Button(text=self.songdata[1], id=self.songdata[0]+':'+self.songdata[1], on_press=self.sort_by_artist)
        self.songdisplay.add_widget(self.artist)
        self.album = Button(text=self.songdata[2], id=self.songdata[0]+':'+self.songdata[2], on_press=self.sort_by_album)
        self.songdisplay.add_widget(self.album)
        self.duration = Label(text=self.songdata[3])
        self.songdisplay.add_widget(self.duration)
        return self.songdisplay
        
    def render_songlist(self, instance, *args): #songindexlocation is the path to a text file produced by the indexer script
		self.songbox.clear_widgets()
		self.songindexlocation = self.wcconf['Playlist Directory']+instance.text
		self.songindex = open(self.songindexlocation, 'r')
		self.songlist = self.songindex.readlines()
		for i in self.songlist:
			self.songbox.add_widget(self.create_songdisplay(i))
			
    def render_listlist(self, indexdir=wcconf['Playlist Directory']):
        self.listbox.clear_widgets()
        for i in os.listdir(indexdir):
            self.listbutton = Button(text=i,size=(1,40),size_hint=(1,None))
            self.listbutton.bind(on_press=self.render_songlist)
            self.listbox.add_widget(self.listbutton)
	
    def stupid_intermediary_function(self, queue):
        self.render_queuelist(queue)
	
    def render_queuelist(self, queue):
        self.queuebox.clear_widgets()
        self.queueupdatebutton = Button(text='Update Queue', size=(1,40),size_hint=(1,None))
        self.queueupdatebutton.bind(on_press=self.render_queuelist)
        self.queuebox.add_widget(self.queueupdatebutton)
        for i in os.listdir('newlists'):
            self.queuebutton = Button(text=i,size=(1,40),size_hint=(1,None), id=i)
            self.queuebutton.bind(on_press=self.openlist)
            self.queuebox.add_widget(self.queuebutton)
	
    def get_queue(self, *args):
        self.connection.write('wants queue: ')
	
    def connect_server(self, *args):
        reactor.connectTCP(self.wcconf['Server Address'], int(self.wcconf['Server Port']), EchoClientFactory(self))

    def on_connection(self, connection):
        print 'connected'
        self.connection = connection
	   
    def send_message(self, *args):
        print 'sending message'
        self.connection.write('test'.encode('utf-8'))

    def setup_controls(self):
		self.stopbutton = Button(text='Stop', on_press=self.stop)
		self.playbutton = Button(text='Play', on_press=self.play)
		self.skipbutton = Button(text='Skip', on_press=self.skip)
		
		self.controlbuttonbox.add_widget(self.stopbutton)
		self.controlbuttonbox.add_widget(self.playbutton)
		self.controlbuttonbox.add_widget(self.skipbutton)
		
		pass
		
    def playsong(self, instance): #was going to hold queuefile here, but decided that's pointless and stupid
        self.when = instance.id.split(':')[0] #so decided to just use this to dispatch messages to the server
        if self.when == 'now': #instead. server will keep queue in a list.
            self.connection.write('now:'+str(instance.id.split(':')[1]))
            Clock.schedule_once(self.get_queue, 0.25)
            
        if self.when == 'queue':
            self.connection.write('queue:'+str(instance.id.split(':')[1]))
            Clock.schedule_once(self.get_queue, 0.25)
        
        if self.when == 'next':
            self.connection.write('insert:'+str(instance.id.split(':')[1])+':0')
            Clock.schedule_once(self.get_queue, 0.25)

	
    def stop(self,*args):
        self.connection.write('stop: ')
	
    def play(self, *args):
        self.connection.write('start: ')
	
    def skip(self, *args):
        self.connection.write('skip: ')

wb = WerecatBase()

class EchoClient(protocol.Protocol, WerecatBase):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
    def dataReceived(self, data):
        print data
        if data.split(':')[0] == 'queue':
			self.queuesplit = data
			self.wb = wb
			self.wb.stupid_intermediary_function(self.queuesplit)
			
class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        print 'started connecting'

    def clientConnectionLost(self, reason, connector):
        print 'lost connection: '+str(reason)

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed: '+str(reason)
		
if __name__ == '__main__':
    wb.run()

