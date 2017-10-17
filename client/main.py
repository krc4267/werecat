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
   
    def build(self):
        return self.setup_gui()

    def setup_gui(self):
        self.baselayout = BoxLayout(orientation='vertical',padding=10)
        self.controlbuttonbox = BoxLayout(orientation='horizontal',size=(1,60),size_hint=(1,None))
        self.songscroll = ScrollView(size_hint=(.7,1))
        self.songbox = BoxLayout(orientation='vertical',size_hint=(.7,1))
        self.listbox = BoxLayout(orientation='vertical',size_hint=(.3,1))
        self.songslists = BoxLayout(orientation='horizontal')
        self.setup_controls()
        
        self.baselayout.add_widget(self.controlbuttonbox)
        self.baselayout.add_widget(self.songslists)
        self.songslists.add_widget(self.listbox)
        self.songslists.add_widget(self.songbox)
        
        self.render_listlist()
        
        return self.baselayout

    def create_songdisplay(self, song):
        self.songdata = song.split(';')
        self.songdisplay = BoxLayout(orientation='horizontal',size=(1,40),size_hint=(1,None))
        print self.songdata[1]
        self.songtitle = Button(text=self.songdata[0])
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
			
			
		
		
        
    def setup_controls(self):
		pass
		
if __name__ == '__main__':
    WerecatBase().run()

