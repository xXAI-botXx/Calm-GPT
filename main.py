# imports
import sys
sys.path.insert(0, './chat_bot')
from bot import Calm_Bot

import threading

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

class User_Input(MDCard):
    text = StringProperty()
    font_size = NumericProperty()

class Bot_Response(MDCard):
    text = StringProperty()
    font_size = NumericProperty()   

class Chat(Screen):
    chat_area = ObjectProperty()
    message = ObjectProperty()

    def __init__(self, **kwargs):
        super(Chat, self).__init__(**kwargs)
        self.bot_loaded = False
        self.bot_is_loading_answer = False
        self.limit_length = 20
        self.min_width = 40

    def load_bot(self):
        self.bot = Calm_Bot("./chat_bot/weights/model_state_V5_6.pt")
        print("model loaded")
        self.bot_loaded = True

    def send_message(self):
        if self.bot_is_loading_answer == False and self.bot_loaded == True:
            self.user_input = self.ids.user_message.text
            length = len(self.user_input)

            if length > 0 and length <= 1024:
                self.ids.user_message.text = ""
                length += len(self.user_input.split("\n"))*self.limit_length
                if length >= self.limit_length:
                    self.ids.chat_area.add_widget(
                        User_Input(text=self.user_input, font_size=17, height=length)
                    )
                else:
                    self.ids.chat_area.add_widget(
                        User_Input(text=self.user_input, font_size=17)
                    )
                self.ids.chat_scroll_view.scroll_y = 0
            else:
                self.user_input = None

    def bot_response(self):
        self.bot_is_loading_answer = True
        self.bot_response_msg = Bot_Response(text="let me think...", font_size=17)
        self.ids.chat_area.add_widget(self.bot_response_msg)
        self.ids.chat_scroll_view.scroll_y = 0
        threading.Thread(target=self.bot_response_post, daemon=True).start()

    def bot_response_post(self):
        if type(self.user_input) == str and len(self.user_input) > 0:
            response = self.bot.inference(self.user_input)
            self.bot_response_msg.text = response
            length = len(response)
            length += len(self.user_input.split("\n"))*self.limit_length
            if length > self.limit_length:
                self.bot_response_msg.height = length

        self.bot_is_loading_answer = False
        self.ids.chat_scroll_view.scroll_y = 0

class Chat_App(MDApp):

    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Teal"
        self.chat = Chat(name="chat")
        threading.Thread(target=self.chat.load_bot, daemon=True).start()
        screen_manager = ScreenManager()
        screen_manager.add_widget(self.chat)
        return screen_manager



if __name__ == "__main__":
    Chat_App().run()

