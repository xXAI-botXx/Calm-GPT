import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class ChatBot(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatBot, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.history = ScrollView(size_hint=(1, 0.9), bar_color=[0.7,0.7,0.7,0.7], bar_inactive_color=[0.7,0.7,0.7,0.7])
        self.conversation = BoxLayout(orientation='vertical', size_hint_y=None)
        self.conversation.bind(minimum_height=self.conversation.setter('height'))
        self.history.add_widget(self.conversation)
        self.add_widget(self.history)
        self.new_message = TextInput(size_hint=(1, 0.1), multiline=False, hint_text="Type your message here...", background_color=[0.8,0.8,0.8,1])
        self.new_message.bind(on_text_validate=self.send_message)
        self.add_widget(self.new_message)
        self.clear_button = Button(text='Clear', size_hint=(1, 0.1), background_color=[0.6,0.6,0.6,1], color=[1,1,1,1])
        self.clear_button.bind(on_press=self.clear_history)
        self.add_widget(self.clear_button)

    def send_message(self, *args):
        message = self.new_message.text
        if len(message.split()) <= 1024:
            self.conversation.add_widget(Label(text='User: ' + message, color=[0,0,0,1]))
            self.new_message.text = ''
            bot_response = 'Bot: ' + 'I am a bot, I respond to everything!'
            self.conversation.add_widget(Label(text=bot_response, color=[0,0,0,1]))
        else:
            self.conversation.add_widget(Label(text='Error: Message exceeds 1024 words limit', color=[1,0,0,1]))

    def clear_history(self, *args):
        self.conversation.clear_widgets()

class ChatApp(App):
    def build(self):
        chat = ChatBot()
        Window.clearcolor = (0.5, 0, 0.5, 1)
        return chat

if __name__ == '__main__':
    ChatApp().run()
