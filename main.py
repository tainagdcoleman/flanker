import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty, StringProperty, DictProperty
from kivy.core.window import Window
from kivy.clock import Clock 

import os
import time
import yaml
from datetime import datetime
from dateutil import relativedelta

path = os.path.dirname(os.path.realpath(__file__))

info = {}
config = {}


Builder.load_file('main.kv')

sm = ScreenManager()

def get_data(log, correct_count):
    dob = datetime.strptime(info['nasc'], '%d/%m/%y')
    difference = relativedelta.relativedelta(datetime.now(), dob)
    info['idade_anos'] = difference.years
    info['idade_meses'] = difference.years * 12 + difference.months
    return {
        'usuario': info,
        'acertos': correct_count,
        'log': log
    }


class Start(Screen):
    def on_enter(self):
        global config
        config = {}

    def update(self, key, value):
        global info
        info[key] = value

    def start_game(self, game):
        global config
        config_path = os.path.join(path, 'data', f'{game}.yml')
        config = yaml.load(open(config_path))
        for i in range(len(config['instructions'])):
            print(i)
            config['instructions'][i]['title'] = config['instructions'][i]['title'].replace('\\n', '\n')
            config['instructions'][i]['prompt'] = config['instructions'][i]['prompt'].replace('\\n', '\n')
        sm.current = 'instruction'

class Flanker(Screen):
    content = ListProperty()
    right_image = StringProperty()
    left_image = StringProperty()
    counter = NumericProperty()

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] in self.keys and len(self.log) < len(self.content):       
            direction = keycode[1] in self.right_keys
            dt = time.time() - self.start_time
            self.log.append((direction, dt))
        
            if self.counter + 1 >= len(self.content):
                sm.current = 'start'
                return True  
            self.counter += 1
            self.start_time = time.time()
        return True

    def on_pre_enter(self):
        self.left_keys = {'q', 'left'}
        self.right_keys = {'p', 'right'}
        self.keys = self.left_keys | self.right_keys
        self.left_image = os.path.join(path, 'data', config['left_image'])
        self.right_image = os.path.join(path, 'data', config['right_image'])
        self.middle = True
        self.crowd = True
        self.content = config['content']
        self.counter = 0

        self.start_time = time.time()
        self.log = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self):
        log_data = []
        correct_count = 0
        for i in range(len(self.log)):
            user_dir, dt = self.log[i]
            ans_dir = self.content[i][1]
            if user_dir == ans_dir:
                correct_count += 1
            log_data.append({
                'resposta do usuario': 'direita' if user_dir else 'esquerda',
                'resposta desejada': 'direita' if ans_dir else 'esquerda',
                'time': dt
            })

        data = get_data(log_data, correct_count)

        import pprint
        pprint.pprint(data)

        self._keyboard.unbind(on_key_down=self._on_keyboard_down)

class Memory(Screen):
    counter = NumericProperty()
    inner_counter = NumericProperty()
    content = ListProperty()
    order = ListProperty()
    paths = DictProperty()
   
    def update(self, dt):
        if self.inner_counter + 1 < len(self.content[self.counter]):
            self.inner_counter += 1
            if self.inner_counter + 1 >= len(self.content[self.counter]):
                self.interval.cancel()
                self.start_time = time.time()
    
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(keycode[1])
        if (keycode[1] in self.keys 
            and self.inner_counter + 1 >= len(self.content[self.counter])
            and len(self.log) < len(self.content)):

            if self.counter + 1 >= len(self.content):
                sm.current = 'start'
                return True

            is_true = keycode[1] in self.true_keys
            dt = time.time() - self.start_time
            self.log.append((is_true, dt))

            self.counter += 1
            self.inner_counter = 0
            self.interval = Clock.schedule_interval(self.update, 2.0)
              
        return True
    
    def on_pre_enter(self):
        paths = {}
        for entry in config['order']:
            paths[entry['name']] = os.path.join(path, 'data', entry['path'])

        self.paths = paths 
        self.counter = 0
        self.inner_counter = 0
        self.content = config['content']

        self.true_keys = {'1', 'numpad1', 'right'}
        self.false_keys = {'0', 'numpad0', 'left'}
        self.keys = self.true_keys | self.false_keys
        self.start_time = time.time()
        self.log = []
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
    
    def on_enter(self):
        self.interval = Clock.schedule_interval(self.update, 2.0)
        
    def on_leave(self):
        log_data = []
        correct_count = 0
        for i in range(len(self.log)):
            is_true, dt = self.log[i]
            if is_true:
                correct_count += 1
            log_data.append({
                'resposta': 'certo' if is_true else 'errado',
                'time': dt
            })

        data = get_data(log_data, correct_count)

        import pprint
        pprint.pprint(data)

        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self.interval.cancel()


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