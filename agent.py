# -*- coding: iso-8859-1 -*-

import helper
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
        self.debug = False

    def get_rectangle(self):
        return helper.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def get_shadow_rect(self):
        if self.shadow_type == "RECT":
            return helper.Rect(self.pos_x + self.shadow_top, self.pos_y + self.shadow_left, 
                self.pos_x + self.shadow_width, self.pos_y + self.shadow_height)
        elif self.shadow_type == "SPRITE":
            return helper.Rect(0, 0, self.width, self.height)

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

        self.shadow_type = config.get("SHADOW", "shadow_type")
        if self.shadow_type == "RECT":
            self.shadow_top = config.getint("SHADOW", "shadow_top")
            self.shadow_left = config.getint("SHADOW", "shadow_left")
            self.shadow_width = config.getint("SHADOW", "shadow_width")
            self.shadow_height = config.getint("SHADOW", "shadow_height")
        elif self.shadow_type == "SPRITE":
            ## For self.shadow_type == "SPRITE", the shadow image is at bottom of the sprite,
            ## with same width and height of the sprite
            ## So, at least, the basical shadow is the full image
            self.shadow_top = 0
            self.shadow_left = 0
            self.shadow_width = self.width
            self.shadow_height = self.height

        if config.has_option("DIMENSION", "sort_position"):
            self.sort_position = config.getint("DIMENSION", "sort_position")
        else:
            self.sort_position = int(self.shadow_height / 2)

        #print("%s: %d, %d, %d, %d" % (self.name, self.shadow_top, self.shadow_left, self.shadow_width, self.shadow_height))
        self.animation_velocity = config.getfloat("ASSET", "animation_velocity")

        self.load_custom_config(config)
        

    """
    To override for sub classes
    """
    def load_custom_config(self, config_parser):
        pass

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
        (src_left, src_top) = positions
        #screen.blit(self.source, 
        #    src_top, src_left, self.width, self.height, 
        #    self.pos_x, self.pos_y,  
        #    True)
        screen.blit(self.source, 
            src_left, src_top, self.width, self.height, 
            self.pos_x, self.pos_y, 
            True)
        if self.debug:
            #print("Debug on " + self.name)
            if self.shadow_type == "RECT":
                screen.fillRect(self.pos_x + self.shadow_left, self.pos_y + self.shadow_top, 
                    self.shadow_width, self.shadow_height, psp2d.Color(255,0,0,128))
                screen.fillRect(self.pos_x, self.pos_y, 
                    self.width, self.height, psp2d.Color(255,0,0,128))
                #font.drawText(screen, 0, 32, "%s: (%d,%d)" % (self.name, self.pos_x, self.pos_y))
            elif self.shadow_type == "SPRITE":
                top_of_shadow_sprite = int(src_top) + int(self.height)
                screen.blit(self.source, 
                    src_left, top_of_shadow_sprite, self.width, self.height, 
                    self.pos_x, self.pos_y, 
                    True)

    """
    Returns True if the agent is in collision with walls or any agent
    @param agents: The list of visible agents
    @param walls: The image of the walls. Transparent = no wall
    @param pos_x: Future position x
    @param pos_y: Future position y
    @return The list of collisionned objects
    """
    def detect_collision(self, agents, walls, future_pos_x, future_pos_y):
        all_collision_objects = []
        for agent in agents:
            if agent == self:
                ## Don't detect collision with myself
                continue
            if self.detect_collision_with_object(agent, future_pos_x, future_pos_y):
                #print("%s collision with %s" % (self.name, agent.name))
                #print("at position %d,%d" % (future_pos_x, future_pos_y))
                all_collision_objects.append(agent)

        if len(all_collision_objects) == 0:
            ## No collision detected with any other agent
            pixel = walls.getPixel(
                future_pos_x + (self.shadow_width/2), 
                future_pos_y + (self.shadow_height/2))
            if pixel.alpha != 0:
                all_collision_objects.append(walls)

        return all_collision_objects

    def detect_collision_with_object(self, another_object, future_pos_x, future_pos_y):
        rectangle_collision = False
        ## Rectangle-type shapes
        player_rect = helper.Rect(
            future_pos_x + self.shadow_left, 
            future_pos_y + self.shadow_top,
            self.shadow_width, 
            self.shadow_height)
        another_object_rect = helper.Rect(
            another_object.pos_x + another_object.shadow_left, 
            another_object.pos_y + another_object.shadow_top,
            another_object.shadow_width, 
            another_object.shadow_height)
        rectangle_collision = helper.collision_on_rectangles(player_rect, another_object_rect)
        #if rectangle_collision:
        #    print("rectangle_collision with %s" % (another_object.name))
        #    print("another_object.shadow_type = %s" % another_object.shadow_type)

        if rectangle_collision and another_object.shadow_type == "SPRITE":
            ## Get the pixel in the shadow sprite
            player_top_left = player_rect.top_left()
            player_top_right = player_rect.top_right()
            player_bottom_left = player_rect.bottom_left()
            player_bottom_right = player_rect.bottom_right()
            #another_object_shadow_rect = another_object.get_shadow_rect()
            #print("Computing collision with rect %s" % another_object_rect)
            #print("with points %s, %s, %s, %s" % (player_top_left, player_top_right, player_bottom_left, player_bottom_right))
            if helper.point_in_rect(player_top_left, another_object_rect):
                #print("player_top_left point_in_rect: %s" % player_top_left)
                pixel = another_object.source.getPixel(
                    player_top_left.x - another_object.pos_x, 
                    player_top_left.y - another_object.pos_y + another_object.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return True
            if helper.point_in_rect(player_top_right, another_object_rect):
                #print("player_top_right point_in_rect: %s" % player_top_right)
                pixel = another_object.source.getPixel(
                    player_top_right.x - another_object.pos_x, 
                    player_top_right.y - another_object.pos_y + another_object.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return True
            if helper.point_in_rect(player_bottom_left, another_object_rect):
                #print("player_bottom_left point_in_rect: %s" % player_bottom_left)
                pixel = another_object.source.getPixel(
                    player_bottom_left.x - another_object.pos_x, 
                    player_bottom_left.y - another_object.pos_y + another_object.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return True
            if helper.point_in_rect(player_bottom_right, another_object_rect):
                #print("player_bottom_right point_in_rect: %s" % player_bottom_right)
                pixel = another_object.source.getPixel(
                    player_bottom_right.x - another_object.pos_x, 
                    player_bottom_right.y - another_object.pos_y + another_object.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return True
            
            return False
        return rectangle_collision
    