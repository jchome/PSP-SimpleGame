# -*- coding: iso-8859-1 -*-

import psp2d
from engine.helper import Point
from engine.widget import Widget

import engine.translation
_ = engine.translation.translate

class InventoryWidget(Widget):
    def __init__(self, player):
        Widget.__init__(self, 11, 2, 25, 27)
        self.player = player
        self.sprite = psp2d.Image("assets/inventory.png")
        self.triangle_button = psp2d.Image("assets/control-triangle.png")

    """
    Catpure buttons to open the inventory display
    """
    def update(self, controller):
        if controller.triangle and controller.l:
            ## Open the display of the inventory
            self.player.current_board.game.open_inventory()

    def draw(self):
        ## Default drawing
        self.screen.blit(self.sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        
        self.language = self.player.current_board.game.current_language
        ## Get the count of items
        self.draw_text(Point(self.pos_x+self.width, self.pos_y), "%d" % self.player.inventory.size())
        
        ## Draw the helper
        self.draw_text(Point(self.pos_x, self.pos_y + self.height), "L+     " )
        self.screen.blit(self.triangle_button, 0,0, 16,16, self.pos_x + 18, self.pos_y + self.height - 1, True)
