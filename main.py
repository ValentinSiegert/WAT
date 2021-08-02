import multiprocessing as mp
import os
import sys
from pathlib import Path
from artifacts.ldfu_spider_artifact import LDFUSpider
from agents.vl10_agent import Vl10Agent
from agents.dx10_agent import Dx10Agent
from agents.apas_agent import ApasAgent
from agents.xy10_agent import Xy10Agent
from agents.cup_provider import CupProvider
from agents.dairy_product_provider import DairyProductProvider

CREDENTIALS = ('simu3', 'simu3')

AGENTS = {
    'cup_provider': {
        'thing': 'cup_provider',
        'credentials': CREDENTIALS,
        'goal': 'provide'
    },
    'dairy_product_provider': {
        'thing': 'dairy_product_provider',
        'credentials': CREDENTIALS,
        'goal': 'provide'
    },
    'xy10_agent': {
        'thing': 'packaging_workshop',
        'credentials': CREDENTIALS,
        'goal': 'package_cups'
    },
    'apas_agent': {
        'thing': 'robot_arm',
        'credentials': CREDENTIALS,
        'goal': 'pot_cups'
    },
    'dx10_agent': {
        'thing': 'filling_workshop',
        'credentials': CREDENTIALS,
        'goal': 'fill_cups'
    },
    'vl10_agent': {
        'thing' : 'storage_rack',
        'credentials': CREDENTIALS,
        'goal': 'bring_cups'
    },
}

ARTIFACTS = {
    'ldfu_spider': {
        'entry_point': 'https://ci.mines-stetienne.fr/kg/',
        'rules': Path(os.getcwd()) / 'get.n3'
    },
}

if __name__ == '__main__':
    queues = {agent: mp.Queue() for agent in AGENTS.keys()}
    spider_pipes = {}
    processes = []
    for name, desc in ARTIFACTS.items():
        if name == 'ldfu_spider':
            spider_queue = mp.Queue()
            queues['ldfu_spider'] = spider_queue
            send_to_agents = {}
            for agent in AGENTS.keys():
                agent_end, spider_end = mp.Pipe()
                spider_pipes[agent] = agent_end
                send_to_agents[agent] = spider_end
            spider = LDFUSpider(desc['entry_point'], desc['rules'], spider_queue, send_to_agents)
            processes.append(spider)
            spider.start()
    for name, desc in AGENTS.items():
        print(f"Initializing agent '{name}'...")
        class_name = name.split('_')
        class_name = [name.capitalize() for name in class_name]
        class_name = ''.join(class_name)
        c = getattr(sys.modules[__name__], class_name)
        agent = c(name, desc['thing'], desc['credentials'], desc['goal'], queues, spider_pipes[name])
        print(f"Starting agent '{name}'...")
        processes.append(agent)
        agent.start()
    print(f'Factory is now fully running!')
