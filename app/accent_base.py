
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, Triangle, Line
import webbrowser
import datetime
import random
import os


class AccentBase:
    def __init__(self):
        self.project_path = os.getcwd().split('accent')[0]
        self.random_colors, self.on_board_colors = [], []
        self.selected_season_color, self.seed_color, self.given_colors = '000000', [], []

# ############################################################### window screenshot

    @staticmethod
    def accent_window_ss(img_path_nm):
        Window.screenshot(name=img_path_nm)

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

# ############################################################### color hex sanity/ quality check

    def given_color_choices(self, gc):
        given_colors = []
        gc_list = gc.split(',')
        for color in gc_list:
            color = self.color_hex_sanity_check(color)
            if len(color) > 0:
                given_colors.append(color)
        return given_colors

    @staticmethod
    def color_hex_sanity_check(hex_color):
        hex_color = hex_color.replace('#', '').strip()
        if len(hex_color) != 6:
            hex_color = ''
        return hex_color

# ################################################ seasons color dictionary

    @staticmethod
    def get_season_col_dict():
        """
        - Datanota Accent seasons colors
        """
        col_dict = {
            'vermilion': ['DFA6A5', 'FF7D7D', 'FF2200', 'CB1212', 'FFFFFF'],
            'orange': ['D9C2A3', 'FFD5A5', 'FF9230', 'C25F17', 'E6E6E6'],
            'amber': ['B8B788', 'F9FDB7', 'FFD509', 'A48B19', 'CDCDCD'],
            'green': ['AFD997', 'D3FFA4', '85D910', '868600', 'B4B4B4'],
            'chartreuse': ['B8ECDC', '95F4D4', '13F793', '049254', '9B9B9B'],
            'teal': ['BDFCF7', '81FDF4', '26E0D3', '1F7C76', '828282'],
            'cyan': ['93D6DA', '55F4FD', '01CDE0', '00A2AE', '696969'],
            'indigo': ['91AAC4', 'A4D4FF', '1289FF', '054B9C', '505050'],
            'violet': ['BCA4D2', 'CABFFF', '8C20FF', '6935BA', '373737'],
            'magenta': ['D49BB6', 'FFBFE4', 'FF1D98', 'B62570', '000000']
        }
        return col_dict

    def add_shapes(self, top_layer, n, x_lim, y_lim, size_x_lim, size_y_lim):
        for i in range(n):
            shape_container = Widget()
            shape = random.choice(['rectangle', 'ellipse', 'triangle', 'line'])
            with shape_container.canvas:
                color_rgb = random.choice(self.on_board_colors)
                color_rgb[-1] = round(random.uniform(0, 1), 2)
                Color(*color_rgb)
                x, y = random.randint(x_lim[0], x_lim[1]), random.randint(y_lim[0], y_lim[1])
                size_x = random.randint(size_x_lim, 1600 - x)
                size_y = random.randint(size_y_lim, 1000 - y)
                if shape == 'rectangle':
                    Rectangle(pos=(x, y), size=(size_x, size_y))
                if shape == 'ellipse':
                    Ellipse(pos=(x, y), size=(size_x, size_y), angle_start=0, angle_end=360)
                if shape == 'triangle':
                    t1_x, t1_y = x, y
                    t2_x, t2_y = random.randint(0, x_lim[0]), random.randint(y_lim[1], 1000)
                    t3_x, t3_y = random.randint(x_lim[1], 1500), random.randint(y_lim[0], 1000)
                    Triangle(points=[t1_x, t1_y, t2_x, t2_y, t3_x, t3_y])
                if (shape == 'line') and (i in range(5)):
                    line_width = random.randint(1, 5)
                    x1, y1 = x, y
                    x2, y2 = random.randint(10, x_lim[0]), random.randint(y_lim[1], 800)
                    x3, y3 = random.randint(x_lim[1], 900), random.randint(y_lim[1], 400)
                    points = [
                        random.choice([x1, x2, x3]), random.choice([y1, y2, y3]),
                        random.choice([x1, x2, x3]), random.choice([y1, y2, y3]),
                        random.choice([x1, x2, x3]), random.choice([y1, y2, y3]),
                        random.choice([x1, x2, x3]), random.choice([y1, y2, y3]),
                    ]
                    Line(points=points, width=line_width)
            top_layer.add_widget(shape_container)
