# -*- coding: iso-8859-1 -*-

import psp2d

from engine.widget import Widget
from engine.helper import Point
from engine.constants import MAX_HEIGHT, MAX_WIDTH

"""
Add this widget in the game to display some debug text

debug = engine.widgets.debug_widget.DebugWidget()
debug.text = "Display this text !"
game.add_widget(debug)
"""
class PlayerLifeWidget(Widget):
    def __init__(self, player):
        ## 100 = width of the life's bar
        Widget.__init__(self, 0, 0, 102, 19)
        self.pos_x = (MAX_WIDTH - self.width)/2
        self.player = player
        self.sprite = psp2d.Image("assets/life-bar.png")
        
    def update(self, controller):
        pass

    def draw(self):
        self.screen.blit(self.sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        
        self.screen.fillRect(self.pos_x + 1, self.pos_y+1, int(self.player.life.food), 8, psp2d.Color(0,0,255,128))
        self.screen.fillRect(self.pos_x + 1, self.pos_y+10, int(self.player.life.food), 8, psp2d.Color(0,255,0,128))
        