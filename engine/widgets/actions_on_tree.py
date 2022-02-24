
from engine.widgets.actions_dictionary import ActionsOnAgent
from engine.widgets.controls_widget import Button

class ActionsOnTree(ActionsOnAgent):
    def __init__(self):
        ActionsOnAgent.__init__(self, "PALM-01")
        self.add_action(Button.TRIANGLE, "Cut the tree", self.cut_tree)
        self.add_action(Button.CIRCLE, "Cancel", self.cancel)
        self.add_action(Button.CROSS, "Take a leaf", self.take_leaf)

    def cut_tree(self, player, action, agent):
        print("The player have to do %s on agent %s" % (action, agent.name))
        player.controls_widget = None
        
    def take_leaf(self, player, action, agent):
        print("The player have to do %s on agent %s" % (action, agent.name))
        player.controls_widget = None
        
    def cancel(self, player, action, agent):
        player.controls_widget = None
        player.current_renderer.exit()

