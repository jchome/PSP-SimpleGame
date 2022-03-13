# -*- coding: iso-8859-1 -*-

import psp2d

from engine.displays.display import Display
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper


class InventoryDisplay(Display):

    def __init__(self, name):
        Display.__init__(self, name)
        self.font = psp2d.Font('font.png')
        (self.background, _) = helper.load_sprite("assets/displays/inventory.png", 
            MAX_WIDTH, MAX_HEIGHT)
        self.item_size = 32
        (self.item, self.item_selected) = helper.load_sprite("assets/displays/inventory-item.png", 
            self.item_size, self.item_size)


    def update(self):
        ## The update method is called only for active displays
        controller = psp2d.Controller()
        if controller.down:
            direction = "DOWN"
        elif controller.up:
            direction = "UP"
        elif controller.left:
            direction = "LEFT"
        elif controller.right:
            direction = "RIGHT"
        elif controller.cross:
            self.game.close_inventory()
        

    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)

        ## Get items collected by the player
        (pos_x, pos_y) = (4, 38)
        for item in self.game.player.inventory.all_items:
            agent_metadata = item.metadata
            #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
            ## Display the sprite of the agent
            asset = psp2d.Image(agent_metadata.sprite_file)
            (width, height) = (agent_metadata.width, agent_metadata.height)
            center_offset_x = (self.item_size - width) / 2
            center_offset_y = (self.item_size - height) / 2
            self.screen.blit(asset, 0, 0, width, height, 
                pos_x + center_offset_x, 
                pos_y + center_offset_y, True)

            ## Display the counter of item
            text_x = pos_x + 23
            text_y = pos_y + 18
            if item.count > 10 :
                text_y += self.font.textWidth("0")
            if item.count > 100 :
                text_y += self.font.textWidth("0")
            self.font.drawText(self.screen, text_x, text_y, str(item.count))
            
            ## Prepare next item
            pos_x += 36

        ## Add the selected item
        #self.screen.blit(self.item_selected, 0, 0, 32, 32, pos_x, pos_y, True)
