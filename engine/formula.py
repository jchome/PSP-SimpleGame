# -*- coding: iso-8859-1 -*-

import os
import re
import psp2d
from configparser import ConfigParser

from engine import constants
from engine.displays.inventory.inventory_item import InventoryItem
from engine.displays.inventory.inventory_item_formula import InventoryItemFormula
from engine.metadata import Metadata

class Formula(object):
    def __init__(self, config_file = None):
        ## Key = name of the component, value = the count
        self.ingredients = [] ## Array of InventoryItem
        self.results = [] ## Array of InventoryItem
        self.cached_assets = {}
        self.cached_assets["CKECK-ICON"] = psp2d.Image("assets/inventory-check.png")
        self.cached_assets["ARROW-ICON"] = psp2d.Image("assets/inventory-arrow.png")

        ## If craft is possible, the player needs to have all required ingredients
        self.all_ingredients_available = False
        if config_file is None:
            return

        ## Check that config file exists
        if not os.path.isfile(config_file):
            raise ValueError("File not found: %s" % config_file)

        config = ConfigParser()
        config.read(config_file)

        in_parameters = config.get("CRAFT", "in").strip()
        out_parameters = config.get("CRAFT", "out").strip()
        
        self.read_components(self.ingredients, in_parameters)
        self.read_components(self.results, out_parameters)

        #print("self.ingredients = %s" % self.ingredients)

    """
    Update the formula with the line of the configuration file
    """
    def read_components(self, list_of_inventory_items, parameters):
        config = ConfigParser()
        for raw_parameter in parameters.split("\n"):
            #print("raw_parameter = %s" % raw_parameter)
            conf = re.search("(.+)\sx\s'(.+)'", raw_parameter.strip())
            if not conf:
                print("Conf not readable as excpected: --%s--" % raw_parameter.strip())
                continue
            metadata_of_component = Metadata()
            try:
                config.read(conf.group(2))
                metadata_of_component.load_config(config)
            except:
                print("Error while reading config file %s" % conf.group(2))

            item = InventoryItemFormula(metadata_of_component)
            item.count = int(conf.group(1))

            list_of_inventory_items.append(item)

            ## Cache the asset of the item
            if metadata_of_component.name not in self.cached_assets:
                try:
                    self.cached_assets[metadata_of_component.name] = psp2d.Image(metadata_of_component.sprite_file)
                except:
                    print("Cannot open file --%s--" % metadata_of_component.sprite_file)

    def check_ingredients_availability(self, player_inventory):
        self.all_ingredients_available = False
        availability_successed = True
        for inventory_item in self.ingredients:
            inventory_item.enough_in_inventory = player_inventory.contains(inventory_item.metadata.name, inventory_item.count)
            if not inventory_item.enough_in_inventory:
                availability_successed = False
        
        self.all_ingredients_available = availability_successed
    
    def craft(self, player_inventory):
        """
        Remove ingredients and add the result
        """
        for inventory_item in self.ingredients:
            player_inventory.remove_item(inventory_item)

        for inventory_item in self.results:
            player_inventory.add_item(inventory_item)

        self.check_ingredients_availability(player_inventory)

    """
    Remove an ingredient
    """
    def remove_ingredient(self, ingredient_name):
        if ingredient_name in self.ingredients:
            self.ingredients.remove(ingredient_name)
            return

    def match(self, another_formula):
        """
        Check that the current formula has the same ingredients and same quantities
        """
        for (quantity, component) in self.ingredients:
            if not component in another_formula.ingredients:
                ## The ingredient is not present
                return False
            if quantity != another_formula.ingredients[component]:
                ## Not the same quantity
                return False
        return True

    def draw_ingredients(self, screen, img_pos, font, lang):
        img_pos.x += 4
        img_pos.y += 6
        
        for inventory_item in self.ingredients:
            text_to_draw = "%dx " % inventory_item.count
            font.drawText(screen, img_pos.x, img_pos.y, text_to_draw)
            screen.blit(self.cached_assets[inventory_item.metadata.name], 
                0, 0, inventory_item.metadata.width, inventory_item.metadata.height, 
                img_pos.x + font.textWidth(text_to_draw), img_pos.y - 4, 
                True)
            font.drawText(screen, 
                img_pos.x + font.textWidth(text_to_draw) + inventory_item.metadata.width + 2, 
                img_pos.y, inventory_item.metadata.label[lang])

            ## Display the check asset if there is enough item
            if inventory_item.enough_in_inventory:
                screen.blit(self.cached_assets["CKECK-ICON"], 
                    0, 0, 24, 24, 
                    410, img_pos.y - 4, 
                    True)
            img_pos.y += 24

        screen.blit(self.cached_assets["ARROW-ICON"], 
                    0, 0, 24, 24, 
                    img_pos.x + 32, img_pos.y, 
                    True)
        img_pos.y += 32

        for inventory_item in self.results:
            text_to_draw = "%dx " % inventory_item.count
            font.drawText(screen, img_pos.x, img_pos.y, text_to_draw)
            screen.blit(self.cached_assets[inventory_item.metadata.name], 
                0, 0, inventory_item.metadata.width, inventory_item.metadata.height, 
                img_pos.x + font.textWidth(text_to_draw), img_pos.y - 4, 
                True)
            font.drawText(screen, 
                img_pos.x + font.textWidth(text_to_draw) + inventory_item.metadata.width + 2, 
                img_pos.y, inventory_item.metadata.label[lang])
            img_pos.y += 24
