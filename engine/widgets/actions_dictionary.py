## Define all actions of player on all agents
all_actions = {}

## -- PALM-01 -- start
def cut_tree_palm001(player, action, agent):
    print("The player have to do %s on agent %s" % (action, agent.name))
    
def take_leaf(player, action, agent):
    print("The player have to do %s on agent %s" % (action, agent.name))
    
def cancel(player, action, agent):
    player.current_renderer.exit()

all_actions["PALM-01"] = {}
all_actions["PALM-01"]["Cut the tree"] = cut_tree_palm001
all_actions["PALM-01"]["Cancel"] = cancel
all_actions["PALM-01"]["Take a leaf"] = take_leaf

## -- PALM-01 -- end
