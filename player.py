# -*- coding: iso-8859-1 -*-

import psp2d
from time import time
import math

from agent import Agent

## screen size: 480 × 272 pixels
MAX_WIDTH = 480
MAX_HEIGHT = 272

class Player(Agent):
    def __init__(self):
        Agent.__init__(self, 'assets/player.png')
        self.split = {
            "RIGHT": [[0,64], [0,32], [0,0], [0,32]],
            "LEFT": [[96,64], [96,32], [96,0], [96,32]],
            "UP": [[32,64], [32,32], [32,0], [32,32]],
            "DOWN": [[64,64], [64,32], [64,0], [64,32]]
            }
        self.width = 32
        self.height = 32
        self.direction = "DOWN"
        self.is_running = False
        self.animation_flow = 0
        self.velocity = 8
        self.pos_x = 30
        self.pos_y = 130
        self.shadow_with = 16
        self.shadow_height = 31
        self.lastPad = time()

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

    def update(self, walls):
        if (self.lastPad and time() - self.lastPad < 0.05):
            # To short time between 2 events
            return

        self.lastPad = time()
        (new_pos_x, new_pos_y) = self.compute_new_position()

        if not self.detect_collision(walls, 
                                     new_pos_x + (self.shadow_with/2), 
                                     new_pos_y + (self.shadow_height/2)):
            self.pos_x = new_pos_x
            self.pos_y = new_pos_y
            
        
    def draw(self, screen):
        image_bank = self.split[self.direction][int(self.animation_flow)]
        top = image_bank[0]
        left = image_bank[1]
        screen.blit(self.sprite, top, left, self.width, self.height, self.pos_x, self.pos_y, True)
        if self.is_running:
            # One more step of the animation
            self.animation_flow = self.animation_flow + 0.25
            if self.animation_flow > len(self.split[self.direction])-1:
                # Restart the animation from the beginning
                self.animation_flow = 0
                