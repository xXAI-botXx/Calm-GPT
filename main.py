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
from kivymd.uix.menu import MDDropdownMenu
from kivymd.toast import toast

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
        self.path_history = "./chat_bot/histories"

        self.menu_items = []
        self.menu = MDDropdownMenu(
            caller = self.ids.menu_button,
            items = self.menu_items,
            width_mult = 5
        )
        self.load_history()

    def menu_callback(self, text_item):
        if self.bot_is_loading_answer == False:
            self.bot.load_history(path=self.path_history, name=text_item)
            self.cur_chat_name = text_item
            histories = self.bot.get_history(path=self.path_history, name=text_item)
            self.ids.chat_scroll_view.scroll_y = 1
            self.ids.chat_area.clear_widgets()
            for idx, message in enumerate(histories):
                length = len(message)
                length += (len(message.split("\n"))-1) *self.limit_length
                if idx % 2 == 0:
                    if length >= self.limit_length:
                        self.ids.chat_area.add_widget(User_Input(text=message, font_size=17, height=length + 50))
                    else:
                        self.ids.chat_area.add_widget(User_Input(text=message, font_size=17))
                    self.bot.add_to_history(is_user=True, message=message)
                else:
                    if length > self.limit_length:
                        self.ids.chat_area.add_widget(Bot_Response(text=message, font_size=17, height=length + 50))
                    else:
                        self.ids.chat_area.add_widget(Bot_Response(text=message, font_size=17))
                    self.bot.add_to_history(is_user=False, message=message)
                self.ids.chat_scroll_view.scroll_y = 0
            # if last message is from user
            if idx % 2 == 0:
                self.user_input = message
                self.bot_response()
        else:
            self.show_toast("Please wait until the bot is finish answering.")

    def load_history(self):
        histories = self.bot.load_histories(path=self.path_history)
        for history_name in histories:
            self.add_menu_item(history_name)
        self.cur_chat_name = None

    def add_menu_item(self, text):
        new_item = {'text': text, 
                    'viewclass': 'OneLineListItem',
                    'on_release': lambda x=text: self.menu_callback(x)}
        self.menu.items.append(new_item)

    def save_history(self, toast=True):
        if type(self.cur_chat_name) == type(None):
            name = self.bot.save_history(path="./chat_bot/histories")
            if name.endswith(".txt"):
                name = ".".join(name.split(".")[:-1])
            self.cur_chat_name = name
            self.add_menu_item(self.cur_chat_name)
        else:
            self.bot.save_history(path="./chat_bot/histories", name=self.cur_chat_name, override=True)
        
        if toast:
            self.show_toast("Your chat has been saved!", duration=1)

    def new_chat(self):
        if type(self.cur_chat_name) != type(None) and self.bot_is_loading_answer == False:
            self.bot.reload()
            self.cur_chat_name = None
            self.ids.chat_scroll_view.scroll_y = 1
            self.ids.chat_area.clear_widgets()
            self.ids.chat_scroll_view.scroll_y = 0
            # reload menu
            self.menu.items = []
            self.load_history()

        if self.bot_is_loading_answer:
            self.show_toast("Please wait until the bot is finish answering.")

    def del_chat(self):
        if type(self.cur_chat_name) != type(None) and self.bot_is_loading_answer == False:
            self.bot.del_history(path=self.path_history, name=self.cur_chat_name)
            self.bot.reload()
            self.cur_chat_name = None
            self.ids.chat_scroll_view.scroll_y = 1
            self.ids.chat_area.clear_widgets()
            self.ids.chat_scroll_view.scroll_y = 0

            # reload menu
            self.menu.items = []
            self.load_history()

        if self.bot_is_loading_answer:
            self.show_toast("Please wait until the bot is finish answering.")

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
                self.bot.add_to_history(is_user=True, message=self.user_input)
                self.save_history()
            else:
                self.user_input = None
                
            if length <= 0:
                self.show_toast("You have to type something.")
            elif length > 1024:
                self.show_toast("You wrote too much.")
        else:
            self.show_toast("Please wait until the bot is finish answering.")

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
            length += (len(response.split("\n"))-1)*self.limit_length
            if length > self.limit_length:
                self.bot_response_msg.height = length + 50

            self.bot_is_loading_answer = False
            self.ids.chat_scroll_view.scroll_y = 0
            self.receive_sound()
            self.bot.add_to_history(is_user=False, message=response)
            self.save_history(toast=False)

    def stop_music(self):
        if self.app.stop_music == False:
            self.ids.music_button.icon = "speaker-play"  #disc-player
            self.app.stop_bg_music()
        else:
            self.ids.music_button.icon = "speaker-pause"  
            self.app.start_bg_music()

    def set_play_symbol(self):
        self.ids.music_button.icon = "speaker-pause"

    def set_pause_symbol(self):
        self.ids.music_button.icon = "speaker-play"

    def next_music(self):
        self.app.next_bg_music(should_play=True)

    def send_sound(self):
        sound = SoundLoader.load("./res/send.mp3")
        sound.play()

    def receive_sound(self, sleep=0):
        time.sleep(sleep)
        sound = SoundLoader.load("./res/receive.mp3")
        sound.play()

    def show_toast(self, text, duration=2):
        toast(text, duration=duration)

    # def toggle_menu(self):
    #     menu_scroll = self.ids.menu_scroll
    #     dropdown_menu = self.ids.dropdown_menu

    #     if menu_scroll.height == 0:
    #         menu_scroll.height = dropdown_menu.height
    #     else:
    #         menu_scroll.height = 0

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

    def __init__(self, mute, model_version, dir_path, **kwargs):
        super(Chat_App, self).__init__(**kwargs)
        self.mute = mute
        self.model_version = model_version
        self.dir_path = dir_path

    def build(self):
        self.title = 'Calm Chat'
        self.icon = 'logo.jpeg'

        self.screen_manager = ScreenManager()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Cyan"
        self.theme_cls.accent_palette = "Orange"
        # ['Red', 'Pink', 'Purple', 'DeepPurple', 'Indigo', 'Blue', 'LightBlue', 'Cyan', 'Teal', 'Green', 'LightGreen', 'Lime', 'Yellow', 'Amber', 'Orange', 'DeepOrange', 'Brown', 'Gray', 'BlueGray']

        threading.Thread(target=self.load_bot, daemon=True).start()

        Window.minimum_width = 200
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
        if self.mute == False:
            self.sound.play()
        self.screen_intro = Intro_Screen(self, name="intro")
        self.screen_manager.add_widget(self.screen_intro)
        self.intro_finish = False

    def load_bot(self):
        self.bot_loaded = False
        self.bot = Calm_Bot(model_version=self.model_version, dir_path=self.dir_path)
        print("model loaded")
        self.bot_loaded = True

    def load_chat(self):
        self.intro_finish = True
        if self.sound:
            self.sound.stop()

        while self.bot_loaded == False:
            toast("Loading GPT-2 model...please wait a moment...", duration=0.5)
            time.sleep(0.5)
        self.chat = Chat(self, self.bot, name="chat")
        self.screen_manager.add_widget(self.chat)

    def start_bg_music(self):
        if self.music_started == False:
            # only visited once by start
            self.sound = SoundLoader.load(f"{self.music_path}/{self.music[self.music_idx]}")
            self.sound.bind(on_stop=self.next_bg_music)
            self.music_started = True
            if self.mute:
                self.chat.set_pause_symbol()
                self.stop_music = True
            else:
                self.sound.play()
                self.stop_music = False
        else:
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
    Chat_App(mute=False, model_version="V6_8", dir_path="./chat_bot").run()


