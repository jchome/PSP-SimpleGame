# -*- coding: iso-8859-1 -*-

import psp2d

from engine.displays.selection_display import SelectionDisplay
from engine.constants import MAX_HEIGHT, MAX_WIDTH
import engine.helper as helper


class InventoryDisplay(SelectionDisplay):

    def __init__(self, name):
        SelectionDisplay.__init__(self, name)
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

        self.craft_selection = []
        

    def update_for_selection(self, controller):
        ## The update method is called only for active displays
        if controller.down:
            self.update_cursor("DOWN")
        elif controller.up:
            self.update_cursor("UP")
        elif controller.left:
            self.update_cursor("LEFT")
        elif controller.right:
            self.update_cursor("RIGHT")

        elif controller.triangle:
            self.select_for_crafting()
            
        elif controller.cross:
            self.game.close_inventory()

    
    def update_cursor(self, direction):
        if direction == "DOWN":
            if self.cursor + self.nb_items_per_row > self.max_items:
                self.cursor = self.cursor % self.nb_items_per_row 
            else:
                self.cursor = self.cursor + self.nb_items_per_row

        elif direction == "UP":
            if self.cursor < self.nb_items_per_row:
                self.cursor = (self.max_items - self.nb_items_per_row) + self.cursor
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

    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)

        self.draw_inventory()
        self.draw_crafting()

    """
    Draw the list of items of the inventory in the left part of the screen
    """
    def draw_inventory(self):
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
                #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
                ## Display the sprite of the agent
                asset = self.cached_assets[index]
                self.draw_asset(asset, pos_x, pos_y, item.metadata)

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

    def draw_asset(self, asset, pos_x, pos_y, agent_metadata):
        #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
        ## Display the sprite of the agent
        (width, height) = (agent_metadata.width, agent_metadata.height)
        center_offset_x = (self.item_size - width) / 2
        center_offset_y = (self.item_size - height) / 2
        self.screen.blit(asset, 0, 0, width, height, 
            pos_x + center_offset_x, 
            pos_y + center_offset_y, True)

    """
    Draw the selection for crafting in the right part of the screen
    """
    def draw_crafting(self):
        (pos_x, pos_y) = (244, 38)
        index = 0
        for cursor in self.craft_selection:
            ## Display the background of the item
            self.screen.blit(self.item_background, 0, 0, self.item_size, self.item_size,
                pos_x, pos_y, True)

            item = self.game.player.inventory.all_items[cursor]
            #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
            ## Display the sprite of the agent
            asset = self.cached_assets[cursor]
            self.draw_asset(asset, pos_x, pos_y, item.metadata)

            ## Prepare next item
            if (index + 1) % self.nb_items_per_row == 0:
                pos_y += 36
                pos_x = 244
            else:
                pos_x += 36
            index += 1

    def select_for_crafting(self):
        if self.cursor in self.craft_selection:
            self.craft_selection.remove(self.cursor)
        else:
            self.craft_selection.append(self.cursor)
