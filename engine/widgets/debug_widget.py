# -*- coding: iso-8859-1 -*-
from engine.widget import Widget

import psp2d

"""
Add this widget in the game to display some debug text

debug = engine.widgets.debug_widget.DebugWidget()
debug.text = "Display this text !"
game.add_widget(debug)
"""
class DebugWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.text = "DEBUG"
        self.font = psp2d.Font('font.png')
        
    def update(self, controller):
        pass

    def draw(self):
        self.screen.fillRect(0, 0, 250, 16, psp2d.Color(0,0,0,128))
        self.font.drawText(self.screen, 0, 0, self.text)
        