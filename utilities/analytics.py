

class Analytics:
    def __init__(self):
        self.accent = 'ACCENT'

    def get_dark_light_accent_colors(self, chosen_color):
        col_dict = self.get_col_dict()
        light_list = []
        color_list = []
        dark_list = []
        accent_list = []
        for col in chosen_color:
            light = col_dict.get(col).get('tint')
            color = [
                col_dict.get(col).get('tone')[0],
                col_dict.get(col).get('tone')[1],
                col_dict.get(col).get('shade')[0],
                col_dict.get(col).get('shade')[1]
            ]
            dark = [
                col_dict.get(col).get('tone')[2],
                col_dict.get(col).get('tone')[3],
                col_dict.get(col).get('shade')[2],
                col_dict.get(col).get('shade')[3]
            ]
            accent = [
                col_dict.get(col).get('accent')[0]
            ]
            light_list.append(light)
            color_list.append(color)
            dark_list.append(dark)
            accent_list.append(accent)
        all_colors_dict = {'light': sum(light_list, []), 'color': sum(color_list, []),
                           'dark': sum(dark_list, []), 'accent': sum(accent_list, [])}
        return all_colors_dict

    @staticmethod
    def get_col_dict():
        """
        HSL
        shade: subtract 10 points from L
        tone: subtract 20 points from s -- first one 100 s if already not
        tint: add 10 points to l -- last one 90 if not already -- some 95
        """
        col_dict = {
            'AC1717': {
                'shade': ['AC1717', '7E1111', '510B0B', '240505'],
                'tone': ['C30000', '982B2B', '982B2B', '715252'],
                'tint': ['D81D1D', 'E64242', 'EC6F6F', 'F9D2D2'],
                'accent': ['FF0000']
            },
            'd9381e': {
                'shade': ['d9381e', 'AA2C18', '7D2011', '51150B'],
                'tone': ['F72200', 'C14A36', 'A85B4F', '8F6D68'],
                'tint': ['E55943', 'EB8170', 'F1A89C', 'F9D8D2'],
                'accent': ['FF2300']
            },
            'FF6F00': {
                'shade': ['FF6F00', 'CC5900', '994300', '662D00'],
                'tone': ['E57319', 'CC7633', 'B3794C', '997C66'],
                'tint': ['FF8C33', 'FFA966', 'FFC699', 'FFE2CC'],
                'accent': ['FF7103']
            },
            'ffc107': {
                'shade': ['ffc107', 'D19D00', '9E7700', '6B5000'],
                'tone': ['E6B520', 'CDA839', 'B59C51', '9C8F6A'],
                'tint': ['FFCD38', 'FFDA6B', 'FFE79E', 'FFF2CC'],
                'accent': ['FFBF00']
            },
            'ffeb3b': {
                'shade': ['ffeb3b', 'FFE60A', 'D6C000', 'A39300'],
                'tone': ['EBDB4F', 'D8CC62', 'C4BC76', 'B1AD89'],
                'tint': ['FFF070', 'FFF6A3', 'FFFACC', 'FFFCE5'],
                'accent': ['FFE500']
            },
            '8AF905': {
                'shade': ['8AF905', '6FC804', '539603', '376402'],
                'tone': ['8AFE00', '88E01E', '85C638', '83AD51'],
                'tint': ['A2FB37', 'B9FC69', 'D0FD9B', 'E8FECD'],
                'accent': ['8BFF01']
            },
            '4caf50': {
                'shade': ['4caf50', '3C8B3F', '2D672F', '1D441F'],
                'tone': ['60A663', '6EAD70', '669568', '778478'],
                'tint': ['6DC071', '91CF93', 'B4DFB6', 'DBF0DC'],
                'accent': ['00FF0A']
            },
            '00ffff': {
                'shade': ['00ffff', '00CCCC', '009999', '006666'],
                'tone': ['19E6E6', '33CCCC', '4CB3B3', '669999'],
                'tint': ['33FFFF', '66FFFF', '99FFFF', 'CCFFFF'],
                'accent': ['06FFFF']
            },
            '2196f3': {
                'shade': ['2196f3', '0C7CD5', '0960A5', '064374'],
                'tone': ['1597FF', '3893DC', '4F91C4', '678EAD'],
                'tint': ['51ADF6', '81C4F8', 'B2DAFB', 'CFE8FC'],
                'accent': ['008EFF']
            },
            '3f51b5': {
                'shade': ['3f51b5', '324090', '252F6A', '181E44'],
                'tone': ['0025F4', '58629C', '7980A4', '707384'],
                'tint': ['6070C8', '8692D5', 'ACB4E2', 'D2D6EF'],
                'accent': ['0027FF']
            },
            '990099': {
                'shade': ['990099', '750075', '5C005C', '330033'],
                'tone': ['8A0F8A', '7A1F7A', '6B2E6B', '5C3D5C'],
                'tint': ['FF00FF', 'FF66FF', 'FF99FF', 'FFE5FF'],
                'accent': ['FF00FF']
            },
            'a50062': {
                'shade': ['a50062', '8A0052', '6B0040', '4D002D'],
                'tone': ['95105F', '84215C', '743259', '634256'],
                'tint': ['FF0097', 'FF4DB7', 'FF8ACF', 'FFE5F5'],
                'accent': ['FF0097']
            },
            'FFFFFF': {
                'shade': ['FFFFFF', 'F6F7FD', 'FDFDF6', 'FDF6FD'],
                'tone': ['F6F1F1', 'F6F6F1', 'F1F6F6', 'F7F7F8'],
                'tint': ['F1FAFF', 'F1FFF3', 'FFFAE9', 'FFF1F1'],
                'accent': ['F5F5F5']
            },
            'a8a9b4': {
                'shade': ['a8a9b4', 'B4A8A8', 'B4B2A8', 'A8B3B4'],
                'tone': ['8B8D9D', '9D8B8B', '9D998B', '8C9D8B'],
                'tint': ['85828A', '8A8282', '828A87', '898A82'],
                'accent': ['E9E9E9']
            },
            '808080': {
                'shade': ['808080', '564E4E', '524E56', '4F564E'],
                'tone': ['3A3532', '363A32', '32383A', '39323A'],
                'tint': ['938B8B', '93918B', '8B938F', '8F8B93'],
                'accent': ['595959']
            },
            '000000': {
                'shade': ['000000', '645A5A', '5D5A64', '5A645D'],
                'tone': ['483939', '483946', '3C3948', '394845'],
                'tint': ['341A1A', '34301A', '1A1C34', '311A34'],
                'accent': ['1B1818']
            }
        }
        return col_dict

