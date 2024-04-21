import kivy
from kivy.app import App
from kivy.lang import Builder

KV = '''
'''

class MyApp(App):
    def build(self):
        return Builder.load_string(KV)
MyApp().run()

