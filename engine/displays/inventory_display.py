# -*- coding: iso-8859-1 -*-

import psp2d

import engine.helper as helper
from engine.displays.selection_display import SelectionDisplay

from engine.widgets.controls_widget import Button
from engine.constants import MAX_HEIGHT, MAX_WIDTH
from engine.formula import Formula
from engine.metadata import Metadata

import engine.translation
_ = engine.translation.translate

IMAGEINDEX_SMALL = 0
IMAGEINDEX_DETAILED = 1


class InventoryDisplay(SelectionDisplay):
    """
    Screen displayed when the user want to show the player's inventory 
    """

    def __init__(self, name):
        SelectionDisplay.__init__(self, name)
        self.font = psp2d.Font('assets/fonts/font-white.png')
        self.title_font = psp2d.Font('assets/fonts/font-Karumbi-46-white.png')
        self.font_black = psp2d.Font('assets/fonts/font-black.png')
        (self.background, _) = helper.load_sprite("assets/displays/inventory.png", 
            MAX_WIDTH, MAX_HEIGHT)
        ## Width, height of the item
        self.item_size = 32
        (self.asset_item_background, self.asset_item_selected) = helper.load_sprite("assets/displays/inventory-item.png", 
            self.item_size, self.item_size)

        self.cursor = 0
        self.current_item = None
        self.nb_items_per_row = 6
        self.max_items = 36

        ## Cache assets of inventory (key = name, value = [image, detailed_image])
        self.cached_assets = {}
        self.assets_loaded = False

        self.controls_assets = {}
        self.controls_assets[Button.TRIANGLE] = psp2d.Image("assets/control-triangle.png")
        self.controls_assets[Button.SQUARE] = psp2d.Image("assets/control-square.png")
        self.controls_assets[Button.CIRCLE] = psp2d.Image("assets/control-circle.png")
        self.controls_assets[Button.CROSS] = psp2d.Image("assets/control-cross.png")
        self.controls_assets[Button.L] = psp2d.Image("assets/control-L.png")
        self.controls_assets[Button.R] = psp2d.Image("assets/control-R.png")
        self.allowed_to_craft = False
        self.timer = -1
        self.round_anim = psp2d.Image("assets/round-anim-green.png")

        self.current_category = Metadata.CATEGORY_OBJECT
        
    def update_nothing_happens(self):
        """
        Update when the player does nothing. 
        """
        ## Prepare the timer
        self.timer = -1

        ## Get the current inventory size, during the first update method
        limit = self.game.player.inventory.limit_size[self.current_category]
        if limit < self.nb_items_per_row:
            self.nb_items_per_row = limit
            self.max_items = limit
        else:
            self.nb_items_per_row = 6
            if limit < self.max_items:
                self.max_items = limit
        
        self.get_current_item(force_check_allowed_to_craft = True)


    def update_for_key_pressed(self, keys_pressed):
        """
        Update method when the user press a key.
        """
        ## For the triangle button, start the craft
        if "TRIANGLE" in keys_pressed:
            if self.timer == -1:
                self.timer = 0
            else:
                self.timer += 0.25
        
        ## Start the crafting
        if self.timer >= 20:
            self.start_crafting()

        if "R" in keys_pressed:
            ## Wait the key is pressed long enough
            if self.timer == -1:
                self.timer = 0
            else:
                self.timer += 0.25

            if self.timer >= 5:
                self.timer = 0
                if self.current_category == Metadata.CATEGORY_OBJECT:
                    self.current_category = Metadata.CATEGORY_CRAFT
                else:
                    self.current_category = Metadata.CATEGORY_OBJECT
                self.cursor = 0
            

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
            
        elif controller.circle:
            self.game.close_inventory()
        

    def get_current_item(self, force_check_allowed_to_craft):
        if not force_check_allowed_to_craft:
            ## Nothing changed
            return

        ## Set the current_item with the cursor value
        self.allowed_to_craft = False
        #print("self.cursor: %d" % self.cursor)
        #print("len(self.game.player.inventory.all_items[Metadata.CATEGORY_OBJECT]): %d" %  len(self.game.player.inventory.all_items[Metadata.CATEGORY_OBJECT]))
        if self.cursor >= len(self.game.player.inventory.all_items[self.current_category]):
            self.current_item = None
            return
        else:
            self.current_item = self.game.player.inventory.all_items[self.current_category].values()[self.cursor]

        if self.current_category == Metadata.CATEGORY_CRAFT:
            formula = self.current_item.metadata.production_plan
            formula.check_ingredients_availability(self.game.player.inventory)
            if not formula.all_ingredients_available:
                ## All ingredients are not available
                self.allowed_to_craft = False
            else:
                self.allowed_to_craft = True
        
    
    def update_cursor(self, direction):
        previous_cursor_position = self.cursor

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

        if self.cursor < 0:
            self.cursor = 0
        if self.cursor >= self.game.player.inventory.limit_size[self.current_category]:
            self.cursor = self.game.player.inventory.limit_size[self.current_category]-1
        self.get_current_item(previous_cursor_position == self.cursor)


    def start_crafting(self):
        """
        Craft something with ingredients
        """
        #print("self.allowed_to_craft = %s" % self.allowed_to_craft)
        if not self.allowed_to_craft:
            return

        formula = self.current_item.metadata.production_plan

        ## End of crafting, add the result, remove each ingredient of the inventory
        formula.craft(self.game.player.inventory)
        self.timer = -1


    def draw(self):
        ## Draw background
        self.screen.blit(self.background, 0, 0, MAX_WIDTH, MAX_HEIGHT, 0, 0, True)
        category = _("category.title.%s" % self.current_category, self.game.current_language)
        title = _("inventory.title", self.game.current_language) + " - " + category

        pos_x = 10 #(MAX_WIDTH - self.title_font.textWidth(title)) / 2
        pos_y = -10
        self.title_font.drawText(self.screen, pos_x, pos_y, title)

        ## Draw the help keys
        ## Go to RIGHT
        pos_x = MAX_WIDTH - 44
        self.screen.blit(self.controls_assets[Button.R], 0, 0, 44, 16, pos_x, 0, True)
        if self.current_category == Metadata.CATEGORY_OBJECT:
            text_left = _("category.title.%s" % Metadata.CATEGORY_CRAFT, self.game.current_language)
        else:
            text_left = _("category.title.%s" % Metadata.CATEGORY_OBJECT, self.game.current_language)
        pos_x -= self.font.textWidth(text_left) - 4
        self.font.drawText(self.screen, pos_x, 0, text_left)

        ## Exit button
        pos_x = 4
        self.screen.blit(self.controls_assets[Button.CIRCLE], 0, 0, 16, 16, pos_x, 252, True)
        pos_x += 16
        text_exit = _("inventory.action.exit", self.game.current_language)
        self.font.drawText(self.screen, pos_x, 253, text_exit)
        pos_x += self.font.textWidth(text_exit) + 10


        ## Interaction button
        if self.current_item is not None and self.current_item.metadata.name == "FORMULA":
            formula = self.current_item.metadata.production_plan
            formula.check_ingredients_availability(self.game.player.inventory)
            if formula.all_ingredients_available:
                pos_x = MAX_WIDTH / 2
                pos_y = 252

                if self.timer > -1:
                    dx = int(self.timer) * 20
                    self.screen.blit(self.round_anim, int(dx), 0, 20, 20, pos_x-2, pos_y-1, True)

                self.screen.blit(self.controls_assets[Button.TRIANGLE], 0, 0, 16, 16, pos_x, pos_y, True)
                pos_x += 16
                text_interaction = _("inventory.action.interaction", self.game.current_language)
                self.font.drawText(self.screen, pos_x + 8, 253, text_interaction)
                pos_x += self.font.textWidth(text_interaction) + 10
        
        self.draw_inventory()
        self.draw_detail()

    def load_asset(self, item):
        asset = psp2d.Image(item.metadata.sprite_file)
        detail_asset = None
        if item.metadata.fullscreen_source:
            detail_asset = psp2d.Image(item.metadata.fullscreen_source)
        ## Use ImageIndex enum
        self.cached_assets[item.metadata.name] = [asset, detail_asset]

    """
    Draw the list of items of the inventory in the left part of the screen
    """
    def draw_inventory(self):
        ## Get items collected by the player
        ## Top left position of the first item
        (pos_x, pos_y) = (4, 38)

        things_to_draw = self.game.player.inventory.all_items[self.current_category]
        if not self.assets_loaded:
            self.cached_assets = {}
            for (item_name, item) in things_to_draw.items():
                self.load_asset(item)
            self.assets_loaded = True

        index = 0
        for index in range(0, self.game.player.inventory.limit_size[self.current_category]):
            if index == self.cursor:
                ## Display the selection image of the item
                self.screen.blit(self.asset_item_selected, 0, 0, self.item_size, self.item_size,
                    pos_x, pos_y, True)
            else:
                ## Display the background of the item
                self.screen.blit(self.asset_item_background, 0, 0, self.item_size, self.item_size,
                    pos_x, pos_y, True)

            ## Draw the item of the player's inventory
            if index < len(things_to_draw):
                item = things_to_draw.values()[index]
                #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
                if item.metadata.name not in self.cached_assets:
                    self.load_asset(item)
                asset = self.cached_assets[item.metadata.name][IMAGEINDEX_SMALL]
                ## Display the sprite of the agent
                self.draw_asset(asset, pos_x, pos_y, item.metadata, item.count)

            
            ## Prepare next item
            if (index + 1) % self.nb_items_per_row == 0:
                pos_y += 36
                pos_x = 4
            else:
                pos_x += 36
            index += 1

    """
    Draw the detail of the item (an agent)
    """
    def draw_detail(self):
        (pos_x, pos_y) = ((MAX_WIDTH / 2) + 4, 38)
        if self.current_item is None:
            nothing_selected = _("inventory.nothing_selected", self.game.current_language)
            self.font.drawText(self.screen, pos_x, pos_y, nothing_selected)
            return

        label = self.current_item.metadata.name + ".metadata.label"
        if self.game.current_language in self.current_item.metadata.label:
            label = self.current_item.metadata.label[self.game.current_language]
        self.font.drawText(self.screen, pos_x, pos_y, label)
        
        ## Draw the asset of the detail view, if exists. Its size is 150x150
        asset = self.cached_assets[self.current_item.metadata.name][IMAGEINDEX_DETAILED]
        img_pos = helper.Point((MAX_WIDTH * 3 / 4) - 75, (MAX_HEIGHT / 2) - 75)
        if asset is not None:
            self.screen.blit(asset, 0, 0, 150, 150, 
                img_pos.x, 
                img_pos.y, True)
        ## Draw the description
        description = self.current_item.metadata.name + ".metadata.description"
        if self.game.current_language in self.current_item.metadata.description:
            description = self.current_item.metadata.description[self.game.current_language]
        pos_y = 240
        pos_x = (MAX_WIDTH * 3 / 4) - (self.font.textWidth(description) / 2)
        self.font.drawText(self.screen, pos_x, pos_y, description)

        if self.current_item.metadata.category == Metadata.CATEGORY_CRAFT:
            formula = self.current_item.metadata.production_plan
            formula.check_ingredients_availability(self.game.player.inventory)
            formula.draw_ingredients(self.screen, img_pos, 
                self.font_black, self.game.current_language)


    """
    Draw the asset of an ingredient
    """
    def draw_asset(self, asset, pos_x, pos_y, agent_metadata, count):
        #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
        ## Display the sprite of the agent
        (width, height) = (agent_metadata.width, agent_metadata.height)
        center_offset_x = (self.item_size - width) / 2
        center_offset_y = (self.item_size - height) / 2
        self.screen.blit(asset, 0, 0, width, height, 
            pos_x + center_offset_x, 
            pos_y + center_offset_y, True)
        ## Display the counter of item
        text_x = pos_x + 23
        text_y = pos_y + 18
        if count >= 10 :
            text_x -= self.font.textWidth("0")
        if count >= 100 :
            text_x -= self.font.textWidth("0")
        self.font.drawText(self.screen, text_x, text_y, str(count))


    """
    Draw the selection for crafting in the right part of the screen
    """
    def draw_crafting(self):
        (pos_x, pos_y) = (244, 38)
        index = 0
        for (name, count) in self.craft_formula.ingredients.items():
            ## Display the background of the item
            self.screen.blit(self.asset_item_background, 0, 0, self.item_size, self.item_size,
                pos_x, pos_y, True)

            item = self.game.player.inventory.all_items[Metadata.CATEGORY_OBJECT][name]
            #print("agent_metadata.sprite_file: %s" % agent_metadata.sprite_file)
            ## Display the sprite of the agent
            asset = self.cached_assets[item.metadata.name][IMAGEINDEX_SMALL]
            self.draw_asset(asset, pos_x, pos_y, item.metadata, count)

            ## Prepare next item
            if (index + 1) % self.nb_items_per_row == 0:
                pos_y += 36
                pos_x = 244
            else:
                pos_x += 36
            index += 1

