# -*- coding: iso-8859-1 -*-

import os
import psp2d
from configparser import ConfigParser

import engine.helper as helper
from engine.metadata import Metadata
from engine.conf_board import ConfBoard
from engine.agent_actions_reader import AgentActionsReader
from engine.formula import Formula


"""
Agent base class, mother class of every visible item on the screen.
"""
class Agent(object):

    ## Black transparent for "no collision"
    NO_COLLISION = psp2d.Color(0, 0, 0, 0)
    ## Pink for wall-collision
    WALL_COLLISION = psp2d.Color(255, 0, 255, 255)

    ## In case of generic agent collision
    AGENT_COLLISION = psp2d.Color(255, 255, 255, 255)

    def __init__(self, sprite_file = None):
        if sprite_file is not None:
            try:
                self.sprite = psp2d.Image(sprite_file)
            except:
                print("Cannot open file --%s--" % sprite_file)

        self.metadata = Metadata()
        self.metadata.sprite_file = sprite_file

        self.pos_x = 0
        self.pos_y = 0
        self.animation_flow = 0
        self.is_animated = True
        self.animation_velocity = 0.25
        self.current_board = None
        self.conf_boards = None
        self.debug = False
        self.id = "String defined by the board"
        ## For formulas
        self.production_plan = None

    def get_rectangle(self):
        return helper.Rect(self.pos_x, self.pos_y, self.metadata.width, self.metadata.height)

    def get_shadow_rect(self):
        if self.shadow_type == "RECT":
            return helper.Rect(self.pos_x + self.shadow_top, self.pos_y + self.shadow_left, 
                self.pos_x + self.shadow_width, self.pos_y + self.shadow_height)
        elif self.shadow_type == "SPRITE":
            return helper.Rect(0, 0, self.metadata.width, self.metadata.height)

    def load_config(self, config_file):
        ## Check that config file exists
        if not os.path.isfile(config_file):
            raise ValueError("File not found: %s" % config_file)

        config = ConfigParser()
        config.read(config_file)
        self.metadata.load_config(config)
        try:
            self.source = psp2d.Image(self.metadata.sprite_file)
        except:
            print("Cannot open file --%s--" % self.metadata.sprite_file)
            
        
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
        self.animation_velocity = config.getfloat("ASSET", "animation_velocity")

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
            self.shadow_width = self.metadata.width
            self.shadow_height = self.metadata.height

        #print("%s: %d, %d, %d, %d" % (self.metadata.name, self.shadow_top, self.shadow_left, self.shadow_width, self.shadow_height))
        if config.has_option("DIMENSION", "sort_position"):
            self.sort_position = config.getint("DIMENSION", "sort_position")
        else:
            self.sort_position = int(self.shadow_height / 2)

        self.conf_boards = []
        if config.has_option("COLLISION", "open_board"):
            open_board_conf = config.get("COLLISION", "open_board")
            board_conf = ConfBoard(open_board_conf)
            if board_conf.board_name is not None:
                self.conf_boards.append(board_conf)
        
        self.actions = None
        if config.has_option("COLLISION", "actions"):
            actions_conf = config.get("COLLISION", "actions")
            self.actions = AgentActionsReader.parse(actions_conf)

        self.inventory_open_color = None
        if config.has_option("COLLISION", "open_inventory"):
            self.inventory_open_color = config.get("COLLISION", "open_inventory")

        if config.has_option("CRAFT", "formula"):
            formula_config_file = config.get("CRAFT", "formula").strip()
            ## remove first and last quote
            if formula_config_file[0] in '\'"':
                formula_config_file = formula_config_file[1:-1]
            self.metadata.production_plan = Formula(formula_config_file)
            
        self.load_custom_config(config)
        
    """
    @return Conf_Board instance
    """
    def get_conf_board(self, color_to_match):
        if self.conf_boards is None:
            return None
        for board_conf in self.conf_boards:
            color = board_conf.board_color
            if helper.match_colors(color, color_to_match):
                return board_conf
        return None


    """
    To override for sub classes
    """
    def load_custom_config(self, config_parser):
        pass

    """
    Update the visibility of the instance.
    agents is a dict of agent.name -> agent object
    """
    def update(self, agents, walls, controller):
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
        #    src_top, src_left, self.metadata.width, self.metadata.height, 
        #    self.pos_x, self.pos_y,  
        #    True)
        src_pos = helper.Point(src_left, src_top)
        screen_pos = helper.Point(self.pos_x, self.pos_y)

        if screen_pos.x < 0 :
            src_pos.x = src_pos.x - screen_pos.x
            screen_pos.x = 0
        if screen_pos.y < 0:
            src_pos.y = src_pos.y - screen_pos.y
            screen_pos.y = 0
        
        screen.blit(self.source, 
                src_pos.x, src_pos.y, self.metadata.width, self.metadata.height, 
                screen_pos.x, screen_pos.y, 
                True)

        if self.debug:
            #print("Debug on " + self.metadata.name)
            if self.shadow_type == "RECT":
                screen.fillRect(self.pos_x + self.shadow_left, self.pos_y + self.shadow_top, 
                    self.shadow_width, self.shadow_height, psp2d.Color(255,0,0,128))
                screen.fillRect(self.pos_x, self.pos_y, 
                    self.metadata.width, self.metadata.height, psp2d.Color(255,0,0,128))
                #font.drawText(screen, 0, 32, "%s: (%d,%d)" % (self.metadata.name, self.pos_x, self.pos_y))
            elif self.shadow_type == "SPRITE":
                top_of_shadow_sprite = int(src_top) + int(self.metadata.height)
                screen.blit(self.source, 
                    src_left, top_of_shadow_sprite, self.metadata.width, self.metadata.height, 
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
            color_of_collision = self.detect_collision_with_object(agent, future_pos_x, future_pos_y)
            if color_of_collision != Agent.NO_COLLISION:
                #print("%s collision with %s" % (self.metadata.name, agent.name))
                #print("at position %d,%d" % (future_pos_x, future_pos_y))
                collision_with_agent = (agent, color_of_collision)
                all_collision_objects.append(collision_with_agent)
        
        if len(all_collision_objects) == 0:
            ## No collision detected with any other agent
            corner_pixels = self.get_pixels_alpha_on_shadow(future_pos_x, future_pos_y)
            if corner_pixels[0].alpha != 0 or corner_pixels[1].alpha != 0 or corner_pixels[2].alpha != 0 or corner_pixels[3].alpha != 0:
                #print("corner_pixels collision with something...")
                if helper.match_one_color(corner_pixels, Agent.WALL_COLLISION):
                    #print("Collision with wall")
                    collision_with_wall = (walls, Agent.WALL_COLLISION)
                    all_collision_objects.append(collision_with_wall)
                else:
                    #print("collision with board ?")
                    ## try to get the destination board from the board
                    color = [c for c in corner_pixels if c.alpha != 0][0]
                    #print(" color %d,%d,%d, %d" % (color.red, color.green, color.blue, color.alpha))
            
                    ## Try to get the board of the agent
                    board_conf = self.get_conf_board(color)
                    #print("board_conf(1): %s" % str(board_conf))

                    if board_conf is None:
                        ## Try to get the board of the current board
                        board_conf = self.current_board.get_conf_board(color)
                        #print("board_conf(2): %s" % str(board_conf))
                        
                    if board_conf is not None:
                        #print("found %s" % board_conf)
                        collision_with_board = (board_conf, color)
                        all_collision_objects.append(collision_with_board)

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
                    player_top_left.y - another_object.pos_y + another_object.metadata.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return pixel
            if helper.point_in_rect(player_top_right, another_object_rect):
                #print("player_top_right point_in_rect: %s" % player_top_right)
                pixel = another_object.source.getPixel(
                    player_top_right.x - another_object.pos_x, 
                    player_top_right.y - another_object.pos_y + another_object.metadata.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return pixel
            if helper.point_in_rect(player_bottom_left, another_object_rect):
                #print("player_bottom_left point_in_rect: %s" % player_bottom_left)
                pixel = another_object.source.getPixel(
                    player_bottom_left.x - another_object.pos_x, 
                    player_bottom_left.y - another_object.pos_y + another_object.metadata.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return pixel
            if helper.point_in_rect(player_bottom_right, another_object_rect):
                #print("player_bottom_right point_in_rect: %s" % player_bottom_right)
                pixel = another_object.source.getPixel(
                    player_bottom_right.x - another_object.pos_x, 
                    player_bottom_right.y - another_object.pos_y + another_object.metadata.height)
                #print("pixel.alpha: %d" % pixel.alpha)
                if pixel.alpha != 0:
                    #print("Collision detected !")
                    return pixel
            
            return Agent.NO_COLLISION
        if rectangle_collision:
            return Agent.AGENT_COLLISION
        else:
            return Agent.NO_COLLISION
    
    """
    Return the set of 4 pixels on the image on the corners of the agent
    """
    def get_pixels_alpha_on_shadow(self, future_pos_x, future_pos_y):
        agent_rect = helper.Rect(
                future_pos_x + self.shadow_left, 
                future_pos_y + self.shadow_top,
                self.shadow_width, 
                self.shadow_height)
        player_top_left     = agent_rect.top_left()
        player_top_right    = agent_rect.top_right()
        player_bottom_left  = agent_rect.bottom_left()
        player_bottom_right = agent_rect.bottom_right()
        image = self.current_board.walls
        pixel_top_left      = image.getPixel(player_top_left.x, player_top_left.y)
        pixel_top_right     = image.getPixel(player_top_right.x, player_top_right.y)
        pixel_bottom_left   = image.getPixel(player_bottom_left.x, player_bottom_left.y)
        pixel_bottom_right  = image.getPixel(player_bottom_right.x, player_bottom_right.y)
        #print("top_left: %s" % helper.str_color(pixel_top_left))
        #print("top_right at %s: %s" % (player_top_right, helper.str_color(pixel_top_right)))
        #print("bottom_left: %s" % helper.str_color(pixel_bottom_left))
        #print("bottom_right: %s" % helper.str_color(pixel_bottom_right))
        return (pixel_top_left, pixel_top_right, pixel_bottom_left, pixel_bottom_right)
        