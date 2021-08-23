import os
from agents.agent import Agent
from pathlib import Path


class CupProvider(Agent):
    def provide(self):
        for message in iter(self.input_queue.get, 'STOP'):
            if message['action'] == 'order' or message['action'] == 'orderPackages':
                query_result = None
                if message['action'] == 'order':
                    query_result = self.invoke_action('order', message['content'])
                elif message['action'] == 'orderPackages':
                    query_result = self.invoke_action('orderPackages', message['content'])
                return_message = {
                    'sender': self.name,
                    'reason': query_result.reason
                }
                self.queues[message['sender']].put(return_message)

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv):
        query_loc = Path(os.getcwd()) / 'ldfu/cup.rq'
        super().__init__(name, thing, credentials, goal, queues, spider_rcv, query_loc)
