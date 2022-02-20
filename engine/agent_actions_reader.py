# -*- coding: iso-8859-1 -*-

import re
import engine.helper as helper
import psp2d

class AgentActionsReader(object):

    @staticmethod
    def parse(conf_string):
        # Example: conf_string = 'engine.widgets.actions_on_tree': ActionOnTree
        action_regex = re.search('"(.*)"\s*:\s*(\w+)', conf_string.strip(), re.IGNORECASE)
        module = action_regex.group(1)
        className = action_regex.group(2)
        #print("module: %s" % module)
        #print("className: %s" % className)
        module = __import__(module, {}, {}, className)
        actionInstance = getattr(module, className )()
        return actionInstance
        
