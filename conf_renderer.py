# -*- coding: iso-8859-1 -*-

import re
import helper
import psp2d

class ConfRenderer(object):

    def __init__(self, conf_string):
        self.renderer_name = None
        self.renderer_color = None
        self.position_in_renderer = None
        ## Example: (0,0,255), "meadow_001" -> (192,118)
        open_renderer_regex = re.search('\(([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\)\s*,\s*"(.*)"\s*->\s*\(([0-9]+)\s*,\s*([0-9]+)\).*', conf_string, re.IGNORECASE)
        
        #print("open_renderer_regex: ")
        #print(open_renderer_regex)
        if open_renderer_regex:
            #print("open_renderer_regex.group(1)")
            #print(open_renderer_regex.group(1))
            self.renderer_color = psp2d.Color(int(open_renderer_regex.group(1)), int(open_renderer_regex.group(2)), int(open_renderer_regex.group(3)), 255)
            self.renderer_name = open_renderer_regex.group(4)
            self.position_in_renderer = helper.Point(int(open_renderer_regex.group(5)), int(open_renderer_regex.group(6)) )
    
    def __str__(self):
        return "ConfRenderer <%s>" % (self.renderer_name)