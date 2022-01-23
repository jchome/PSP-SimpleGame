# -*- coding: iso-8859-1 -*-

import re
import engine.helper as helper
import psp2d

class ConfRenderer(object):

    def __init__(self, conf_string):
        self.renderer_name = None
        self.renderer_color = None
        self.position_in_renderer = None
        ## Example: (0,0,255), "meadow_001" -> (192,118)
        open_renderer_regex = re.search('\(([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\)\s*,\s*"(.*)"\s*->\s*\((-?[0-9]+)\s*,\s*(-?[0-9]+)\).*', conf_string, re.IGNORECASE)
        
        if open_renderer_regex:
            try:
                self.renderer_color = psp2d.Color(int(open_renderer_regex.group(1)), int(open_renderer_regex.group(2)), int(open_renderer_regex.group(3)), 255)
            except:
                print("ConfRenderer Error - Cannot convert %d or %d or %d as int for renderer_color" % (open_renderer_regex.group(1), open_renderer_regex.group(2), open_renderer_regex.group(3)))
                raise ValueError("Error in %d" % conf_string)
            self.renderer_name = open_renderer_regex.group(4)
            try:
                self.position_in_renderer = helper.Point(int(open_renderer_regex.group(5)), int(open_renderer_regex.group(6)) )
            except:
                print("ConfRenderer Error - Cannot convert %d or %d as int for position_in_renderer" % (open_renderer_regex.group(5), open_renderer_regex.group(6)))
                raise ValueError("Error in %d" % conf_string)
        else:
            print("ConfRenderer Error - Cannot match %s with the regexp" % conf_string)
            raise ValueError("Error in %s" % conf_string)

    def __str__(self):
        return "ConfRenderer <%s> (%d,%d,%d) -> %s" % (self.renderer_name,
            self.renderer_color.red, self.renderer_color.green, self.renderer_color.blue,
            self.position_in_renderer)