# -*- coding: iso-8859-1 -*-

import os
import re
from configparser import ConfigParser

class Component(object):
    def __init__(self, count, name):
        self.count = count
        self.name = name
        
    def __str__(self):
        return "%d x %s" % (self.count, self.name)

class Formula(object):
    def __init__(self, config_file = None):

        ## Check that config file exists
        if not os.path.isfile(config_file):
            raise ValueError("File not found: %s" % config_file)
        self.ingredients = []
        self.results = []

        config = ConfigParser()
        config.read(config_file)

        in_parameters = config.get("FORMULA", "in").strip()
        self.read_components(self.ingredients, in_parameters)
        
        out_parameters = config.get("FORMULA", "out").strip()
        self.read_components(self.results, out_parameters)

        print("self.ingredients = %s" % self.ingredients)

    def read_components(self, array, parameters):
        for raw_parameter in parameters.split("\n"):
            #print("raw_parameter = %s" % raw_parameter)
            conf = re.search("(.+)\sx\s(.+)", raw_parameter.strip())
            if conf:
                parameter_data = Component(conf.group(1), conf.group(2))
                array.append(parameter_data)