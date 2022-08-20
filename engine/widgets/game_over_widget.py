# -*- coding: iso-8859-1 -*-

import psp2d

from engine.widget import Widget
from engine.constants import MAX_HEIGHT, MAX_WIDTH

class GameOverWidget(Widget):
    def __init__(self, game):
        Widget.__init__(self, 0, 0, MAX_WIDTH, MAX_HEIGHT)
        self.font = psp2d.Font('assets/font-white.png')
        self.game = game
        self.is_visible = False

    def update(self, controller):
        if self.is_visible and controller.cross:
            self.is_visible = False
            ## Open the display of the inventory
            self.game.restart_game()

    def draw(self):
        ## Fill the whole screen of black, with 50% transparency
        self.screen.fillRect(0, 0, MAX_WIDTH, MAX_HEIGHT, psp2d.Color(0,0,0, 128))

        self.font.drawText(self.screen, MAX_WIDTH/2, MAX_HEIGHT/2, 
            "Game over. Press X to restart")