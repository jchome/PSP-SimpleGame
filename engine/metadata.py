
"""
Store all information about the agent
"""
class Metadata:
    def __init__(self):
        self.sprite_file = None
        self.width = 0
        self.height = 0
        self.name = ""
        ## Dict of <lang> -> <text translated>
        self.label = {}
        self.description = {}