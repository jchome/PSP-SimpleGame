# -*- coding: iso-8859-1 -*-

import psp2d

class Widget:

    def __init__(self, sprite_path, pos_x, pos_y):
        self.font = psp2d.Font('font.png')
        (self.pos_x, self.pos_y) = (pos_x, pos_y)
        ## Set default width and height
        (self.width, self.height) = (50,50)
        self.sprite = psp2d.Image(sprite_path)
        self.screen = psp2d.Screen()
        self.is_visible = True
    

    def draw_text(self, point, label):
        self.screen.fillRect(point.x, point.y, self.font.textWidth(label) + 2, 15, psp2d.Color(0,0,0,128))
        self.font.drawText(self.screen, point.x + 1, point.y, label)


    def update(self):
        ## Override this method
        pass

    def draw(self):
        ## Default drawing
        self.screen.blit(self.sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        