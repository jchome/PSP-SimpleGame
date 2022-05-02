# -*- coding: iso-8859-1 -*-

import os
import re
from configparser import ConfigParser

class Formula(object):
    def __init__(self, config_file = None):
        ## Key = name of the component, value = the count
        self.ingredients = {}
        self.results = {}
        if config_file is None:
            return

        ## Check that config file exists
        if not os.path.isfile(config_file):
            raise ValueError("File not found: %s" % config_file)

        config = ConfigParser()
        config.read(config_file)

        in_parameters = config.get("FORMULA", "in").strip()
        self.read_components(self.ingredients, in_parameters)
        
        out_parameters = config.get("FORMULA", "out").strip()
        self.read_components(self.results, out_parameters)

        #print("self.ingredients = %s" % self.ingredients)

    """
    Update the formula with the line of the configuration file
    """
    def read_components(self, dict, parameters):
        for raw_parameter in parameters.split("\n"):
            #print("raw_parameter = %s" % raw_parameter)
            conf = re.search("(.+)\sx\s(.+)", raw_parameter.strip())
            if conf:
                dict[conf.group(2)] = conf.group(1)

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

