# -*- coding: iso-8859-1 -*-

import psp2d

from engine.helper import Point

class Widget:

    def __init__(self, pos_x, pos_y, width, height):
        self.screen = psp2d.Screen()
        self.font = psp2d.Font('assets/font-white.png')
        (self.pos_x, self.pos_y) = (pos_x, pos_y)
        (self.width, self.height) = (width, height)
        self.is_visible = True
    

    def draw_text(self, point, label):
        self.screen.fillRect(point.x, point.y, self.font.textWidth(label) + 2, 15, psp2d.Color(0,0,0,128))
        self.font.drawText(self.screen, point.x + 1, point.y, label)


    def update(self, controller):
        ## Override this method
        pass

    def draw(self):
        ## Override this method
        if self.is_visible:
            self.draw_text(Point(self.pos_x, self.pos_y), "Override the method Widget#draw")
        