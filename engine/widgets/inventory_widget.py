# -*- coding: iso-8859-1 -*-

from engine.helper import Point
from engine.widget import Widget


class InventoryWidget(Widget):
    def __init__(self, player):
        pos_x, pos_y = (11,2)
        Widget.__init__(self, "assets/inventory.png", pos_x, pos_y)
        (self.width, self.height) = (25,27)
        self.player = player

    def draw(self):
        ## Default drawing
        self.screen.blit(self.sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        self.draw_text(Point(27,17), "%d items" % self.player.inventory.size() )
