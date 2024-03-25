
from utilities.common import Common
from kivy.uix.gridlayout import GridLayout
from kivy.utils import get_color_from_hex
import random


class Analytics(Common):
    """
    """
    def __init__(self):
        super().__init__()
        self.accent = 'ACCENT'

# ################################################ grading color shades

    def get_lighter_shades_list(self, n):
        rgb_color = get_color_from_hex(random.choices(self.given_added_color_list, k=1)[0])
        rgb_color = [rgb_color[0], rgb_color[1], rgb_color[2]]
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

    def get_style_layout(self, given_style, given_border_width):
        ll = None
        if given_style == 'default':
            ll = GridLayout(cols=3, spacing=given_border_width)
            ll.add_widget(self.get_generic_layout('vertical', given_border_width, [1, 1], [(1, 1/4), (1, 3/4)], None))
            ll.add_widget(self.get_generic_layout('vertical', given_border_width, [1, 1], [(1, 1/5), (1, 3/5), (1, 1/5)], None))
            ll.add_widget(self.get_generic_layout('vertical', given_border_width, [1, 1], [(1, 3/4), (1, 1/4)], None))
        if given_style == 's1':
            ll = GridLayout(rows=3, spacing=given_border_width)
            ll.add_widget(self.get_generic_layout('horizontal', given_border_width, [1, 0.2], [(1/2, 1), (1/2, 1)], None))
            ll.add_widget(self.get_generic_layout('horizontal', given_border_width,[1, 0.6], [(1/4, 1), (1/2, 1), (1/4, 1)], None))
            ll.add_widget(self.get_generic_layout('horizontal', given_border_width,[1, 0.2], [(1/2, 1), (1/2, 1)], None))
        if given_style == 's2':
            ll = GridLayout(cols=2, spacing=given_border_width)
            ll.add_widget(self.get_generic_layout('vertical', given_border_width, [0.5, 1], [(1, 4/5), (1, 1/5)], None))
            ll.add_widget(self.get_generic_layout('vertical', given_border_width, [0.5, 1], [(1, 1/5), (1, 4/5)], None))
        if given_style == 's3':
            num_shades = 30
            self.final_colors = self.get_lighter_shades_list(num_shades)
            self.color_order = 'y'
            ll = GridLayout(cols=num_shades, spacing=given_border_width)
            for col in range(num_shades):
                ll.add_widget(
                    self.get_generic_layout(
                        orientation='vertical', spacing=given_border_width, size_hint=[1/num_shades, 1],
                        b_size_list=[(1, 1)], color_order=self.final_colors[col])
                )
        return ll

# ################################################ season color dictionary

    @staticmethod
    def get_season_col_dict():
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

