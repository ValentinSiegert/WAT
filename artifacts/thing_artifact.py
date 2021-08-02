import multiprocessing as mp
import requests
from requests.auth import HTTPBasicAuth


class ThingArtifact(mp.Process):
    def read_property(self, prop, credentials):
        r = requests.get(self.endpoints[prop], auth=HTTPBasicAuth(credentials[0], credentials[1]))
        return r

    def write_property(self, prop, credentials, content=None):
        if content:
            if type(content) is list or type(content) is dict:
                r = requests.put(self.endpoints[prop], json=content, auth=HTTPBasicAuth(credentials[0], credentials[1]))
            else:
                r = requests.put(self.endpoints[prop], data=content, auth=HTTPBasicAuth(credentials[0], credentials[1]))
        else:
            r = requests.put(self.endpoints[prop], auth=HTTPBasicAuth(credentials[0], credentials[1]))
        return r

    def invoke_action(self, action, credentials, content=None):
        if content:
            if type(content) is list or type(content) is dict:
                r = requests.post(self.endpoints[action], json=content,
                                  auth=HTTPBasicAuth(credentials[0], credentials[1]))
            else:
                r = requests.post(self.endpoints[action], data=content,
                                  auth=HTTPBasicAuth(credentials[0], credentials[1]))
        else:
            r = requests.post(self.endpoints[action], auth=HTTPBasicAuth(credentials[0], credentials[1]))
        return r

    def run(self):
        for message in iter(self.pipe.recv, 'STOP'):
            return_msg = ''
            if message['type'] == 'read_prop':
                return_msg = self.read_property(message['prop'], message['credentials'])
            elif message['type'] == 'write_prop':
                return_msg = self.write_property(message['prop'], message['credentials'], message['content'])
            elif message['type'] == 'invoke_action':
                return_msg = self.invoke_action(message['action'], message['credentials'], message['content'])
            self.pipe.send(return_msg)

    def __init__(self, pipe, endpoints):
        super().__init__()
        self.pipe = pipe
        self.endpoints = endpoints
