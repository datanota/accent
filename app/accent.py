
from app.accent_base import AccentBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from functools import partial
from kivy.core.window import Window
from kivymd.uix.button import MDFillRoundFlatButton
from kivymd.app import MDApp
import datetime
import random
import csv


class AccentContent(BoxLayout):
    pass


class AccentApp(MDApp, AccentBase):
    def __init__(self):
        super().__init__()
        self.seasons_col_dict = self.get_season_col_dict()
        self.seasons_col_hex = [item for sublist in self.seasons_col_dict.values() for item in sublist]

# ##############################################################
# ############################################################## seasons and settings screens
# ##############################################################

    def populate_season_palette_tab(self):
        """
        - creates 50 seasons buttons, press to select, default #000000
        """
        self.root.ids.screen_manager.current = 'seasons_screen'
        self.root.ids.season_palette.clear_widgets()
        for i in range(50):
            btn = Button(
                text=self.seasons_col_hex[i], color='BD9D74', background_color=self.seasons_col_hex[i],
                background_normal='', size_hint=(1 / 5, 1 / 10)
            )
            btn.bind(on_press=partial(self.season_color_is_selected, self.seasons_col_hex[i]))
            self.root.ids.season_palette.add_widget(btn)

    def season_color_is_selected(self, *args):
        self.selected_season_color = args[0]
        btn = Button(background_color=self.selected_season_color, background_normal='')
        self.root.ids.selected_season_color_widget.clear_widgets()
        self.root.ids.selected_season_color_widget.add_widget(btn)
        self.root.ids.settings_season_color.background_color = self.selected_season_color

    @staticmethod
    def get_color_composition(color_in_hex):
        red = int(color_in_hex[0:2], 16)
        green = int(color_in_hex[2:4], 16)
        blue = int(color_in_hex[4:6], 16)
        return [red, green, blue]

    def generate_random_colors(self):
        self.root.ids.screen_manager.current = 'settings_screen'
        self.root.ids.generated_colors.clear_widgets()
        self.random_colors = []
        self.seed_color = self.get_color_composition(self.selected_season_color)
        dominant_color = max(self.seed_color)
        dominant_rgb = [255 if c == dominant_color else 0 for c in self.seed_color]
        self.random_colors.append(''.join([f'{c:02x}' for c in dominant_rgb]))
        shade_weight = random.choice([0.8, 0.6, 0.3])
        darker = [max(0, int(c * shade_weight)) for c in self.seed_color]
        self.random_colors.append(''.join([f'{c:02x}' for c in darker]))
        tint_weight = random.choice([1.4, 1.6, 1.8])
        lighter = [min(255, int(c * tint_weight)) for c in self.seed_color]
        self.random_colors.append(''.join([f'{c:02x}' for c in lighter]))
        tone_weight = random.choice([128, 80, 20])
        toned = [int((c + tone_weight) / 2) for c in self.seed_color]
        self.random_colors.append(''.join([f'{c:02x}' for c in toned]))
        # self.generated_colors = self.generated_colors + self.random_colors
        for i in range(4):
            btn = Button(text='', background_color=self.random_colors[i], background_normal='')
            btn.bind(on_press=partial(self.pressed_to_select_board_colors, btn))
            self.root.ids.generated_colors.add_widget(btn)

    def pressed_to_select_board_colors(self, *args):
        btn = args[0]
        btn_background_color = btn.background_color
        self.on_board_colors.append(btn_background_color)
        if len(self.on_board_colors) < 9:
            self.root.ids.generated_colors.remove_widget(btn)
            round_btn = MDFillRoundFlatButton(md_bg_color=btn_background_color)
            round_btn.bind(on_press=partial(self.remove_selected_board_colors, round_btn))
            self.root.ids.selected_board_colors.add_widget(round_btn)

    def remove_selected_board_colors(self, *args):
        round_btn = args[0]
        round_btn_background_color = round_btn.md_bg_color
        self.on_board_colors.remove(round_btn_background_color)
        self.root.ids.selected_board_colors.remove_widget(round_btn)

    def add_custom_colors(self):
        self.given_colors = self.given_color_choices(self.root.ids.board_given_colors.text)
        for i in range(len(self.given_colors)):
            btn = Button(text='', background_color=self.given_colors[i], background_normal='')
            btn.bind(on_press=partial(self.pressed_to_select_board_colors, btn))
            self.root.ids.generated_colors.add_widget(btn)

# ##############################################################
# ############################################################## board screen
# ##############################################################

    def create_mood_board(self):
        self.root.ids.screen_manager.current = 'board_screen'
        self.root.ids.board_layout.clear_widgets()
        top_layer = BoxLayout(orientation='horizontal')
        self.add_shapes(
            top_layer=top_layer, n=8, x_lim=[300, 500], y_lim=[10, 200], size_x_lim=100, size_y_lim=40
        )
        self.root.ids.board_layout.add_widget(top_layer)

# ############################################################## save board

    def save_created_board(self):
        img_time = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')
        assets_path = self.get_assets_path('')
        img_nm = f'accent_board_{img_time}.png'
        img_path_nm = f"{assets_path}/{img_nm}"
        self.accent_window_ss(img_path_nm=img_path_nm)
        new_data = {
            'name': img_nm,
            'date': img_time,
            'colors': self.on_board_colors
        }
        with open(f'{assets_path}accent_board_db.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(new_data.keys()))
            writer.writerow(new_data)
            print(f'==================> saved: {new_data}')

# ############################################################## generic

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Datanota - ACCENT - V2.1'
        return AccentContent()


if __name__ == '__main__':
    AccentApp().run()
