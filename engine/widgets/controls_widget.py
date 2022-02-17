# -*- coding: iso-8859-1 -*-
from engine.helper import Point
import psp2d

from engine.widget import Widget

class Button:
    TRIANGLE = 1
    CIRCLE = 2
    CROSS = 3
    SQUARE = 4

class ControlsWidget(Widget):
    def __init__(self):
        Widget.__init__(self)
        self.control_sprite = psp2d.Image("assets/controls.png")
        self.font = psp2d.Font('font.png')
        (self.width, self.height) = (50,50)
        (self.pos_x, self.pos_y) = (200,100)
        self.labels = {
            Button.TRIANGLE: "Triangle",
            Button.CIRCLE: "Circle",
            Button.CROSS: "Cross",
            Button.SQUARE: "Square"
        }

    def update(self):
        pass

    def draw(self):
        self.screen.blit(self.control_sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        ## Draw the text for actions
        if len(self.labels[Button.TRIANGLE]) > 0:
            triangle_pos = Point(self.pos_x + 35, self.pos_y)
            self.screen.fillRect(triangle_pos.x, triangle_pos.y, 50, 16, psp2d.Color(0,0,0,128))
            self.font.drawText(self.screen, triangle_pos.x, triangle_pos.y, self.labels[Button.TRIANGLE])
        
        if len(self.labels[Button.CIRCLE]) > 0:
            triangle_pos = Point(self.pos_x + 50, self.pos_y + 17)
            self.screen.fillRect(triangle_pos.x, triangle_pos.y, 50, 16, psp2d.Color(0,0,0,128))
            self.font.drawText(self.screen, triangle_pos.x, triangle_pos.y, self.labels[Button.CIRCLE])
        
        if len(self.labels[Button.CROSS]) > 0:
            triangle_pos = Point(self.pos_x + 35, self.pos_y + 34)
            self.screen.fillRect(triangle_pos.x, triangle_pos.y, 50, 16, psp2d.Color(0,0,0,128))
            self.font.drawText(self.screen, triangle_pos.x, triangle_pos.y, self.labels[Button.CROSS])
        
        if len(self.labels[Button.SQUARE]) > 0:
            triangle_pos = Point(self.pos_x - 50, self.pos_y + 17)
            self.screen.fillRect(triangle_pos.x, triangle_pos.y, 50, 16, psp2d.Color(0,0,0,128))
            self.font.drawText(self.screen, triangle_pos.x, triangle_pos.y, self.labels[Button.SQUARE])
        