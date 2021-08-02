import os
from agents.agent import Agent
from pathlib import Path


class Xy10Agent(Agent):
    def package_cups(self):
        conveyor_speed = float(self.observe_property('conveyorSpeed').text)
        if conveyor_speed != 0.8:
            conveyor_speed = 0.8
            self.change_property('conveyorSpeed', str(conveyor_speed))
        package_buffer = int(self.observe_property('packageBuffer').text)
        if  package_buffer < self.package_buffer_to_reorder and not self.ordered:
            print(f'Requesting new Packages...')
            self.ordered = True
            message = {
                'sender': self.name,
                'action': 'orderPackages',
                'content': '10'
            }
            self.queues['cup_provider'].put(message)
            self.input_queue.get()
        elif package_buffer >= self.package_buffer_to_reorder:
            self.ordered = False

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv):
        query_loc = Path(os.getcwd()) / 'ldfu/xy10.rq'
        super().__init__(name, thing, credentials, goal, queues, spider_rcv, query_loc)
        self.ordered = False
        self.package_buffer_to_reorder = 10
