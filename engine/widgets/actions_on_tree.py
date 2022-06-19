
from engine.widgets.actions_on_agent import ActionsOnAgent
from engine.widgets.controls_widget import Button

class ActionsOnTree(ActionsOnAgent):
    def __init__(self):
        ActionsOnAgent.__init__(self, "PALM-01")
        #self.add_action(Button.TRIANGLE, "action.on_simple_object.cut", self.cut_tree)
        self.add_action(Button.CIRCLE, "action.on_simple_object.cancel", self.cancel)
        #self.add_action(Button.CROSS, "action.on_simple_object.take-leaf", self.take_leaf)

    def cut_tree(self, player, action, agent):
        print("The player have to do %s on agent %s" % (action, agent.metadata.name))
        player.close_controls_widget()
        
    def take_leaf(self, player, action, agent):
        print("The player have to do %s on agent %s" % (action, agent.metadata.name))
        player.close_controls_widget()
        
    def cancel(self, player, action, agent):
        player.close_controls_widget()
        #player.current_board.exit()

