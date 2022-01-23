# -*- coding: iso-8859-1 -*-

from engine.conf_renderer import ConfRenderer
from engine.interaction_object import InteractionObject
import psp2d
import engine.helper as helper
from configparser import ConfigParser
import re


## screen size: 480 × 272 pixels
MAX_WIDTH = 480
MAX_HEIGHT = 272
## X = left axis
## Y = bottom axis

font = psp2d.Font('font.png')

"""
Main class of the game.
Every item is resistered in this container.
"""
class Render():
    def __init__(self, config_file):
        self.screen = psp2d.Screen()
        config = ConfigParser()
        config.read(config_file)
        self.name = config_file
        self.game = None
        self.agents = {}
        self.active = False 
        background_image = config.get("ASSET", "source")
        (self.background, self.walls) = helper.load_sprite(background_image, 
            MAX_WIDTH, MAX_HEIGHT)
        self.final_walls = psp2d.Image(MAX_WIDTH, MAX_HEIGHT)
        self.final_walls.blit(self.walls, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        self.add_interaction_objects(config.get("ASSET", "sprites"))

        ## Visual effect to change the renderer
        self.curtain_value = 0
        self.curtain_mode = "OPEN"

        self.debug = False

        self.conf_renderers = []
        if config.has_option("COLLISION", "open_renderer"):
            open_renderer_conf = config.get("COLLISION", "open_renderer")
            #print("Getting COLLISION / open_renderer from %s" % open_renderer_conf)
            renderer_conf = ConfRenderer(open_renderer_conf)
            if renderer_conf.renderer_name is not None:
                #print(renderer_conf)
                self.conf_renderers.append(renderer_conf)
                
                
    """
    @return Conf_Renderer instance
    """
    def get_conf_renderer(self, color_to_match):
        for renderer_conf in self.conf_renderers:
            color = renderer_conf.renderer_color
            if helper.match_colors(color, color_to_match):
                return renderer_conf
        return None

    def add_interaction_objects(self, raw_conf):
        #print("Reading %s" % raw_conf)
        for item in raw_conf.split("\n"):
            if len(item.strip()) == 0:
                continue
            #print("  item: %s" % item)
            data = item.strip().split("=")
            number = data[0]
            definition = data[1].strip()
            #print("  definition: %s" % definition)
            conf_item = re.search('\'(.*)\'\s*:\s*\((-?\d+)\s*,\s*(-?\d+)\).*', definition, re.IGNORECASE)
            if conf_item:
                source = conf_item.group(1)
                pos_x = int(conf_item.group(2))
                pos_y = int(conf_item.group(3))
                #print("%s: (%d,%d)" % (source, pos_x, pos_y))
                object_on_renderer = InteractionObject(source, pos_x, pos_y)
                ## Update the agent name to have unique objects name
                object_on_renderer.name += "_#" + number
                self.add_agent(object_on_renderer)
            else:
                print("Cannot get position from string <%s>" % definition)

    """
    Add the static agent with its wall
    """
    def add_static_agent(self, agent):
        self.final_walls.blit(agent.walls, 0, 0, 
            agent.width, agent.height, 
            agent.pos_x, agent.pos_y, True)
        self.add_agent(agent)
    
    def add_agent(self, agent):
        self.agents[agent.name] = agent
        agent.current_renderer = self

    def remove_agent(self, agent):
        del(self.agents[agent.name])

    def exit(self):
        # When the player calls the exit, tell all Agents to stop running
        self.active = False
        for agent in self.agents.values():
            agent.running = False
            if self.game is not None:
                self.game.is_finished = True

    """
    Get the wall's color at the position
    """
    def get_color_at_position(self, position):
        return self.final_walls.getPixel(position.x, position.y)

    """
    Update all registered agents, then draw all
    """
    def update(self):
        pad = psp2d.Controller()
        if pad.circle:
            print("exit")
            self.exit()

        ## Update agents considering all walls
        for agent in self.agents.values():
            agent.update(self.agents, self.walls)

    def draw(self):
        # Each frame the renderer apply the background,
        # writes the text and draws each registered agent.
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        if self.debug:
            self.screen.blit(self.final_walls, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        
        #player = self.agents[0]
        #font.drawText(self.screen, 0, 0, "coins: %d - Press O to exit" % (player.bonus))
        # Sort agents before display
        for agent in sorted(self.agents.values(), key=lambda agent: agent.pos_y + agent.sort_position, reverse=False):
            agent.draw(self.screen)

        if self.curtain_mode == "CLOSING":
            ## Close the curtain
            black = psp2d.Color(0,0,0)
            self.screen.fillRect(0, MAX_HEIGHT/2, MAX_WIDTH, MAX_HEIGHT/2, black)
            self.curtain_value += 10
            if self.curtain_value == 100:
                self.curtain_mode = "CLOSED"
            
        ## Draw the player's coins
        #font.drawText(self.screen, 0,0, "coins: %d" % self.game.player.bonus)

        #self.screen.drawLine(10,20,200,300, black)

        self.screen.swap()
