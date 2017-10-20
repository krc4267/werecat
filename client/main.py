from __future__ import unicode_literals
from kivy.support import install_twisted_reactor
install_twisted_reactor()

from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
    def dataReceived(self, data):
        print data
		
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

		
import kivy
import os

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView

#index = open('index', 'r')

class WerecatBase(App):
   
    connection = None
   
    def build(self):
        self.read_config()
        return self.setup_gui()
        
    def read_config(self):
        self.wcconf = {'test': 603}
        self.config = open('/home/krc/.config/werecatrc')
        self.configlines = self.config.readlines()
        for i in self.configlines:
            print i.split()
            self.wcconf [i.split(':')[0].strip()] = i.split(':')[1].strip()
        print 'loaded configuration'
        print self.wcconf

    def setup_gui(self):
        self.baselayout = BoxLayout(orientation='vertical',padding=10)
        self.controlbuttonbox = BoxLayout(orientation='horizontal',size=(1,60),size_hint=(1,None))
        self.songscroll = ScrollView(size_hint=(.7,1))
        self.listscroll = ScrollView(size_hint=(.3,1))
        self.songbox = BoxLayout(orientation='vertical',size_hint=(1,None))
        self.listbox = BoxLayout(orientation='vertical',size_hint=(1,None))
        self.songslists = BoxLayout(orientation='horizontal')
        self.setup_controls()
        
        self.listbox.bind(minimum_height=self.listbox.setter('height'))
        self.songbox.bind(minimum_height=self.songbox.setter('height'))
        
        self.baselayout.add_widget(self.controlbuttonbox)
        self.baselayout.add_widget(self.songslists)
        self.songslists.add_widget(self.listscroll)
        self.songslists.add_widget(self.songscroll)
        
        self.songscroll.add_widget(self.songbox)
        self.listscroll.add_widget(self.listbox)
        
        self.render_listlist()
        
        #TESTING
        self.connectbutton = Button(text='connect', on_press=self.connect_server,size=(20,20),size_hint=(None,None))
        self.sendbutton = Button(test='sending', on_press=self.send_message,size=(20,20),size_hint=(None,None))
        self.controlbuttonbox.add_widget(self.sendbutton)
        self.controlbuttonbox.add_widget(self.connectbutton)
        
        return self.baselayout

    def create_songdisplay(self, song):
        self.songdata = song.split(';')
        self.songdisplay = BoxLayout(orientation='horizontal',size=(1,40),size_hint=(1,None))
        print self.songdata[1]
        self.playnext = Button(text='Play\nNext', id='next:'+self.songdata[0], size=(55,1), size_hint=(None,1),on_press=self.playsong)
        self.songdisplay.add_widget(self.playnext)
        self.queue = Button(text='Add to\nQueue', id='queue:'+self.songdata[0], size=(55,1), size_hint=(None,1),on_press=self.playsong)
        self.songdisplay.add_widget(self.queue)
        self.songtitle = Button(text=self.songdata[0], id='now:'+self.songdata[0], on_press=self.playsong)
        self.songdisplay.add_widget(self.songtitle)
        self.artist = Button(text=self.songdata[1])
        self.songdisplay.add_widget(self.artist)
        self.album = Button(text=self.songdata[2])
        self.songdisplay.add_widget(self.album)
        self.duration = Label(text=self.songdata[3])
        self.songdisplay.add_widget(self.duration)
        return self.songdisplay
        
    def render_songlist(self, instance, *args): #songindexlocation is the path to a text file produced by the indexer script
		self.songbox.clear_widgets()
		self.songindexlocation = "./lists/"+instance.text
		self.songindex = open(self.songindexlocation, 'r')
		self.songlist = self.songindex.readlines()
		for i in self.songlist:
			self.songbox.add_widget(self.create_songdisplay(i))
			
    def render_listlist(self, indexdir="./lists"):
        for i in os.listdir(indexdir):
            self.listbutton = Button(text=i,size=(1,40),size_hint=(1,None))
            self.listbutton.bind(on_press=self.render_songlist)
            self.listbox.add_widget(self.listbutton)
			
    def connect_server(self, *args):
        reactor.connectTCP('localhost', 1234, EchoClientFactory(self))

    def on_connection(self, connection):
        print 'connected'
        self.connection = connection
	   
    def send_message(self, *args):
        print 'sending message'
        self.connection.write('test'.encode('utf-8'))

    def setup_controls(self):
		pass
		
    def playsong(self, instance):
#		self.queuefile = open(
#        self.when = instance.id.split(:)[0]
        if self.when == now:
            self.connection.write('now:'+song)
        
#        if self.when == 'next':
			
		
if __name__ == '__main__':
    WerecatBase().run()

