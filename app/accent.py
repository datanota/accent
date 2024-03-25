
from utilities.analytics import Analytics
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
import datetime
from functools import partial
import random
import csv


class AccentContent(BoxLayout):
    pass


class Seasons(Screen):
    pass


class Colors(Screen):
    pass


class Styles(Screen):
    pass


class Board(Screen):
    pass


class AccentApp(MDApp, Analytics):
    """
    There are 2 choices:
        1. random (all is done randomly: from color choices to board style)
        2. seasons (step-by-step customization)
    """
    def __init__(self):
        super().__init__()
        self.random_colors = ['000000']
        self.chosen_season_colors = ['FFFFFF']
        self.col_dict = self.get_season_col_dict()
        self.col_hex = [item for sublist in self.col_dict.values() for item in sublist]
        self.given_board_nm = ''
        self.given_style = 'default'
        self.given_border_width = 0
        self.rect = None

# ############################################################## seasons screen

    def accent_season_palette(self, x):
        self.root.ids.screen_manager.current = x
        for i in range(50):
            btn = Button(
                text=self.col_hex[i], color='BD9D74', background_color=self.col_hex[i],
                background_normal='', size_hint=(1 / 5, 1 / 10)
            )
            btn.bind(on_press=partial(self.color_is_chosen, self.col_hex[i], x))
            self.root.ids.screen_manager.get_screen(x).ids.season_palette.add_widget(btn)

    def color_is_chosen(self, *args):
        self.season_color = args[0]
        screen_x = args[1]
        self.root.ids.screen_manager.get_screen(screen_x).ids.chosen_colors.clear_widgets()
        btn = Button(background_color=self.season_color, background_normal='', size_hint=(1 / 3, 1))
        self.root.ids.screen_manager.get_screen(screen_x).ids.chosen_colors.add_widget(btn)
        self.season_color = self.season_color

    def seasons_color_selected(self, x):
        self.root.ids.screen_manager.current = x
        self.root.ids.screen_manager.get_screen(x).ids.colors_initial_color.clear_widgets()
        self.root.ids.screen_manager.get_screen(x).ids.colors_screen_random_colors.clear_widgets()
        self.root.ids.screen_manager.get_screen(x).ids.final_colors.clear_widgets()
        btn = Button(background_color=self.season_color, background_normal='')
        # btn.bind(on_press=partial(self.colors_screen_add_final_colors, x, btn, 1))
        self.root.ids.screen_manager.get_screen(x).ids.colors_initial_color.add_widget(btn)

# ############################################################## colors screen

    def show_colors_screen_random_colors(self, x):
        self.root.ids.screen_manager.get_screen(x).ids.colors_screen_random_colors.clear_widgets()
        self.random_colors = []
        for num in range(5):
            rgb_dict = {
                'high': random.sample(range(200, 255), 1)[0],
                'medium': random.sample(range(50, 200), 1)[0],
                'low': random.sample(range(50), 1)[0]
            }
            rgb_color = [rgb_dict.get(random.choices(list(rgb_dict.keys()), k=1)[0]) / 255 for i in range(3)]
            self.random_colors = rgb_color
            btn = Button(
                text='', background_color=rgb_color,
                background_normal=''
            )
            btn.bind(on_press=partial(self.colors_screen_add_final_colors, x, btn, 0))
            self.root.ids.screen_manager.get_screen(x).ids.colors_screen_random_colors.add_widget(btn)

    def colors_screen_add_final_colors(self, *args):
        if args[2] == 1:
            self.root.ids.screen_manager.get_screen(args[0]).ids.colors_initial_color.remove_widget(args[1])
        else:
            self.root.ids.screen_manager.get_screen(args[0]).ids.colors_screen_random_colors.remove_widget(args[1])
        self.root.ids.screen_manager.get_screen(args[0]).ids.final_colors.add_widget(args[1])
        self.final_colors.append(args[1].background_color)

    def colors_screen_show_styles(self, x):
        self.root.ids.screen_manager.get_screen(x).ids.board_colors.clear_widgets()
        self.root.ids.screen_manager.current = x
        for color in self.final_colors:
            btn = Button(background_color=color, background_normal='')
            self.root.ids.screen_manager.get_screen(x).ids.board_colors.add_widget(btn)

# ############################################################## styles screen

    def styles_screen_next(self, x):
        self.root.ids.screen_manager.current = 'board_screen'
        self.given_board_nm = self.root.ids.screen_manager.get_screen(x).ids.board_given_name.text
        given_style = self.root.ids.screen_manager.get_screen(x).ids.board_given_style.text.strip().lower()
        self.given_style = self.style_choice(given_style)
        given_border_width = self.root.ids.screen_manager.get_screen(x).ids.board_given_border_width.text.strip()
        self.given_border_width = self.border_choice(given_border_width)
        given_added_colors = self.root.ids.screen_manager.get_screen(x).ids.board_added_colors.text.strip()
        self.given_added_color_list = self.added_color_choices(given_added_colors)

    def style_choice(self, s):
        if len(s) == 0:
            style = self.given_style
        else:
            style = s
        return style

    @staticmethod
    def border_choice(w):
        if len(w) == 0:
            border_width = 0
        else:
            border_width = int(w)
        return border_width

    def added_color_choices(self, ac):
        added_colors = []
        ac_list = ac.split(',')
        for color in ac_list:
            color = self.color_hex_sanity_check(color)
            if len(color) > 0:
                added_colors.append(color)
        added_colors = [self.season_color] + added_colors
        return added_colors

# ############################################################## board screen

    def create_board(self, x):
        self.root.ids.screen_manager.current = x
        self.root.ids.screen_manager.get_screen(x).ids.board_layout.clear_widgets()
        with self.root.ids.screen_manager.get_screen(x).ids.board_layout.canvas.before:
            Color(
                tuple(get_color_from_hex(self.season_color))[0],
                tuple(get_color_from_hex(self.season_color))[1],
                tuple(get_color_from_hex(self.season_color))[2]
            )
            self.rect = Rectangle(
                size=self.root.ids.screen_manager.get_screen(x).ids.board_layout.size,
                pos=self.root.ids.screen_manager.get_screen(x).ids.board_layout.pos
            )
        self.root.ids.screen_manager.get_screen(x).ids.board_layout.bind(pos=self.update_rect, size=self.update_rect)
        ll = self.get_style_layout(given_style=self.given_style, given_border_width=self.given_border_width)
        self.root.ids.screen_manager.get_screen(x).ids.board_layout.add_widget(ll)

    def update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos

# ############################################################## generic

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def accent_mood_board_ss(self):
        img_date = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        img_nm = f'../images/accent_saved_board_{img_date}.png'
        self.root.ids.board_canvas.export_to_png(img_nm, quality=100)

    def accent_board_ss(self, x):
        img_time = datetime.datetime.now().strftime('%Y_%m%d%H%M')
        img_path = f'{self.project_path }/accent/images/'
        self.root.ids.screen_manager.get_screen(x).ids.board_layout.export_to_png(f"{img_path}/{self.given_board_nm}_{img_time}.png", quality=100)
        new_data = {'date': img_time, 'board_given_name': self.given_board_nm, 'board_colors': self.final_colors}
        with open(f'{img_path}accent_board_db.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(new_data.keys()))
            writer.writerow(new_data)
            print(f'==================> saved: {new_data}')

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Datanota - ACCENT'
        return AccentContent()


if __name__ == '__main__':
    AccentApp().run()



