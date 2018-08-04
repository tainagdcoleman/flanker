import kivy
kivy.require('1.10.1')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout

info = {}
game = 'start'
app = None

def update(key, value):
    global info
    info[key] = value

def start_game(name):
    global app, game
    game = name
    app.update()

class StartWidget(Widget):
    pass

class MyApp(App):
    widget = None

    def update(self): 
        global game, info
        self.widget.clear_widgets()
        if game == 'start':
            self.widget.add_widget(StartWidget())
        else:
            self.widget.add_widget(GridLayout())

    def build(self):
        self.widget = StartWidget()
        return self.widget

app = MyApp()
app.run()