# -*- coding: iso-8859-1 -*-

import psp2d

from engine.widget import Widget
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper

class GameOverWidget(Widget):
    MENU_ITEM_WIDTH = 330
    MENU_ITEM_HEIGHT = 54

    def __init__(self, game):
        Widget.__init__(self, 0, 0, MAX_WIDTH, MAX_HEIGHT)
        self.font = psp2d.Font('fonts/font-Karumbi-46-black.png')
        self.small_font = psp2d.Font('assets/font-white.png')
        self.game = game
        self.is_visible = False
        (self.menu_bg, _) = helper.load_sprite("assets/displays/parchment.png", 
            GameOverWidget.MENU_ITEM_WIDTH, GameOverWidget.MENU_ITEM_HEIGHT)
        self.button_CROSS_asset = psp2d.Image("assets/control-cross.png")

    def update(self, controller):
        if self.is_visible and controller.cross:
            self.is_visible = False
            ## Open the display of the inventory
            self.game.restart_game()

    def draw(self):
        ## Fill the whole screen of black, with 50% transparency
        self.screen.fillRect(0, 0, MAX_WIDTH, MAX_HEIGHT, psp2d.Color(0,0,0, 128))

        pos_x = (MAX_WIDTH - GameOverWidget.MENU_ITEM_WIDTH) / 2
        pos_y = (MAX_HEIGHT - GameOverWidget.MENU_ITEM_HEIGHT) / 2

        self.screen.blit(self.menu_bg, 0, 0, 
            GameOverWidget.MENU_ITEM_WIDTH, 
            GameOverWidget.MENU_ITEM_HEIGHT, pos_x, pos_y, True)

        label = "Game over"
        pos_x = (MAX_WIDTH - self.font.textWidth(label)) / 2
        pos_y = (MAX_HEIGHT - self.font.textHeight(label)) / 2
        self.font.drawText(self.screen, pos_x, pos_y + 8, label)

        label = " Restart"
        pos_x = (MAX_WIDTH - self.small_font.textWidth(label)) / 2
        pos_y = ( (MAX_HEIGHT - GameOverWidget.MENU_ITEM_HEIGHT) / 2 ) + (GameOverWidget.MENU_ITEM_HEIGHT + 1.5)
        self.screen.blit(self.button_CROSS_asset, 0, 0, 16, 16, pos_x, pos_y, True)
        pos_x += 16
        self.small_font.drawText(self.screen, pos_x, pos_y + 1, label)
