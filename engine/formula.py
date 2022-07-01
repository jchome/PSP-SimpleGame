# -*- coding: iso-8859-1 -*-

import os
import re
import psp2d
from configparser import ConfigParser

from engine.displays.inventory.inventory_item import InventoryItem
from engine.metadata import Metadata

class Formula(object):
    def __init__(self, config_file = None):
        ## Key = name of the component, value = the count
        self.ingredients = [] ## Array of InventoryItem
        self.results = [] ## Array of InventoryItem
        self.cached_assets = {}
        if config_file is None:
            return

        ## Check that config file exists
        if not os.path.isfile(config_file):
            raise ValueError("File not found: %s" % config_file)

        config = ConfigParser()
        config.read(config_file)

        in_parameters = config.get("FORMULA", "in").strip()
        out_parameters = config.get("FORMULA", "out").strip()
        
        self.read_components(self.ingredients, in_parameters)
        self.read_components(self.results, out_parameters)

        #print("self.ingredients = %s" % self.ingredients)

    """
    Update the formula with the line of the configuration file
    """
    def read_components(self, listOfInventoryItems, parameters):
        config = ConfigParser()
        for raw_parameter in parameters.split("\n"):
            #print("raw_parameter = %s" % raw_parameter)
            conf = re.search("(.+)\sx\s'(.+)'", raw_parameter.strip())
            if not conf:
                print("Conf not readable as excpected: --%s--" % raw_parameter.strip())
                continue
            item = InventoryItem()
            item.counter = int(conf.group(1))
            config.read(conf.group(2))
            item.metadata = Metadata()
            item.metadata.load_config(config)
            listOfInventoryItems.append(item)

            ## Cache the asset of the item
            if item.metadata.name not in self.cached_assets:
                try:
                    self.cached_assets[item.metadata.name] = psp2d.Image(item.metadata.sprite_file)
                except:
                    print("Cannot open file --%s--" % item.metadata.sprite_file)


    """
    Remove an ingredient
    """
    def remove_ingredient(self, ingredient_name):
        if ingredient_name in self.ingredients:
            self.ingredients.remove(ingredient_name)
            return

    """
    Check that the current formula has the same ingredients and same quantities
    """
    def match(self, another_formula):
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
        for inventoryItem in self.ingredients:
            text_to_draw = "%dx " % inventoryItem.count
            font.drawText(screen, img_pos.x, img_pos.y, text_to_draw)
            screen.blit(self.cached_assets[inventoryItem.metadata.name], 
                0, 0, inventoryItem.metadata.width, inventoryItem.metadata.height, 
                img_pos.x + font.textWidth(text_to_draw), img_pos.y - 4, 
                True)
            font.drawText(screen, 
                img_pos.x + font.textWidth(text_to_draw) + inventoryItem.metadata.width + 2, 
                img_pos.y, inventoryItem.metadata.label[lang])
            img_pos.y += 24

        img_pos.y += 12
        font.drawText(screen, img_pos.x, img_pos.y, "==>")
        img_pos.y += 24

        for inventoryItem in self.results:
            text_to_draw = "%dx " % inventoryItem.count
            font.drawText(screen, img_pos.x, img_pos.y, text_to_draw)
            screen.blit(self.cached_assets[inventoryItem.metadata.name], 
                0, 0, inventoryItem.metadata.width, inventoryItem.metadata.height, 
                img_pos.x + font.textWidth(text_to_draw), img_pos.y - 4, 
                True)
            font.drawText(screen, 
                img_pos.x + font.textWidth(text_to_draw) + inventoryItem.metadata.width + 2, 
                img_pos.y, inventoryItem.metadata.label[lang])
            img_pos.y += 24
