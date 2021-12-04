# -*- coding: iso-8859-1 -*-

import psp2d
"""
Agent base class, mother class of every visible item on the screen.
"""
class Agent(object):
    def __init__(self, sprite_file):
        try:
            self.sprite = psp2d.Image(sprite_file)
        except:
            print("Cannot open file --%s--" % sprite_file)

        self.width = 32
        self.height = 32
        self.pos_x = 0
        self.pos_y = 0
        
    """
    Update the visibility of the instance.
    """
    def update(self, walls):
        # In the base class do nothing
        pass

    """
    Draw the instance in the screen.
    """
    def draw(self, screen, walls):
        # In the base class do nothing
        pass

    """
    Returns True if the agent is in collision with walls
    @param walls: the image of the walls. Transparent = no wall
    """
    def detect_collision(self, walls, pos_x, pos_y):
        pixel = walls.getPixel(pos_x, pos_y)
        return pixel.alpha != 0
