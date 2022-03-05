# -*- coding: iso-8859-1 -*-

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper


class InventoryDisplay(Display):

    def __init__(self, name):
        Display.__init__(self, name)
        self.font = psp2d.Font('font.png')
        (self.background, _) = helper.load_sprite("assets/displays/inventory.png", 
            MAX_WIDTH, MAX_HEIGHT)
        (self.item, self.item_selected) = helper.load_sprite("assets/displays/inventory-item.png", 
            16, 16)


    def update(self):
        ## The update method is called only for active displays
        controller = psp2d.Controller()
        if controller.down:
            direction = "DOWN"
        elif controller.up:
            direction = "UP"
        elif controller.left:
            direction = "LEFT"
        elif controller.right:
            direction = "RIGHT"
        elif controller.cross:
            self.game.close_inventory()
        

    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        ## Add the selected item
        self.screen.blit(self.item_selected, 0, 0, 16, 16, 4, 34, True)
