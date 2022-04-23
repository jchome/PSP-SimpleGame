# -*- coding: iso-8859-1 -*-

import psp2d
from time import time
import math
from configparser import ConfigParser

from engine.displays.conf_board import ConfBoard
from engine.constants import MAX_HEIGHT, MAX_WIDTH
from engine.helper import Point, color_not_alpha_0, match_colors, str_color
from engine.interaction_object import InteractionObject
from engine.agent import Agent
from engine.displays.board import Board

from engine.widgets.controls_widget import Button, ControlsWidget
from engine.displays.inventory.inventory import Inventory


font = psp2d.Font('font.png')

class Player(Agent):
    def __init__(self):
        config = ConfigParser()
        config.read('conf/player.ini')
        Agent.__init__(self, config.get("ASSET", "source") )
        self.metadata.name = config.get("ASSET", "name")
        sprite_directions = config.get("ASSET", "sprite_directions")

        self.velocity = config.getfloat("ASSET", "velocity")
        self.animation_velocity = config.getfloat("ASSET", "animation_velocity")

        ## By default, the player is visible
        self.is_visible = True
        
        self.sprites = {}
        for item in sprite_directions.split("\n"):
            if len(item.strip()) == 0:
                continue
            data = item.strip().split("=")
            key = data[0].strip()
            positions = eval(data[1].strip())
            self.sprites[key] = positions

        self.metadata.width = config.getint("DIMENSION", "width")
        self.metadata.height = config.getint("DIMENSION", "height")
        self.direction = "DOWN"
        self.is_running = False
        self.animation_flow = 0
        self.pos_x = config.getint("DIMENSION", "pos_x")
        self.pos_y = config.getint("DIMENSION", "pos_y")
        self.shadow_type = config.get("SHADOW", "shadow_type")
        if self.shadow_type == "RECT":
            self.shadow_top = config.getint("SHADOW", "shadow_top")
            self.shadow_left = config.getint("SHADOW", "shadow_left")
            self.shadow_width = config.getint("SHADOW", "shadow_width")
            self.shadow_height = config.getint("SHADOW", "shadow_height")
            
        if config.has_option("DIMENSION", "sort_position"):
            self.sort_position = config.getint("DIMENSION", "sort_position")
        else:
            self.sort_position = int(self.shadow_height / 2)

        self.player_interact_with_agent = None
        self.controls_widget = None
        self.bonus = 0
        self.debug = False
        self.inventory = Inventory()

    def compute_new_position(self, controller):
        (dx, dy) = (0, 0)
        if controller.down:
            dy = 1 * self.velocity
            self.direction = "DOWN"
        elif controller.up:
            dy = -1 * self.velocity
            self.direction = "UP"
        elif controller.left:
            dx = -1 * self.velocity
            self.direction = "LEFT"
        elif controller.right:
            dx = 1 * self.velocity
            self.direction = "RIGHT"
        else:
            pass
            """dx = (controller.analogX / 127) * self.velocity
            dy = (controller.analogY / 127) * self.velocity
            if dx == 0 and dy == 0:
                self.animation_flow = 0
            else:
                angle = int(math.degrees(math.atan2(dy, dx)) + 180)
                # 360 = left
                # 270 = down
                # 180 = right
                # 90 = up
                if angle > 45 and angle <= 135:
                    self.direction = "UP"
                elif angle > 135 and angle <= 225:
                    self.direction = "RIGHT"
                elif angle > 225 and angle <= 315:
                    self.direction = "DOWN"
                else:
                    self.direction = "LEFT"
            """
        if dx == 0 and dy == 0:
            self.is_running = False
        else:
            if not self.is_running:
                self.is_running = True
                # Force to restart the animation to frame #0
                self.animation_flow = 0

        #print("dx, dy = %d, %d" % (dx,dy))
        new_pos_x = max( min(self.pos_x + dx, MAX_WIDTH), 0 - self.metadata.width)
        new_pos_y = max( min(self.pos_y + dy, MAX_HEIGHT), 0 - self.metadata.height)

        #print("position: %d,%d -> %d,%d" % (self.pos_x, self.pos_y, new_pos_x, new_pos_y))
        return (new_pos_x, new_pos_y)

    """
    agents is a dict of agent.name -> agent object
    """
    def update(self, agents, walls, controller):
        if not self.is_visible:
            return

        ## Capture the START key, to display the main menu
        if controller.start:
            self.current_board.game.set_active_display("MainMenu")
            return
        

        if self.controls_widget is not None:
            ## Don't allow to move when the controls-widget is present
            self.is_running = False
            return

        (new_pos_x, new_pos_y) = self.compute_new_position(controller)

        collisioned_agents = self.detect_collision(agents.values(), walls, 
                                     new_pos_x, 
                                     new_pos_y)
        player_is_blocked = False
        self.player_interact_with_agent = None
        for (agent, color) in collisioned_agents:
            #print("collisioned_agents:")
            #print(collisioned_agents)
            #print(">>>>> collision with color %s" % str_color(color))
            
            if color == Agent.NO_COLLISION:
                continue
            elif color == Agent.WALL_COLLISION:
                ## The user is blocked by the wall layer
                player_is_blocked = True
                break

            elif color.alpha != 0:
                #print(">>>>> collision with color %d,%d,%d, %d" % (color.red, color.green, color.blue, color.alpha))
                if isinstance(agent, InteractionObject):
                    if agent.bonus is not None:
                        ## Take the bonus
                        player_is_blocked = False
                        self.bonus += agent.bonus
                        self.current_board.remove_agent(agent)
                    else:
                        ## Collision with InteractionObject having a conf_boards
                        board_conf = agent.get_conf_board(color)
                        if board_conf is not None :
                            #print("agent.conf_boards")
                            #print(agent.conf_boards)
                            ## Open a new board
                            ## Get the game to update the board
                            new_position = self.go_to_board(board_conf)
                            #print("new_position: %s" % new_position)
                            new_pos_x = new_position.x
                            new_pos_y = new_position.y
                            break
                        elif agent.inventory_open_color is not None:
                            player_is_blocked = True
                            self.current_board.game.open_inventory()
                            break
                        else:
                            player_is_blocked = True
                            self.set_controls_widget_from_agent(agent)
                            break
                        
                        
                ## The player goes into a new zone
                elif isinstance(agent, ConfBoard):
                    #print(">>>>> collision with ConfBoard %s" % agent.board_name)
                    new_position = self.go_to_board(agent)
                    #print(">>>>> from %d,%d to new_position: %s" % (self.pos_x, self.pos_y, new_position))
                    new_pos_x = new_position.x
                    new_pos_y = new_position.y
                    break


        if not player_is_blocked:
            #print("position: %d,%d -> %d,%d" % (self.pos_x, self.pos_y, new_pos_x, new_pos_y))
            self.pos_x = int(new_pos_x)
            self.pos_y = int(new_pos_y)
            
    def get_new_position_in_new_board(self, board_conf):
        point_to_new_board = board_conf.position_in_board.copy()

        ## If the new position is < 0, keep the same position of the user
        if point_to_new_board.x < 0:
            point_to_new_board.x = self.pos_x

        if point_to_new_board.y < 0:
            point_to_new_board.y = self.pos_y

        return point_to_new_board

    def go_to_board(self, board_conf):
        #print("Going to display %s" % board_conf)
        ## Remove the player from the board
        self.current_board.remove_agent(self)
        ## Set the next active display
        self.current_board.game.set_active_display(board_conf.board_name)
        self.current_board = self.current_board.game.active_display
        ## Add the player to the next board
        self.current_board.add_agent(self)

        point_to_new_board = self.get_new_position_in_new_board(board_conf)
        #print(" ... at position %s" % str(point_to_new_board))

        return point_to_new_board

    def draw(self, screen):
        if not self.is_visible:
            return

        image_bank = self.sprites[self.direction][int(self.animation_flow)]
        top = image_bank[0]
        left = image_bank[1]
        
        screen.blit(self.sprite, top, left, self.metadata.width, self.metadata.height, self.pos_x, self.pos_y, True)

        if self.debug:
            screen.fillRect(self.pos_x + self.shadow_left, self.pos_y + self.shadow_top, 
                self.shadow_width, self.shadow_height, psp2d.Color(0,0,255,128))
            font.drawText(screen, 0, 0, "(%d,%d) - Press O to exit" % (self.pos_x, self.pos_y))

        if self.is_running:
            # One more step of the animation
            self.animation_flow = self.animation_flow + self.animation_velocity
            if self.animation_flow > len(self.sprites[self.direction])-1:
                # Restart the animation from the beginning
                self.animation_flow = 0


    def set_controls_widget_from_agent(self, agent):
        ## Get the actions of the agent
        #print("player_interact_with_agent: %s" % self.player_interact_with_agent)
        
        ## Display the control widget
        self.controls_widget = ControlsWidget(self, (MAX_WIDTH / 2) - 25, (MAX_HEIGHT / 2) - 25)
        self.controls_widget.set_agent(agent)
        self.current_board.game.add_widget(self.controls_widget)

    def close_controls_widget(self):
        self.controls_widget = None

    def add_to_inventory(self, agent):
        self.inventory.add_item(agent)
        