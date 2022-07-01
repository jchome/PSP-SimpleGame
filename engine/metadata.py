
"""
Store some information about the agent
"""


class Metadata:
    def __init__(self):
        self.sprite_file = None
        self.width = 32
        self.height = 32
        self.name = ""
        self.fullscreen_source = None
        ## Dict of <lang> -> <text translated>
        self.label = {}
        self.description = {}
        self.production_plan = None

    """
    Read .INI file and update the properties of the instance
    """
    def load_config(self, config):
        self.name = config.get("ASSET", "name")
        self.sprite_file = config.get("ASSET", "source")

        if config.has_option("ASSET", "fullscreen_source"):
            self.fullscreen_source = config.get("ASSET", "fullscreen_source")
        if config.has_section('LABEL'):
            self.label = dict(config.items('LABEL'))
        if config.has_section('DESCRIPTION'):
            self.description = dict(config.items('DESCRIPTION'))

        self.width = config.getint("DIMENSION", "width")
        self.height = config.getint("DIMENSION", "height")

