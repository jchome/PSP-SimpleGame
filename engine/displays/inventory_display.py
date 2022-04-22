# -*- coding: iso-8859-1 -*-

from time import sleep, time
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
        (self.item_background, self.item_selected) = helper.load_sprite("assets/displays/inventory-item.png", 
            self.item_size, self.item_size)

        self.cursor = 0
        self.nb_items_per_row = 6
        self.max_items = 36

        ## Cache assets of inventory
        self.cached_assets = []
        self.assets_loaded = False
        self.first_display_time = None
        

    def update(self):
        ## Slow down the update feature
        if self.first_display_time is None:
            self.first_display_time = time()
            sleep(0.2)
            return
        if time() - self.first_display_time < 0.1:
            return
        self.first_display_time = time()
        
        
        ## The update method is called only for active displays
        controller = psp2d.Controller()
        if controller.down or controller.up or controller.left or controller.right:
            if controller.down:
                direction = "DOWN"
            elif controller.up:
                direction = "UP"
            elif controller.left:
                direction = "LEFT"
            elif controller.right:
                direction = "RIGHT"
            self.update_cursor(direction)

        elif controller.cross:
            self.game.close_inventory()
        
    
    def update_cursor(self, direction):
        print("cursor before = %d" % self.cursor)
        if direction == "DOWN":
            if self.cursor + self.nb_items_per_row > self.max_items:
                self.cursor = self.cursor % self.nb_items_per_row
            else:
                self.cursor = self.cursor + self.nb_items_per_row

        elif direction == "UP":
            if self.cursor < self.nb_items_per_row:
                self.cursor = (self.max_items - self.nb_items_per_row) + self.cursor + 1
            else:
                self.cursor = self.cursor - self.nb_items_per_row

        elif direction == "LEFT":
            if self.cursor % self.nb_items_per_row == 0:
                self.cursor = self.cursor - 1 + self.nb_items_per_row
            else:
                self.cursor = self.cursor - 1

        elif direction == "RIGHT":
            if (self.cursor + 1) % self.nb_items_per_row == 0:
                self.cursor = self.cursor + 1 - self.nb_items_per_row
            else:
                self.cursor = self.cursor + 1
        print("      cursor after = %d" % self.cursor)

    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)

        ## Get items collected by the player
        ## Top left position of the first item
        (pos_x, pos_y) = (4, 38)

        if not self.assets_loaded:
            for item in self.game.player.inventory.all_items:
                asset = psp2d.Image(item.metadata.sprite_file)
                self.cached_assets.append(asset)
            self.assets_loaded = True

        index = 0
        #for item in self.game.player.inventory.all_items:
        for index in range(0, self.max_items):
            if index == self.cursor:
                ## Display the selection image of the item
                self.screen.blit(self.item_selected, 0, 0, self.item_size, self.item_size,
                    pos_x, pos_y, True)
            else:
                ## Display the background of the item
                self.screen.blit(self.item_background, 0, 0, self.item_size, self.item_size,
                    pos_x, pos_y, True)

            if index < len(self.game.player.inventory.all_items):
                item = self.game.player.inventory.all_items[index]
                agent_metadata = item.metadata
                #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
                ## Display the sprite of the agent
                asset = self.cached_assets[index]
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
            if (index + 1) % self.nb_items_per_row == 0:
                pos_y += 36
                pos_x = 4
            else:
                pos_x += 36
            index += 1

        ## Add the selected item
        #self.screen.blit(self.item_selected, 0, 0, 32, 32, pos_x, pos_y, True)
