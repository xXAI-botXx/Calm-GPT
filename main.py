# imports
import sys
sys.path.insert(0, './chat_bot')
from bot import Calm_Bot

import os
import random
import time

import threading

from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.card import MDCard
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.animation import Animation

# dark green: #3e6465
# dust: #ddcdab
# dirt: #9d8c67
# sky: #67acc8
# cloudysky: #a0cad4
# dark: #232128
# water_blue: #71a0a7
# orange: #c45c2a
# brown: #643e26

class Intro_Screen(Screen):
    def __init__(self, app, **kwargs):
        super(Intro_Screen, self).__init__(**kwargs)
        self.app = app

    def release_action(self):
        self.app.load_chat()
        self.app.start_bg_music()
        self.parent.remove_widget(self)
    

class User_Input(MDCard):
    text = StringProperty()
    font_size = NumericProperty()

class Bot_Response(MDCard):
    text = StringProperty()
    font_size = NumericProperty()   

class Chat(Screen):
    chat_area = ObjectProperty()
    message = ObjectProperty()
    music_button = ObjectProperty()
    bg_button = ObjectProperty()
    bg_img = ObjectProperty()

    # data = {
    #     'Standard': 'language-python',
    #     'Color Gradient': 'language-php',
    #     'Wallpaper': 'language-php',
    #     'Snow': 'language-cpp',
    #     'Rain': 'language-cpp'
    # }

    def __init__(self, app, bot, **kwargs):
        super(Chat, self).__init__(**kwargs)
        self.app = app
        self.bot = bot
        self.bot_loaded = False
        self.bot_is_loading_answer = False
        self.limit_length = 30
        self.min_width = 40

    def send_message(self):
        if self.bot_is_loading_answer == False:
            self.user_input = self.ids.user_message.text
            length = len(self.user_input)

            if length > 0 and length <= 1024:
                self.ids.user_message.text = ""
                length += (len(self.user_input.split("\n"))-1) *self.limit_length
                if length >= self.limit_length:
                    self.ids.chat_area.add_widget(
                        User_Input(text=self.user_input, font_size=17, height=length + 50)
                    )
                else:
                    self.ids.chat_area.add_widget(
                        User_Input(text=self.user_input, font_size=17)
                    )
                self.ids.chat_scroll_view.scroll_y = 0
                self.send_sound()
            else:
                self.user_input = None

    def bot_response(self):
        if self.bot_is_loading_answer == False and type(self.user_input) == str and len(self.user_input) > 0:
            self.bot_is_loading_answer = True
            self.bot_response_msg = Bot_Response(text="let me think...", font_size=17)
            self.ids.chat_area.add_widget(self.bot_response_msg)
            self.ids.chat_scroll_view.scroll_y = 0
            
            threading.Thread(target=lambda:self.receive_sound(sleep=1), daemon=True).start()
            threading.Thread(target=self.bot_response_post, daemon=True).start()

    def bot_response_post(self):
        if type(self.user_input) == str and len(self.user_input) > 0:
            response = self.bot.inference(self.user_input)
            self.bot_response_msg.text = response
            length = len(response)
            length += (len(self.user_input.split("\n"))-1)*self.limit_length
            if length > self.limit_length:
                self.bot_response_msg.height = length + 50

        self.bot_is_loading_answer = False
        self.ids.chat_scroll_view.scroll_y = 0
        self.receive_sound()

    def stop_music(self):
        if self.app.stop_music == False:
            self.ids.music_button.icon = "speaker-play"  #disc-player
            self.app.stop_bg_music()
        else:
            self.ids.music_button.icon = "speaker-pause"  
            self.app.start_bg_music()

    def set_play_symbol(self):
        self.ids.music_button.icon = "speaker-pause"

    def next_music(self):
        self.app.next_bg_music(should_play=True)

    def send_sound(self):
        sound = SoundLoader.load("./res/send.mp3")
        sound.play()

    def receive_sound(self, sleep=0):
        time.sleep(sleep)
        sound = SoundLoader.load("./res/receive.mp3")
        sound.play()

    # def animate_color_change(self, pressed=True, *args):
    #     screen = self.root.ids.bg_img
    #     anim_duration = 5
    #     anim = Animation(color=[random.random(), random.random(), random.random(), 1], duration=anim_duration)
    #     anim.bind(on_complete=self.animate_color_change)
    #     anim.start(screen)
    #     #on_release: root.animate_color_change(True)
    #     Image:
    #         id: bg_img
    #         source: './logo.jpeg'
    #         allow_stretch: True

class Chat_App(MDApp):

    def build(self):
        self.title = 'Calm Chat'
        self.icon = 'logo.jpeg'

        self.screen_manager = ScreenManager()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "Orange"
        # ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

        threading.Thread(target=self.load_bot, daemon=True).start()

        Window.minimum_width = 500
        Window.minimum_height = 400

        self.load_music()
        self.load_intro()
        return self.screen_manager

    def load_music(self):
        self.music_path = "./res/bg_music"
        self.music = os.listdir(self.music_path)
        self.music_intro = "./res/intro.mp3"
        self.shuffle_playlist()
        self.music_idx = 0
        self.music_started = False
        self.stop_music = False

    def shuffle_playlist(self):
        random.shuffle(self.music)

    def load_intro(self):
        self.sound = SoundLoader.load(self.music_intro)
        self.sound.bind(on_stop=lambda x:self.next_bg_music(x, intro=True))
        self.sound.play()
        self.screen_intro = Intro_Screen(self, name="intro")
        self.screen_manager.add_widget(self.screen_intro)
        self.intro_finish = False

    def load_bot(self):
        self.bot_loaded = False
        self.bot = Calm_Bot("./chat_bot/weights/model_state_V5_6.pt")
        print("model loaded")
        self.bot_loaded = True

    def load_chat(self):
        self.intro_finish = True
        if self.sound:
            self.sound.stop()

        while self.bot_loaded == False:
            time.sleep(0.5)
        self.chat = Chat(self, self.bot, name="chat")
        self.screen_manager.add_widget(self.chat)

    def start_bg_music(self):
        if self.music_started == False:
            self.sound = SoundLoader.load(f"{self.music_path}/{self.music[self.music_idx]}")
            self.music_started = True
            self.sound.bind(on_stop=self.next_bg_music)
        self.sound.play()
        self.stop_music = False

    def stop_bg_music(self):
        self.stop_music = True
        self.sound.stop()

    def next_bg_music(self, t=None, should_play=False, intro=False):
        if (self.stop_music == False or should_play == True) and intro == False:
            self.sound.stop()
            self.stop_music = False
            self.chat.set_play_symbol()
            self.music_idx += 1
            if self.music_idx >= len(self.music):
                self.music_idx = 0
            self.sound = SoundLoader.load(f"{self.music_path}/{self.music[self.music_idx]}")
            self.sound.bind(on_stop=self.next_bg_music)
            self.sound.play()
        elif intro == True and self.intro_finish == False:
            self.sound = SoundLoader.load(self.music_intro)
            self.sound.bind(on_stop=lambda x:self.next_bg_music(x, intro=True))
            self.sound.play()

if __name__ == "__main__":
    Chat_App().run()

