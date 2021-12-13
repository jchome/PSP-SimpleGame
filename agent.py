# -*- coding: iso-8859-1 -*-

import psp2d
from configparser import ConfigParser
from time import time


font = psp2d.Font('font.png')

"""
Agent base class, mother class of every visible item on the screen.
"""
class Agent(object):
    def __init__(self, sprite_file = None):
        if sprite_file is not None:
            try:
                self.sprite = psp2d.Image(sprite_file)
            except:
                print("Cannot open file --%s--" % sprite_file)

        self.width = 32
        self.height = 32
        self.pos_x = 0
        self.pos_y = 0
        self.last_animation_timestamp = time()
        self.animation_flow = 0
        self.is_animated = True
        self.animation_velocity = 0.25

    def load_config(self, config_file):
        config = ConfigParser()
        config.read(config_file)
        self.name = config.get("ASSET", "name")
        self.source = psp2d.Image(config.get("ASSET", "source"))
        sprites_definition = config.get("ASSET", "sprites")
        self.sprites = {}
        for item in sprites_definition.split("\n"):
            if len(item.strip()) == 0:
                continue
            data = item.strip().split("=")
            key = int(data[0].strip())
            positions = eval(data[1].strip())
            self.sprites[key] = positions
        
        self.is_animated = len(self.sprites) > 0

        self.width = config.getint("DIMENSION", "width")
        self.height = config.getint("DIMENSION", "height")
        self.pos_x = config.getint("DIMENSION", "pos_x")
        self.pos_y = config.getint("DIMENSION", "pos_y")
        self.shadow_top = config.getint("DIMENSION", "shadow_top")
        self.shadow_left = config.getint("DIMENSION", "shadow_left")
        self.shadow_width = config.getint("DIMENSION", "shadow_width")
        self.shadow_height = config.getint("DIMENSION", "shadow_height")
        self.animation_velocity = config.getfloat("ASSET", "animation_velocity")
        #print("shadow agent: %d %d %d %d" % (self.shadow_top, self.shadow_left, 
        #    self.shadow_width, self.shadow_height) )

    """
    Update the visibility of the instance.
    """
    def update(self, agents, walls):
        if self.is_animated:
            # One more step of the animation
            self.animation_flow += self.animation_velocity
            if self.animation_flow > len(self.sprites)-1:
                # Restart the animation from the beginning
                self.animation_flow = 0


    """
    Draw the instance in the screen.
    """
    def draw(self, screen):
        positions = self.sprites[int(self.animation_flow)]
        (src_top, src_left) = positions
        screen.blit(self.source, 
            src_top, src_left, self.width, self.height, 
            self.pos_x, self.pos_y,  
            True)
        screen.fillRect(self.pos_x + self.shadow_left, self.pos_y + self.shadow_top, 
            self.shadow_width, self.shadow_height, psp2d.Color(255,0,0,128))
        #screen.fillRect(self.pos_x, self.pos_y, 
        #    self.width, self.height, psp2d.Color(255,0,0,128))

        font.drawText(screen, 0, 32, "%s: (%d,%d)" % (self.name, self.pos_x, self.pos_y))

    """
    Returns True if the agent is in collision with walls or any agent
    @param walls: the image of the walls. Transparent = no wall
    """
    def detect_collision(self, agents, walls, pos_x, pos_y):
        for agent in agents:
            if agent == self:
                ## Don't detect collision with myself
                continue
            if self.detect_collision_with_object(agent, pos_x, pos_y):
                return True

        ## No collision detected with any other agent
        pixel = walls.getPixel(
            pos_x + (self.shadow_width/2), 
            pos_y + (self.shadow_height/2))
        return pixel.alpha != 0

    def detect_collision_with_object(self, another_object, agent_pos_x, agent_pos_y):
        player_pos_x = agent_pos_x + self.shadow_top
        player_pos_y = agent_pos_y + self.shadow_left
        another_object_pos_x = another_object.pos_x+another_object.shadow_top
        another_object_pos_y = another_object.pos_y+another_object.shadow_left
        if player_pos_x < another_object_pos_x+another_object.shadow_width and player_pos_x+self.shadow_width > another_object_pos_x:
            if player_pos_y < another_object_pos_y+another_object.shadow_height and player_pos_y+self.shadow_height > another_object_pos_y:
                return True
        return False