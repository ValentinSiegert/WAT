import os
import subprocess
import sys
import multiprocessing as mp
from pathlib import Path


class LDFUSpider(mp.Process):
    def call_ldfu(self, query_file_location, credentials):
        cred_path = self.ldfu_location/'ldfu.properties'
        with open(cred_path, "w+") as cred_file:
            print(f'ldfu.http.auth.user = {credentials[0]}', file=cred_file)
            print(f'ldfu.http.auth.password = {credentials[1]}', file=cred_file)
        cmd = subprocess.Popen([f'{self.ldfu_script_location}', f'-i', f'{self.entry_point}', f'-c',
                                f'{cred_path}', f'-p', f'{self.rules}', f'-q', f'{query_file_location}', '-'],
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        cmd_out, cmd_err = cmd.communicate()
        os.remove(cred_path)
        query_result = [item for item in cmd_out.decode('utf-8').split('\r\n')[1:] if item != '']
        return query_result

    def run(self):
        for message in iter(self.queue.get, 'STOP'):
            query_result = self.call_ldfu(message['query_loc'], message['credentials'])
            self.agent_pipes[message['sender']].send(query_result)

    def __init__(self, entry_point, rules, queue, agent_pipes):
        super().__init__()
        self.entry_point = entry_point
        self.rules = rules
        self.queue = queue
        self.agent_pipes = agent_pipes
        self.ldfu_location = Path(os.getcwd()) / 'ldfu'
        if sys.platform == 'win32' or sys.platform == 'win64':
            self.ldfu_script_location = self.ldfu_location / 'prog/bin/ldfu.bat'
        else:
            self.ldfu_script_location = self.ldfu_location / 'prog/bin/ldfu.sh'