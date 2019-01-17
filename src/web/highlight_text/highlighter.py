COLOR_SCHEME = {'genitives': '<b><font color="#A52A2A">{}</font></b>'
                , 'comparativ':'<span style="background-color: #66CDAA">{}</span>'
                , 'coordinate_NPs': '<span style="background-color: #228B22">{}</span>'
                , 'not in vocabulary': '<span style="background-color: #FFE4E1">{}</span>'
                , 'i vs we': '<b><font color="#8B008B">{}</font></b>'
                , 'imperative mood': '<span style="background-color: #DEB887">{}</span>'
                , 'subjunctive mood': '<span style="background-color: #BC8F8F">{}</span>'}

class HTMLStyle:
    """
    Класс для создания цветовой схемы текста
    """
    def __init__(self, color_scheme=COLOR_SCHEME):
        self.color_scheme = color_scheme

