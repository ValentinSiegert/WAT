import os
from agents.agent import Agent
from pathlib import Path


class Vl10Agent(Agent):
    def bring_cups(self):
        conveyor_speed = float(self.observe_property('conveyorSpeed').text)
        if conveyor_speed != 0.5:
            conveyor_speed = 0.5
            self.change_property('conveyorSpeed', str(conveyor_speed))
        try:
            next_cup = self.cup_locations.pop()
            self.invoke_action('pickItem', next_cup)
            if len(self.cup_locations) < self.cups_amount_before_reorder and not self.ordered:
                self.ordered = True
                self.reorder_cups()
            elif len(self.cup_locations) >= self.cups_amount_before_reorder:
                self.ordered = False
        except IndexError:
            self.reorder_cups()

    def reorder_cups(self):
        print(f'Requesting new Cups...')
        message = {
            'sender': self.name,
            'action': 'order',
            'content': str(self.capacity[0] * self.capacity[1])
        }
        self.queues['cup_provider'].put(message)
        return_message = self.input_queue.get()
        if return_message['sender'] == 'cup_provider' and return_message['reason'] == 'OK':
            new_locations = [[i, j] for i in range(0, self.capacity[0]) for j in range(0, self.capacity[1])
                             if [i, j] not in self.cup_locations]
            self.cup_locations = new_locations + self.cup_locations

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv):
        query_loc = Path(os.getcwd()) / 'ldfu/vl10.rq'
        super().__init__(name, thing, credentials, goal, queues, spider_rcv, query_loc)
        self.capacity = list(map(int, self.observe_property('capacity').text.strip('][').split(',')))
        self.ordered = False
        self.cup_locations = [[i, j] for i in range(0, self.capacity[0]) for j in range(0, self.capacity[1])]
        self.cups_amount_before_reorder = 21
