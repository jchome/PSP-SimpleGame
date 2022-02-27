# -*- coding: iso-8859-1 -*-

import re
import engine.helper as helper
import psp2d

class ConfBoard(object):

    def __init__(self, conf_string):
        self.board_name = None
        self.board_color = None
        self.position_in_board = None
        ## Example: (0,0,255), "meadow_001" -> (192,118)
        open_board_regex = re.search('\(([0-9]+)\s*,\s*([0-9]+)\s*,\s*([0-9]+)\)\s*,\s*"(.*)"\s*->\s*\((-?[0-9]+)\s*,\s*(-?[0-9]+)\).*', conf_string, re.IGNORECASE)
        
        if open_board_regex:
            try:
                self.board_color = psp2d.Color(int(open_board_regex.group(1)), int(open_board_regex.group(2)), int(open_board_regex.group(3)), 255)
            except:
                print("ConfBoard Error - Cannot convert %d or %d or %d as int for renderer_color" % (open_board_regex.group(1), open_board_regex.group(2), open_board_regex.group(3)))
                raise ValueError("Error in %d" % conf_string)
            self.board_name = open_board_regex.group(4)
            try:
                self.position_in_board = helper.Point(int(open_board_regex.group(5)), int(open_board_regex.group(6)) )
            except:
                print("ConfBoard Error - Cannot convert %d or %d as int for position_in_renderer" % (open_board_regex.group(5), open_board_regex.group(6)))
                raise ValueError("Error in %d" % conf_string)
        else:
            print("ConfBoard Error - Cannot match %s with the regexp" % conf_string)
            raise ValueError("Error in %s" % conf_string)

    def __str__(self):
        return "ConfBoard <%s> (%d,%d,%d) -> %s" % (self.board_name,
            self.board_color.red, self.board_color.green, self.board_color.blue,
            self.position_in_board)