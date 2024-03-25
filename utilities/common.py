
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from functools import partial
import webbrowser
import datetime
import random
import os


class Common:
    def __init__(self):
        self.project_path = os.getcwd().split('accent')[0]
        self.app_nm = 'ACCENT'
        self.season_color = '000000'
        self.final_colors = ['B4B4B4']
        self.color_order = 'n'
        self.given_added_color_list = [self.season_color]
        self.board_nm = 'random'

# ############################################################### screenshot

    @staticmethod
    def accent_ss():
        img_nm = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        Window.screenshot(name=img_nm + '.png')

# ############################################################## demo

    @staticmethod
    def dn_sage_demo():
        webbrowser.open('https://www.datanota.com/accent')

# ############################################################### navbar top-right tip

    @staticmethod
    def tip_dialog(*args):
        title = args[0]
        tip = args[1]
        dialog = MDDialog(
            title=title,
            text='[color=222222]' + tip,
            buttons=[
                MDFlatButton(
                    text='Dismiss',
                    theme_text_color='Custom',
                    text_color=args[2],
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

# ############################################################### window size

    @staticmethod
    def window_size_settings(size):
        if size == 'large':
            Window.size = (1200, 800)
            Window.top = 60
            Window.left = 200
        else:
            Window.size = (800, 600)

# ############################################################### color hex sanity/ quality check

    @staticmethod
    def color_hex_sanity_check(hex_color):
        hex_color = hex_color.strip()
        if len(hex_color) != 6:
            hex_color = ''
        return hex_color

# ############################################################### boards generic layout

    def get_generic_layout(self, orientation, spacing, size_hint, b_size_list, color_order):
        li = BoxLayout(orientation=orientation, spacing=spacing, size_hint=size_hint)
        for size in b_size_list:
            if self.color_order == 'y':
                background_color = color_order
            else:
                background_color = random.choices(self.final_colors, k=1)[0]
            lbi = Button(
                background_color=background_color, background_normal='', size_hint=size)
            lbi.bind(on_press=partial(self.revise_board_colors, lbi))
            li.add_widget(lbi)
        return li

    def revise_board_colors(self,  *args):
        btn = args[0]
        customized_colors = self.given_added_color_list if len(self.given_added_color_list) != 0 else self.final_colors
        btn.background_color = random.choices(customized_colors, k=1)[0]
