# PLoad Copyright (c) 2021, 2021 Qingfu Wen under GPLv3.
# You should have received a copy of the license as LICENSE 
# 
# auther: Qingfu Wen
# email: qingfu.wen@gmail.com

from uhashring import HashRing
import socket, time
from threading import Thread

class LoadBalancer(object):
    '''
        Load Balancer for Python using persistent hash
        user can get_one_instance in load balancing and remove_instance if it is down
    '''
    
    def __init__(self, instances, interval=5):
        self.instances = instances 
        self.hash = HashRing(nodes=self.instances, hash_fn='ketama')
        self.interval = interval
        process = Thread(target=self.check_alive)
        process.start()

        
    def get_instance(self, remote_addr):
        return self.hash.get_node(remote_addr)
        
    
    def get_all_instances(self):
        return self.instances
    
    
    def get_alive_instances(self):
        return list(self.hash.get_nodes())

    
    def remove_instance(instance):
        self.hash.remove_node(instance)
    
    
    def check_alive(self):
        while True:
            for instance in self.instances:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                host, port = instance.split(":")
                result = -1
                try:
                    result = sock.connect_ex((host, int(port)))
                except:
                    pass
                if result == 0:
                    self.hash.add_node(instance)
                else:
                    try:
                        self.hash.remove_node(instance)
                    except:
                        pass
                sock.close()
            time.sleep(self.interval)