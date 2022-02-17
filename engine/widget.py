# -*- coding: iso-8859-1 -*-

import psp2d

class Widget:

    def __init__(self):
        self.screen = psp2d.Screen()
        self.visible = True
        
    def update(self):
        pass

    def draw(self):
        pass