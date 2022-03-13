# -*- coding: iso-8859-1 -*-
from engine.helper import Point
from engine.widgets import actions_on_agent
import psp2d

from engine.widget import Widget

import engine.translation
_ = engine.translation.translate


class Button:
    TRIANGLE = 1
    CIRCLE = 2
    CROSS = 3
    SQUARE = 4

class ControlsWidget(Widget):
    def __init__(self, player, pos_x, pos_y):
        Widget.__init__(self, "assets/controls.png", pos_x, pos_y)
        (self.width, self.height) = (50,50)
        self.labels = {
            Button.TRIANGLE: None,
            Button.CIRCLE: None,
            Button.CROSS: None,
            Button.SQUARE: None
        }
        ## The agent to interact
        self.agent = None
        self.player = player
        self.language = player.current_board.game.current_language
        print("current_language : %s" % player.current_board.game.current_language)

    def set_agent(self, agent):
        self.agent = agent
        if self.agent.actions is not None:
            for action in self.agent.actions.all_actions:
                self.labels[action.button] = action.label

    def update(self):
        ## Listen to inputs
        pad = self.player.controller

        if pad.triangle and self.labels[Button.TRIANGLE] is not None:
            self.do_action_on_agent(self.labels[Button.TRIANGLE])

        if pad.circle and self.labels[Button.CIRCLE] is not None:
            self.do_action_on_agent(self.labels[Button.CIRCLE])

        if pad.cross and self.labels[Button.CROSS] is not None:
            self.do_action_on_agent(self.labels[Button.CROSS])

        if pad.square and self.labels[Button.SQUARE] is not None:
            self.do_action_on_agent(self.labels[Button.SQUARE])

    def draw(self):
        self.screen.blit(self.sprite, 0, 0, self.width, self.height, self.pos_x, self.pos_y, True)
        
        ## Draw title of the widget
        title_translated = _("action.on_simple_object.title", self.language) + _(self.agent.metadata.label, self.language)
        width_of_title = self.font.textWidth(title_translated)
        title_pos = Point(self.pos_x - (width_of_title / 2) + 25, self.pos_y - 17)
        self.draw_text(title_pos, title_translated)
        
        ## Draw the text for actions
        if self.labels[Button.TRIANGLE] is not None:
            triangle_pos = Point(self.pos_x + 35, self.pos_y)
            self.draw_text(triangle_pos, _(self.labels[Button.TRIANGLE], self.language))
        
        if self.labels[Button.CIRCLE] is not None:
            triangle_pos = Point(self.pos_x + 50, self.pos_y + 17)
            self.draw_text(triangle_pos, _(self.labels[Button.CIRCLE], self.language))

        if self.labels[Button.CROSS] is not None:
            triangle_pos = Point(self.pos_x + 35, self.pos_y + 35)
            self.draw_text(triangle_pos, _(self.labels[Button.CROSS], self.language))

        if self.labels[Button.SQUARE] is not None:
            triangle_pos = Point(self.pos_x - 50, self.pos_y + 17)
            self.draw_text(triangle_pos, _(self.labels[Button.SQUARE], self.language))


    def do_action_on_agent(self, action_label):
        if self.agent.actions is None:
            print("Agent's actions reference is missing for agent %s" % self.agent.name)
            return
        callback = self.agent.actions.get_callback_for_label(action_label)
        if callback is None:
            print("No action reference found for agent %s and action <%s>" % (self.agent.name, action_label))
            return
        callback(self.player, action_label, self.agent)
        ## Close this controls widget
        self.player.current_board.game.remove_widget(self)
        