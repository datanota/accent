
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.utils import get_color_from_hex
import webbrowser
import datetime
import os


class Common:
    def __init__(self):
        # TODO for next version: add docstring to functions in this module
        self.project_path = os.getcwd().split('accent')[0]
        self.season_screen, self.board_screen = 'seasons_screen', 'board_screen'
        self.random_colors, self.final_board_colors, self.on_board_colors = [], [], []
        self.chosen_season_color = '000000'
        self.chosen_style, self.style_list = 'default', ['default', 'masonry', 'twin', 'graded', 'quilt', 'raw', 'paradox']
        self.given_board_nm, self.given_border_width, self.board_border_background = '', 0, [1, 1, 1, 1]
        self.given_colors, self.all_colors = [], []

# ############################################################### window screenshot

    @staticmethod
    def accent_window_ss(img_nm):
        Window.screenshot(name=img_nm)

# ############################################################### current year

    @staticmethod
    def get_current_year(additional_text):
        current_year = datetime.datetime.now().year
        if additional_text == '':
            returned_year = current_year
        else:
            returned_year = f'{current_year} {additional_text}'
        return returned_year

# ############################################################### path to assets

    def get_assets_path(self, additional_path):
        assets_path = f'{self.project_path}accent/assets/'
        if additional_path == '':
            returned_path = assets_path
        else:
            returned_path = f'{assets_path}{additional_path}'
        return returned_path

# ############################################################## demo

    @staticmethod
    def accent_demo():
        webbrowser.open('https://www.datanota.com/accent')

# ############################################################## window settings

    def window_size_settings(self, window_button):
        dropdown = DropDown()
        for size in ['default', 'large']:
            btn = Button(text=size, size_hint_y=None, height=60)
            btn.bind(on_release=lambda x: self.selected_window_size(window_button, x.text, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(window_button)

    @staticmethod
    def selected_window_size(window_button, text, dropdown):
        window_button.text = text
        if text == 'large':
            Window.size = (1200, 800)
            Window.top = 60
            Window.left = 200
        else:
            Window.size = (800, 600)
        dropdown.dismiss()

# ############################################################## style drop-down

    def style_settings(self, style_button):
        dropdown = DropDown()
        for style in self.style_list:
            btn = Button(text=style, size_hint_y=None, height=60)
            btn.bind(on_release=lambda x: self.selected_style(style_button, x.text, dropdown))
            dropdown.add_widget(btn)
        dropdown.open(style_button)

    def selected_style(self, style_button, text, dropdown):
        style_button.text = text
        self.chosen_style = style_button.text
        dropdown.dismiss()

# ############################################################### color hex sanity/ quality check

    def given_color_choices(self, gc):
        """
        :param gc:
            - list of hex colors given in settings tab of season screen
        :return:
            - processed and cleaned list of given_colors
        """
        given_colors = []
        gc_list = gc.split(',')
        for color in gc_list:
            color = self.color_hex_sanity_check(color)
            if len(color) > 0:
                rgba_given_color = get_color_from_hex(color)
                given_colors.append(rgba_given_color)
            else:
                given_colors = self.final_board_colors
        return given_colors

    @staticmethod
    def color_hex_sanity_check(hex_color):
        hex_color = hex_color.strip()
        if len(hex_color) != 6:
            hex_color = ''
        return hex_color

# ############################################################### border condition

    @staticmethod
    def border_choice(w):
        if len(w) == 0:
            border_width = 0
        else:
            border_width = int(w)
        return border_width



