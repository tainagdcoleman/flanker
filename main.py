import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty

import yaml

info = {}
config = {}


Builder.load_file('main.kv')

sm = ScreenManager()

class Start(Screen):
    def on_enter(self):
        global config
        config = {}

    def update(self, key, value):
        global info
        info[key] = value.encode('ascii')

    def start_game(self, game):
        global config
        config = yaml.load(open('data/flanker.yml'))
        sm.current = 'instruction'

class Flanker(Screen):
    def on_enter(self):
        pass

class Memory(Screen):
    def on_enter(self):
        pass

class Instruction(Screen):
    instructions = ListProperty([{'title': 'N/A'}])
    
    def on_enter(self):
        global info, config
        self.info = info 
        self.instructions = config['instructions']
        print(self.info)
        print(self.instructions)

    def next(self):
        self.instructions = self.instructions[1:]


sm.add_widget(Start(name='start'))
sm.add_widget(Flanker(name='flanker'))
sm.add_widget(Memory(name='memory'))
sm.add_widget(Instruction(name = 'instruction'))

class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()