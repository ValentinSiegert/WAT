import os
from agents.agent import Agent
from pathlib import Path


class DairyProductProvider(Agent):
    def provide(self):
        for message in iter(self.input_queue.get, 'STOP'):
            if message['action'] == 'order':
                query_result = self.invoke_action('order', '2')
                return_message = {
                    'sender': self.name,
                    'reason': query_result.reason
                }
                self.queues[message['sender']].put(return_message)

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv):
        query_loc = Path(os.getcwd()) / 'ldfu/dairy.rq'
        super().__init__(name, thing, credentials, goal, queues, spider_rcv, query_loc)
