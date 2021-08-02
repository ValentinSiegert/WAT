import multiprocessing as mp
import re
import time
from artifacts.thing_artifact import ThingArtifact


class Agent(mp.Process):
    def observe_property(self, prop):
        message = {
            'type': 'read_prop',
            'prop': prop,
            'credentials': self.credentials
        }
        self.thing_pipe.send(message)
        return self.thing_pipe.recv()

    def change_property(self, prop, content=None):
        message = {
            'type': 'write_prop',
            'prop': prop,
            'content': content,
            'credentials': self.credentials
        }
        self.thing_pipe.send(message)
        return self.thing_pipe.recv()

    def invoke_action(self, action, content=None):
        message = {
            'type': 'invoke_action',
            'action': action,
            'content': content,
            'credentials': self.credentials
        }
        self.thing_pipe.send(message)
        return self.thing_pipe.recv()

    def init_thing(self):
        self.thing_pipe, agent_pipe = mp.Pipe()
        ldfu_call = {
            'sender': self.name,
            'query_loc': self.query_loc,
            'credentials': self.credentials
        }
        self.queues['ldfu_spider'].put(ldfu_call)
        kg_response = self.spider_rcv.recv()
        kg_response = [re.sub(r'["<>]', '', line) for line in kg_response]
        kg_response = {line.split()[0]: line.split()[1] for line in kg_response if line.split()[1].endswith(line.split()[0])}
        # fixing a bug in the knowledge graph with wrong link given
        if self.name == 'cup_provider':
            kg_response['orderPackages'] = 'https://ci.mines-stetienne.fr/simu/cupProvider/actions/orderPackages'
        thing = ThingArtifact(agent_pipe, kg_response)
        thing.start()

    def run(self):
        method_to_exec = getattr(self, self.goal)
        while True:
            method_to_exec()
            # letting all agents sleep for 5 sec besides the agent controlling the robot arm
            if self.name != 'apas_agent':
                time.sleep(5)

    def __init__(self, name, thing, credentials, goal, queues, spider_rcv, query_loc):
        super().__init__()
        self.name = name
        self.thing = thing
        self.credentials = credentials
        self.goal = goal
        self.input_queue = queues[self.name]
        self.queues = queues
        self.spider_rcv = spider_rcv
        self.thing_pipe = None
        self.query_loc = query_loc
        self.init_thing()
