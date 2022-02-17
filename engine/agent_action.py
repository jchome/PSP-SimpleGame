# -*- coding: iso-8859-1 -*-

import re
import engine.helper as helper
import psp2d


class AgentAction(object):

    @staticmethod
    def parse(conf_string):
        # Example: "TRIANGLE": "Cut the tree"
        all_action_conf = []
        for raw_conf_line in conf_string.strip().split("\n"):
            conf_line = raw_conf_line.strip()
            if len(conf_line) == 0:
                continue
            action_regex = re.search('.*"(TRIANGLE|CROSS|SQUARE|CIRCLE)"\s*:\s*"(.*)".*', conf_line, re.IGNORECASE)
            if action_regex:
                action = AgentAction(action_regex.group(1), action_regex.group(2))
                all_action_conf.append(action)
        return all_action_conf

    def __init__(self, action_button, action_label):
        self.button = action_button
        self.label = action_label

    def __str__(self):
        return "AgentAction: %s -> %s" % (self.button, self.label)
