# -*- coding: iso-8859-1 -*-

from interaction_object import InteractionObject
import psp2d
import helper
from configparser import ConfigParser
import re


## screen size: 480 × 272 pixels
MAX_WIDTH = 480
MAX_HEIGHT = 272
## X = left axis
## Y = bottom axis

"""
Main class of the game.
Every item is resistered in this container.
"""
class Render():
    def __init__(self, config_file):
        self.screen = psp2d.Screen()
        config = ConfigParser()
        config.read(config_file)
        self.name = config.get("ASSET", "name")
        self.game = None
        self.agents = {}
        self.active = False 
        background_image = config.get("ASSET", "source")
        (self.background, self.walls) = helper.load_sprite(background_image, 
            MAX_WIDTH, MAX_HEIGHT)
        self.final_walls = psp2d.Image(MAX_WIDTH, MAX_HEIGHT)
        self.final_walls.blit(self.walls, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        self.add_interaction_objects(config.get("ASSET", "sprites"))

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
            conf_item = re.search('\'(.*)\'\s*:\s*\(([0-9]+)\s*,\s*([0-9]+)\).*', definition, re.IGNORECASE)
            if conf_item:
                source = conf_item.group(1)
                pos_x = int(conf_item.group(2))
                pos_y = int(conf_item.group(3))
                object_on_renderer = InteractionObject(source, pos_x, pos_y)
                self.add_agent(object_on_renderer)

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
        
        #player = self.agents[0]
        #font.drawText(self.screen, 0, 0, "coins: %d - Press O to exit" % (player.bonus))
        # Sort agents before display
        for agent in sorted(self.agents.values(), key=lambda agent: agent.pos_y + agent.sort_position, reverse=False):
            agent.draw(self.screen)

        self.screen.swap()
