# -*- coding: iso-8859-1 -*-

import psp2d

from engine.widget import Widget
from engine.helper import Point

"""
Add this widget in the game to display some debug text

debug = engine.widgets.debug_widget.DebugWidget()
debug.text = "Display this text !"
game.add_widget(debug)
"""
class DebugWidget(Widget):
    def __init__(self):
        Widget.__init__(self, 0, 0, 10, 10)
        self.text = "DEBUG"
        self.font = psp2d.Font('assets/font-white.png')
        
    def update(self, controller):
        pass

    def draw(self):
        self.screen.fillRect(0, 0, 250, 16, psp2d.Color(0,0,0,128))
        self.draw_text( Point(0,0), self.text)
        