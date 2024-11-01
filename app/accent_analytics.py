
from utilities.common import Common
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from functools import partial
import random


class Analytics(Common):
    def __init__(self):
        super().__init__()

# ################################################ graded style grading color shades

    def get_lighter_shades_list(self, n):
        """
        if selected style is graded
        :param n:
            total grades
        :return:
            - if no color is given in the settings tab of season screen, use final_board_colors as default
            - finds the dominant value in the randomly selected rgb color
            - finds n gradually darker and lighter shades of the color and sort them from light to dark
        """
        graded_color = []
        if len(self.given_colors) != 0:
            graded_color = self.given_colors
        else:
            graded_color = self.final_board_colors
        rgba_color = random.choice(graded_color)
        rgb_color = [rgba_color[0], rgba_color[1], rgba_color[2]]
        dom_color = max(rgb_color)
        dom_position = rgb_color.index(dom_color)
        s = 255/dom_color
        final_colors = []
        for i in range(1, n + 1):
            adjustment_factor = 1 + (s - 1) * (i / n)
            new_shade = tuple(min(int(component * adjustment_factor), 255)/255 for component in rgb_color)
            final_colors.append(new_shade)
        sorted_final_colors = sorted(final_colors, key=lambda x: x[dom_position], reverse=True)
        return sorted_final_colors

# ################################################ styles

    def get_style_layout(self):
        """
        By clicking on either create_board button or re-run button
        :return:
            - based on chosen_style, populates the board
            - chosen_style sample images are posted on README file
        """
        ll = None
        if self.chosen_style == 'default':
            ll = GridLayout(cols=3, spacing=self.given_border_width)
            ll.add_widget(self.get_generic_layout('vertical', [1, 1], [(1, 1/4), (1, 3/4)]))
            ll.add_widget(self.get_generic_layout('vertical', [1, 1], [(1, 1/5), (1, 3/5), (1, 1/5)]))
            ll.add_widget(self.get_generic_layout('vertical', [1, 1], [(1, 3/4), (1, 1/4)]))
        if self.chosen_style == 'masonry':
            ll = GridLayout(rows=3, spacing=self.given_border_width)
            ll.add_widget(self.get_generic_layout('horizontal', [1, 0.2], [(1/2, 1), (1/2, 1)]))
            ll.add_widget(self.get_generic_layout('horizontal', [1, 0.6], [(1/4, 1), (1/2, 1), (1/4, 1)]))
            ll.add_widget(self.get_generic_layout('horizontal', [1, 0.2], [(1/2, 1), (1/2, 1)]))
        if self.chosen_style == 'twin':
            ll = GridLayout(cols=2, spacing=self.given_border_width)
            ll.add_widget(self.get_generic_layout('vertical', [0.5, 1], [(1, 4/5), (1, 1/5)]))
            ll.add_widget(self.get_generic_layout('vertical', [0.5, 1], [(1, 1/5), (1, 4/5)]))
        if self.chosen_style == 'graded':
            num_shades = 10
            graded_colors = self.get_lighter_shades_list(num_shades)
            ll = GridLayout(cols=num_shades, spacing=self.given_border_width)
            for col in range(num_shades):
                lbi = Button(background_color=graded_colors[col], background_normal='', size_hint=[1, 1])
                ll.add_widget(lbi)
        if self.chosen_style == 'quilt':
            ll = GridLayout(rows=1, spacing=self.given_border_width)
            ll.add_widget(self.get_generic_stack_layout())
        if self.chosen_style == 'raw':
            ll = BoxLayout(orientation='horizontal', spacing=self.given_border_width)

            ll1 = GridLayout(cols=1, spacing=self.given_border_width, size_hint=[0.25, 1])
            s1 = self.get_generic_stack_layout()
            ll1.add_widget(s1)
            ll.add_widget(ll1)

            ll2 = GridLayout(rows=1, spacing=self.given_border_width, size_hint=[0.5, 1])
            s2 = self.get_generic_stack_layout()
            ll2.add_widget(s2)
            ll.add_widget(ll2)

            ll3 = GridLayout(cols=1, spacing=self.given_border_width, size_hint=[0.25, 1])
            s3 = self.get_generic_stack_layout()
            ll3.add_widget(s3)
            ll.add_widget(ll3)
        if self.chosen_style == 'paradox':
            ll = BoxLayout(orientation='horizontal', spacing=self.given_border_width)

            ll1 = GridLayout(cols=1, spacing=self.given_border_width, size_hint=[0.3, 1])
            s1 = self.get_generic_stack_layout()
            ll1.add_widget(s1)
            ll.add_widget(ll1)

            ll2 = GridLayout(cols=1, spacing=self.given_border_width, size_hint=[0.2, 1])
            s2 = self.get_generic_stack_layout()
            ll2.add_widget(s2)
            ll.add_widget(ll2)

            ll3 = GridLayout(cols=1, spacing=self.given_border_width, size_hint=[0.5, 1])
            s3 = self.get_generic_stack_layout()
            ll3.add_widget(s3)
            ll.add_widget(ll3)
        return ll

# ############################################################### generic layouts

    def get_generic_stack_layout(self):
        """
        :return:
            - set n to 800 if style is quilt, else n is assigned randomly
            - generate a stack of buttons
        """
        s = StackLayout()
        if self.chosen_style == 'quilt':
            n = 800
            btn_size_hint = [1 / 40, 1 / 20]
        else:
            n = random.choice(list(range(1, 11)))
            btn_size_hint = [1, 1 / n]
        for _ in range(n):
            btn = self.board_button(btn_size_hint)
            s.add_widget(btn)
        return s

    def get_generic_layout(self, orientation, size_hint, b_size_list):
        """
        :param orientation:
            parent boxlayout orientation
        :param size_hint:
            parent size
        :param b_size_list:
            button sizes
        :return:
            - creates a parent widget
            - adds as many buttons as specified in d_size_list
        """
        li = BoxLayout(orientation=orientation, spacing=self.given_border_width, size_hint=size_hint)
        for size in b_size_list:
            lbi = self.board_button(size)
            li.add_widget(lbi)
        return li

    def board_button(self, size):
        """
        :param size: button size
        :return:
            - randomly chooses a color from final_board_colors for button background
            - binds a function to revise the color on press
        """
        background_color = random.choice(self.final_board_colors)
        lbi = Button(
            background_color=background_color, background_normal='', size_hint=size)
        lbi.bind(on_press=partial(self.revise_board_colors, lbi))
        return lbi

    def revise_board_colors(self, *args):
        """
        :param args:
            args[0]: board button object (the one we click to change its color)
        :return:
            - removes the clicked button old background color and adds the newly randomly chosen color
        """
        btn = args[0]
        new_background_color = random.choice(self.final_board_colors)
        btn.background_color = new_background_color

# ################################################ season color dictionary

    @staticmethod
    def get_season_col_dict():
        """
        :return:
            - DataNota season colors
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

