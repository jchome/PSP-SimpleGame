# -*- coding: iso-8859-1 -*-

from engine.conf_board import ConfBoard
from engine.constants import MAX_HEIGHT, MAX_WIDTH
from engine.display import Display
from engine.interaction_object import InteractionObject
import psp2d
import engine.helper as helper
from configparser import ConfigParser
import re


"""
Main class of the game.
Every item is resistered in this container.
"""
class Board(Display):
    def __init__(self, config_file):
        ## Set the name: use the config file
        Display.__init__(self, config_file)
        config = ConfigParser()
        config.read(config_file)
        self.agents = {}
        background_image = config.get("ASSET", "source")
        (self.background, self.walls) = helper.load_sprite(background_image, 
            MAX_WIDTH, MAX_HEIGHT)
        self.add_interaction_objects(config.get("ASSET", "sprites"))

        self.conf_boards = []
        self.add_board_conf(config.get("COLLISION", "open_board"))
        
                
    """
    @return Conf_Board instance
    """
    def get_conf_board(self, color_to_match):
        #print("Board.get_conf_board()")
        for board_conf in self.conf_boards:
            color = board_conf.board_color
            #print("board_conf.board_color = %s" % helper.str_color(color))
            if helper.match_colors(color, color_to_match):
                #print("board found: %s" % board_conf.board_name)
                return board_conf
        print("No board matched...")
        return None


    def add_board_conf(self, raw_conf):
        for open_board_conf in raw_conf.split("\n"):
            if len(open_board_conf.strip()) == 0:
                continue
            #print("Getting COLLISION / open_board from %s" % open_board_conf)
            board_conf = ConfBoard(open_board_conf)
            if board_conf.board_name is not None:
                self.conf_boards.append(board_conf)
                #print("Added board %s" % board_conf)


    def add_interaction_objects(self, raw_conf):
        #print("Reading %s" % raw_conf)
        for item in raw_conf.split("\n"):
            if len(item.strip()) == 0:
                continue
            #print("  item: %s" % item)
            data = item.strip().split("=")
            #number = data[0]
            definition = data[1].strip()
            #print("  definition: %s" % definition)
            conf_item = re.search('\'(.*)\'\s*:\s*\((-?\d+)\s*,\s*(-?\d+)\).*', definition, re.IGNORECASE)
            if conf_item:
                source = conf_item.group(1)
                pos_x = int(conf_item.group(2))
                pos_y = int(conf_item.group(3))
                #print("%s: (%d,%d)" % (source, pos_x, pos_y))
                object_on_board = InteractionObject(source, pos_x, pos_y)
                ## Update the agent name to have unique objects name
                self.add_agent(object_on_board)
            else:
                print("Cannot get position from string <%s>" % definition)

    def add_agent(self, agent):
        number = len(self.agents)
        agent.id = "%s_#%d" % (agent.metadata.name, number)
        self.agents[agent.id] = agent
        agent.current_board = self

    def remove_agent(self, agent):
        del(self.agents[agent.id])

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
        return self.walls.getPixel(position.x, position.y)

    """
    Update all registered agents, then draw all
    """
    def update(self):
        
        ## Update agents considering all walls
        for agent in self.agents.values():
            agent.update(self.agents, self.walls)

    def draw(self):
        # Each frame the board apply the background,
        # writes the text and draws each registered agent.
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        #self.screen.clear(psp2d.Color(0,0,0,0))
        if self.debug:
            self.screen.blit(self.walls, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
            #print("color at (478,177): %s" % helper.str_color(self.get_color_at_position(helper.Point(478,177))) )
        
        # Sort agents before display
        for agent in sorted(self.agents.values(), key=lambda agent: agent.pos_y + agent.sort_position, reverse=False):
            agent.draw(self.screen)

        #self.screen.drawLine(10,20,200,300, black)
