# -*- coding: iso-8859-1 -*-

import psp2d

class Widget:

    def __init__(self, sprite_path, pos_x, pos_y):
        (self.pos_x, self.pos_y) = (pos_x, pos_y)
        (self.width, self.height) = (50,50)
        self.sprite = psp2d.Image(sprite_path)
        self.screen = psp2d.Screen()
        
    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        