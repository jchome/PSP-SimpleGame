"""
Helper class to manage actions on an agent
"""
class ActionsOnAgent:
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.all_actions = []

    def add_action(self, button, label, callback):
        action = ActionButton(button, label, callback)
        self.all_actions.append(action)

    def contains_action_with_label(self, label):
        for action in self.all_actions:
            if action.label == label:
                return True
        return False

    def get_callback_for_label(self, label):
        for action in self.all_actions:
            if action.label == label:
                return action.callback
        return None

class ActionButton:
    def __init__(self, button, label, callback):
        self.button = button
        self.label = label
        self.callback = callback