import os
from agents.agent import Agent
from pathlib import Path


class ApasAgent(Agent):
    def pot_cups(self):
        grasping = self.observe_property('grasping').text == 'true'
        in_movement = self.observe_property('inMovement').text == 'true'
        if not grasping and not in_movement:
            start = {
                'x': 2.2,
                'y': 0.0,
                'z': 1.0
            }
            if not self.at_start:
                self.invoke_action('moveTo', start)
                self.at_start = True
                self.at_end = False
            else:
                self.invoke_action('grasp')
        elif grasping and not in_movement:
            end = {
                'x': 3.2,
                'y': 0.0,
                'z': 1.0
            }
            if not self.at_end:
                self.invoke_action('moveTo', end)
                self.at_end = True
                self.at_start = False
            else:
                self.invoke_action('release')

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv):
        query_loc = Path(os.getcwd()) / 'ldfu/apas.rq'
        super().__init__(name, thing, credentials, goal, queues, spider_rcv, query_loc)
        self.at_start = False
        self.at_end = False
