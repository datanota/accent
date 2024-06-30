
from app.accent_analytics import Analytics
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.button import Button
from kivymd.app import MDApp
from kivy.uix.screenmanager import Screen
import datetime
from functools import partial
import random
import csv


class AccentContent(BoxLayout):
    pass


class AccentSeasons(Screen):
    pass


class AccentBoard(Screen):
    pass


class AccentApp(MDApp, Analytics):

    def __init__(self):
        super().__init__()
        self.col_dict = self.get_season_col_dict()
        self.col_hex = [item for sublist in self.col_dict.values() for item in sublist]
        self.rect = ''

# ##############################################################
# ############################################################## seasons tab
# ##############################################################

    def populate_season_palette_tab(self):
        """
        By clicking the seasons button on the home screen
        :return:
            - creates 50 season-color buttons and populates the season_tab stack_layout
            - when a season color is selected, calls the color_is_chosen function
        """
        self.root.ids.screen_manager.current = self.season_screen
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.season_palette.clear_widgets()
        for i in range(50):
            btn = Button(
                text=self.col_hex[i], color='BD9D74', background_color=self.col_hex[i],
                background_normal='', size_hint=(1 / 5, 1 / 10)
            )
            btn.bind(on_press=partial(self.color_is_chosen, self.col_hex[i]))
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.season_palette.add_widget(btn)

    def color_is_chosen(self, *args):
        """
        By clicking on a season color
        :param args:
            args[0]: season color button background_color
        :return:
            - updates the inherited variable, chosen_season_color
            - adds chosen_season_color on top of the screen to show the selected color
            - updates the finalized colors in settings tab of season screen
        """
        self.chosen_season_color = args[0]
        btn = Button(background_color=self.chosen_season_color, background_normal='')
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.selected_season_color_widget.clear_widgets()
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.selected_season_color_widget.add_widget(btn)
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.finalized_colors_season_color.background_color = self.chosen_season_color

# ##############################################################
# ############################################################## random colors tab
# ##############################################################

    def generate_random_colors(self):
        """
        By clicking the generate_color button in season screen:
        :return:
            - switches to the random tab of season screen
            - clears both inherited random_colors list and random tab of season screen
            - creates 40 randomly generated colors TODO for next version: improve the algorithm
            - updates the inherited list, random_colors
            - any selected random color will show up in the settings tab of season screen
        """
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.tab_panel.switch_to(
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.random_tab
        )
        self.random_colors = []
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.random_colors.clear_widgets()
        for i in range(40):
            rgb_dict = {
                'high': round((random.sample(range(200, 255), 1)[0] / 255), 2),
                'medium': round((random.sample(range(50, 200), 1)[0] / 255), 2),
                'low': round((random.sample(range(50), 1)[0] / 255), 2),
                'opacity': random.sample(range(0, 1), 1)[0]
            }
            rgb_color = [rgb_dict.get(random.choices(list(rgb_dict.keys()), k=1)[0]) for _ in range(4)]
            self.random_colors.append(rgb_color)
            btn = Button(text='', background_color=rgb_color, background_normal='', size_hint=(1/8, 1/5))
            btn.bind(on_press=partial(self.add_to_settings_tab, self.random_colors[i]))
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.random_colors.add_widget(btn)

# ##############################################################
# ############################################################## settings tab
# ##############################################################

    def add_to_settings_tab(self, *args):
        """
        By clicking on random colors in the random tab of season screen
        :param args:
            args[0]: the selected random color
        :return:
            - adds the selected random colors to the inherited list, final_board_colors - does not re-write the list
            - all selected random colors show up in the settings tab of season screen
            - binds the remove_from_settings_tab function to selected random colors
        """
        btn_color = args[0]
        self.final_board_colors.append(btn_color)
        btn = Button(text='', background_color=btn_color, background_normal='')
        btn.bind(on_press=partial(self.remove_from_settings_tab, btn))
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.finalized_colors.add_widget(btn)

    def remove_from_settings_tab(self, *args):
        """
        By clicking on finalized random colors in the settings tab of season screen
        :param args:
            args[0]: the selected color
        :return:
            - removes selected color from the inherited list, final_board_colors
            - removes the color from the settings tab of season screen
        """
        btn = args[0]
        btn_background_color = btn.background_color
        self.final_board_colors.remove(btn_background_color)
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.finalized_colors.remove_widget(btn)

    def transition_to_seasons_tab(self):
        """
        called from the accent_seasons.kv file TODO for next version: minimize the use of kv widgets
        :return:
            - the screen transitions to seasons tab to change selected season color, if needed
        """
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.tab_panel.switch_to(
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.seasons_palette_tab
        )

# ############################################################## custom board

    def custom_board_settings(self):
        """
        By clicking the custom button in home screen
        :return:
            - switches to the settings tab of season screen
        """
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.finalized_colors.clear_widgets()
        self.root.ids.screen_manager.current = self.season_screen
        self.root.ids.screen_manager.get_screen(self.season_screen).ids.tab_panel.switch_to(
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.settings_tab
        )

# ##############################################################
# ############################################################## board screen
# ##############################################################

    def create_mood_board(self):
        """
        By clicking the create_board button in the settings tab of season screen
        :return:
            - all the settings input values are updated by calling the update_settings_inputs function
            - creates a list of given_colors, if any, and final_board_colors, if any
            - updates the final_board_colors list with all_colors and removes duplicates
            - if final_board_colors list is empty, add white to the list as default value
            - if border_width is not zero, calls set_canvas_background_for_border_color function
            - creates the board based on chosen_style from drop_down or settings tab of season screen
            - board style algorithm is implemented in the get_style_layout function
        """
        self.root.ids.screen_manager.current = self.board_screen
        self.root.ids.screen_manager.get_screen(self.board_screen).ids.board_layout.clear_widgets()
        self.update_settings_inputs()
        self.all_colors = self.given_colors + self.final_board_colors
        tuple_unique_colors = set(tuple(x) for x in self.all_colors)
        self.final_board_colors = [list(x) for x in tuple_unique_colors]
        if len(self.final_board_colors) == 0:
            self.final_board_colors = [[1, 1, 1, 1]]
        if self.given_border_width != 0:
            self.board_border_background = random.choice(self.final_board_colors)
            self.set_canvas_background_for_border_color()
        ll = self.get_style_layout()
        self.root.ids.screen_manager.get_screen('board_screen').ids.board_layout.add_widget(ll)

    def update_settings_inputs(self):
        """
        :return:
            - updates the three inherited variables based on input data in settings tab of season screen
            - if no board_name is given, sets the board name as empty string
            - if no border width is given, sets the border width to 0 (e.g. given border width 20, 10)
            - the given color should be in hex format separated by comma (e.g. ffffff, 000000)
            - if no color is given in settings tab of season screen, final_board_colors is used as default
        """
        self.given_board_nm = self.root.ids.screen_manager.get_screen(self.season_screen).ids.board_given_name.text

        self.given_border_width = self.border_choice(
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.board_given_border_width.text
        )
        self.given_colors = self.given_color_choices(
            self.root.ids.screen_manager.get_screen(self.season_screen).ids.board_given_colors.text
        )

    def set_canvas_background_for_border_color(self):
        """
        :return:
            - randomly chooses a color from inherited and updated final_board_colors
            - sets canvas color background (visible only if board has a border)
        """
        with self.root.ids.screen_manager.get_screen(self.board_screen).ids.board_layout.canvas.before:
            Color(
                self.board_border_background[0], self.board_border_background[1],
                self.board_border_background[2], self.board_border_background[3]
            )
            self.rect = Rectangle(
                size=self.root.ids.screen_manager.get_screen(self.board_screen).ids.board_layout.size,
                pos=self.root.ids.screen_manager.get_screen(self.board_screen).ids.board_layout.pos
            )
        self.root.ids.screen_manager.get_screen(self.board_screen).ids.board_layout.bind(
            pos=partial(self.update_rect, self.update_rect)
        )

    def update_rect(self, *args):
        """
        :param args: to update canvas background color for border color
        :return:
        """
        instance = args[0]
        self.rect.size = instance.size
        self.rect.pos = instance.pos

# ############################################################## save board

    def save_created_board(self):
        """
        By clicking the save button on top-navigation bar
        :return:
            - assigns a name to the screenshot based on timestamp and the given_board_name
            - creates a dictionary of board identifiers
            - append the new board data to accent_board_db.csv file
        """
        img_time = datetime.datetime.now().strftime('%Y%m%d_%H%M_%S')
        img_path = self.get_assets_path('')
        img_name = f"{img_path}/{self.given_board_nm}_{img_time}.png"
        self.accent_window_ss(img_nm=img_name)
        new_data = {
            'date': img_time,
            'board_given_name': self.given_board_nm,
            'board_colors': self.final_board_colors
        }
        with open(f'{img_path}accent_board_db.csv', mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=list(new_data.keys()))
            writer.writerow(new_data)
            print(f'==================> saved: {new_data}')

# ############################################################## generic

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.title = 'Datanota - ACCENT'
        return AccentContent()


if __name__ == '__main__':
    AccentApp().run()



