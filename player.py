# -*- coding: iso-8859-1 -*-

from conf_renderer import ConfRenderer
from interaction_object import InteractionObject
import psp2d
from time import time
import math

from configparser import ConfigParser

from agent import Agent
from renderer import Render

## screen size: 480 × 272 pixels
MAX_WIDTH = 480
MAX_HEIGHT = 272

font = psp2d.Font('font.png')

class Player(Agent):
    def __init__(self):
        config = ConfigParser()
        config.read('conf/player.ini')
        self.name = config.get("ASSET", "name")
        Agent.__init__(self, config.get("ASSET", "source") )
        sprite_directions = config.get("ASSET", "sprite_directions")
        self.sprites = {}
        for item in sprite_directions.split("\n"):
            if len(item.strip()) == 0:
                continue
            data = item.strip().split("=")
            key = data[0].strip()
            positions = eval(data[1].strip())
            self.sprites[key] = positions

        self.width = config.getint("DIMENSION", "width")
        self.height = config.getint("DIMENSION", "height")
        self.direction = "DOWN"
        self.is_running = False
        self.animation_flow = 0
        self.velocity = 8
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

        self.bonus = 0
        self.lastPad = time()
        self.debug = False

    def compute_new_position(self):
        pad = psp2d.Controller()
        (dx, dy) = (0, 0)
        if pad.down:
            dy = 1 * self.velocity
            self.direction = "DOWN"
        elif pad.up:
            dy = -1 * self.velocity
            self.direction = "UP"
        elif pad.left:
            dx = -1 * self.velocity
            self.direction = "LEFT"
        elif pad.right:
            dx = 1 * self.velocity
            self.direction = "RIGHT"
        else:
            pass
            """dx = (pad.analogX / 127) * self.velocity
            dy = (pad.analogY / 127) * self.velocity
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

        new_pos_x = min(self.pos_x + dx, MAX_WIDTH - self.width)
        new_pos_x = max(new_pos_x, 0)
        new_pos_y = min(self.pos_y + dy, MAX_HEIGHT - self.height)
        new_pos_y = max(new_pos_y, 0)

        return (new_pos_x, new_pos_y)

    """
    agents is a dict of agent.name -> agent object
    """
    def update(self, agents, walls):
        if (self.lastPad and time() - self.lastPad < 0.05):
            # To short time between 2 events
            return

        self.lastPad = time()
        (new_pos_x, new_pos_y) = self.compute_new_position()

        collisioned_agents = self.detect_collision(agents.values(), walls, 
                                     new_pos_x, 
                                     new_pos_y)
        player_is_blocked = False
        for (agent, color) in collisioned_agents:
            #print("collisioned_agents:")
            #print(collisioned_agents)
            #print(">>>>> collision with color %d,%d,%d, %d" % (color.red, color.green, color.blue, color.alpha))
                
            if color == Agent.NO_COLLISION:
                continue
            elif color == Agent.WALL_COLLISION:
                ## The user is blocked by the wall layer
                player_is_blocked = True
                break

            elif color == Agent.AGENT_COLLISION or color.alpha != 0:
                #print(">>>>> collision with color %d,%d,%d, %d" % (color.red, color.green, color.blue, color.alpha))
                if isinstance(agent, InteractionObject):
                    if agent.bonus is not None:
                        ## Take the bonus
                        player_is_blocked = False
                        self.bonus += agent.bonus
                        self.current_renderer.remove_agent(agent)
                    else:
                        if not (color.red == 0 and color.green == 0 and color.blue == 255):
                            ## Collision with InteractionObject
                            player_is_blocked = True
                            break
                        elif agent.conf_renderers is not None :
                            #print("agent.conf_renderers")
                            #print(agent.conf_renderers)
                            ## Open a new renderer
                            ## Get the game to update the renderer
                            renderer_conf = agent.get_conf_renderer(color)
                            if renderer_conf is not None:
                                new_position = self.go_to_renderer(renderer_conf)
                                #print("new_position: %s" % new_position)
                                new_pos_x = new_position.x
                                new_pos_y = new_position.y
                        else:
                            ## Collision with InteractionObject
                            player_is_blocked = True
                            break
                elif isinstance(agent, ConfRenderer):
                    #print(">>>>> collision with agent %s" % agent.renderer_name)
                    new_position = self.go_to_renderer(agent)
                    #print(">>>>> new_position: %s" % new_position)
                    new_pos_x = new_position.x
                    new_pos_y = new_position.y

            else:
                ## There is a specific collision with an agent
                pass

        if not player_is_blocked:
            self.pos_x = new_pos_x
            self.pos_y = new_pos_y
            
    def go_to_renderer(self, renderer_conf):
        ## Remove the player from the renderer
        self.current_renderer.remove_agent(self)
        ## Set the next active renderer
        self.current_renderer.game.set_active_renderer(renderer_conf.renderer_name)
        self.current_renderer = self.current_renderer.game.active_renderer
        ## Add the player to the next renderer
        self.current_renderer.add_agent(self)
        return renderer_conf.position_in_renderer

    def draw(self, screen):
        image_bank = self.sprites[self.direction][int(self.animation_flow)]
        top = image_bank[0]
        left = image_bank[1]
        screen.blit(self.sprite, top, left, self.width, self.height, self.pos_x, self.pos_y, True)

        if self.debug:
            screen.fillRect(self.pos_x + self.shadow_left, self.pos_y + self.shadow_top, 
                self.shadow_width, self.shadow_height, psp2d.Color(0,0,255,128))
            font.drawText(screen, 0, 0, "(%d,%d) - Press O to exit" % (self.pos_x, self.pos_y))

        if self.is_running:
            # One more step of the animation
            self.animation_flow = self.animation_flow + 0.25
            if self.animation_flow > len(self.sprites[self.direction])-1:
                # Restart the animation from the beginning
                self.animation_flow = 0
                