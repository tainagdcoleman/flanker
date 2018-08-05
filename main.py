import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty
import os

import yaml

path = os.path.dirname(os.path.realpath(__file__))

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
        config_path = os.path.join(path, 'data', f'{game}.yml')
        config = yaml.load(open(config_path))
        sm.current = 'instruction'

class Flanker(Screen):
    def on_enter(self):
        pass

class Memory(Screen):
    def on_enter(self):
        pass

class Instruction(Screen):
    instructions = ListProperty([])
    counter = NumericProperty(0)
    
    def on_pre_enter(self):
        global info, config
        self.info = info 
        instructions = config['instructions']  
        for instruction in instructions:
            instruction['image'] = os.path.join(path, 'data', instruction['image'])
        
        self.counter = 0
        self.instructions = instructions

    def next(self):
        if self.counter + 1 >= len(self.instructions):
            sm.current = config['game']
            return
        self.counter += 1


sm.add_widget(Start(name='start'))
sm.add_widget(Flanker(name='flanker'))
sm.add_widget(Memory(name='memory'))
sm.add_widget(Instruction(name = 'instruction'))

class MyApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()