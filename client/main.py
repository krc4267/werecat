import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout

index = open('index', 'r')

class WerecatBase(App):
    def build(self):
        return self.setup_gui()

    def setup_gui(self):
        self.baselayout = BoxLayout(orientation='vertical')
        self.controlbuttonbox = BoxLayout(orientation='horizontal')
        self.stopbutton = Button(text='Stop')
        self.controlbuttonbox.add_widget(self.stopbutton)
        self.baselayout.add_widget(self.controlbuttonbox)
        for i in index.readlines():
            self.baselayout.add_widget(self.create_songdisplay(i))
        return self.baselayout

    def create_songdisplay(self, song):
        self.songdata = song.split(';')
        self.songdisplay = BoxLayout(orientation='horizontal',size=(800,40),size_hint=(None,None))
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

if __name__ == '__main__':
    WerecatBase().run()
