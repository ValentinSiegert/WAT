import os
from agents.agent import Agent
from pathlib import Path


class Dx10Agent(Agent):
    def fill_cups(self):
        conveyor_speed = float(self.observe_property('conveyorSpeed').text)
        if conveyor_speed != 0.5:
            conveyor_speed = 0.5
            self.change_property('conveyorSpeed', str(conveyor_speed))
        tank_level = float(self.observe_property('tankLevel').text)
        if tank_level < self.tank_level_for_reorder and not self.ordered:
            self.ordered = True
            print(f'Requesting new Yogurt...')
            message = {
                'sender': self.name,
                'action': 'order',
                'content': '2.0'
            }
            self.queues['dairy_product_provider'].put(message)
            self.input_queue.get()
        elif tank_level >= self.tank_level_for_reorder:
            self.ordered = False

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv):
        query_loc = Path(os.getcwd()) / 'ldfu/dx10.rq'
        super().__init__(name, thing, credentials, goal, queues, spider_rcv, query_loc)
        self.ordered = False
        self.tank_level_for_reorder = 1.0
