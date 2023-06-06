
from utilities.analytics import Analytics
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import webbrowser
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import datetime
from functools import partial
import random


class AccentContent(BoxLayout):
    pass


class AccentApp(MDApp, Analytics):
    def __init__(self):
        super().__init__()
        self.prom_color = '000000'
        self.chosen_colors = []
        self.col_dict = self.get_col_dict()
        self.btn_xy = [[3, 3]]
        self.col_hex = ['AC1717', 'd9381e', 'FF6F00', 'ffc107', 'ffeb3b', '8AF905', '4caf50', '00ffff',
                        '2196f3', '3f51b5', '990099', 'a50062', 'FFFFFF', 'a8a9b4', '808080', '000000']

        self.board_colors = {'background': '', 'highlight': '', 'accent': ''}

# ############################################################## mood-board

    def create_boards(self):
        b = self.board_colors.get('background')
        h = self.board_colors.get('highlight')
        a = self.board_colors.get('accent')
        board_sections = {'board_r1': self.root.ids.board_r1,
                          'board_r2': self.root.ids.board_r2,
                          'board_r3': self.root.ids.board_r3}
        bs_keys = board_sections.keys()
        self.root.ids.screen_manager.current = 'sb'
        for key in bs_keys:
            board_sections.get(key).clear_widgets()
        for key in bs_keys:
            btn_size = [random.choice(list(range(4, 10))), random.choice(list(range(4, 10)))]
            total_pixels = btn_size[0] * btn_size[1]
            for i in range(total_pixels):
                random_btn = Button(
                    background_color=random.choices([b, h, a], weights=(60, 25, 15), k=1)[0],
                    background_normal='',
                    size_hint=(1 / btn_size[0], 1 / btn_size[1])
                )
                board_sections.get(key).add_widget(random_btn)

# ############################################################### navbar top-right tip

    def tip_dialog(self, title, tip):
        dialog = MDDialog(
            title=title,
            text='[color=222222]' + tip,
            buttons=[
                MDFlatButton(
                    text='Dismiss',
                    theme_text_color='Custom',
                    text_color=self.theme_cls.primary_color,
                    on_release=lambda x: dialog.dismiss()
                )
            ],
        )
        dialog.open()

# ############################################################## top navigation left-hand side icons

    def callback_top_nav(self, x):
        self.root.ids.screen_manager.current = x

    def clear_chosen_colors(self):
        self.root.ids.chosen_colors.clear_widgets()
        self.root.ids.board_chosen_colors.clear_widgets()
        self.chosen_colors = []

# ############################################################## palette

    def accent_palette(self, x):
        self.root.ids.screen_manager.current = x
        for i in range(16):
            btn = Button(
                text=self.col_hex[i], color='BD9D74', background_color=self.col_hex[i],
                background_normal='', size_hint=(1/8, 0.5)
            )
            btn.bind(on_press=partial(self.color_is_chosen, self.col_hex[i]))
            self.root.ids.prom_palette.add_widget(btn)

    def color_is_chosen(self, *args):
        self.prom_color = args[0]
        btn = Button(
            text='', color='BD9D74', background_color=self.prom_color,
            background_normal='', size_hint=(1/3, 1)
        )
        self.root.ids.chosen_colors.add_widget(btn)
        self.chosen_colors.append(self.prom_color)

# ############################################################## mood-board color and style buttons

    def mood_board_chosen_colors(self):
        self.root.ids.board_chosen_colors.clear_widgets()
        for col in self.chosen_colors:
            btn = Button(
                text='', color='000000', background_color=col,
                background_normal='', size_hint=(1/3, 1)
            )
            self.root.ids.board_chosen_colors.add_widget(btn)

# ############################################################## color sections

    def create_color_board(self):
        if len(self.chosen_colors) == 0:
            self.callback_top_nav('s1')
        else:
            for key in self.section_ids().keys():
                self.per_section_color_board(key, self.section_ids().get(key)[0])

    def per_section_color_board(self, key, section_id):
        section_id.clear_widgets()
        all_colors_dict = self.get_dark_light_accent_colors(self.chosen_colors)
        btn_size = random.choice(self.btn_xy)
        total_pixels = btn_size[0] * btn_size[1]
        for i in range(total_pixels):
            default_style = random.choice(['light', 'dark'])
            default_color = all_colors_dict.get(default_style)
            btn = Button(
                background_color=random.choice(default_color),
                background_normal='',
                size_hint=(1/btn_size[0], 1/btn_size[1])
            )
            section_id.add_widget(btn)
            btn.bind(on_press=partial(self.section_chosen, key, btn.background_color))

    def section_chosen(self, *args):
        if len(args) == 1:
            key = list(self.section_ids().keys())[args[0]]
            color = self.section_ids().get(key)[2].text
        else:
            key = args[0]
            color = args[1]
        self.section_ids().get(key)[1].clear_widgets()
        btn = Button(text=key, background_normal='', background_color='gray', size_hint=[1, 0.2])
        self.section_ids().get(key)[1].add_widget(btn)
        btn.background_color = color
        self.board_colors[key] = color

    def section_ids(self):
        id_dict = {
            'background': [
                self.root.ids.b_color_board,
                self.root.ids.b_colors,
                self.root.ids.b_hex
            ],
            'highlight': [
                self.root.ids.h_color_board,
                self.root.ids.h_colors,
                self.root.ids.h_hex
            ],
            'accent': [
                self.root.ids.a_color_board,
                self.root.ids.a_colors,
                self.root.ids.a_hex
            ]
        }
        return id_dict

# ############################################################## demo

    def accent_mood_board_ss(self):
        img_date = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        img_nm = f'../images/accent_saved_board_{img_date}.png'
        self.root.ids.board_canvas.export_to_png(img_nm, quality=100)

    @staticmethod
    def accent_ss():
        img_nm = datetime.datetime.now().strftime("%Y_%m%d%H%M_")
        Window.screenshot(name=f'window_{img_nm}.png')

    @staticmethod
    def accent_demo():
        webbrowser.open('https://www.datanota.com/accent')

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        return AccentContent()


if __name__ == '__main__':
    AccentApp().run()



