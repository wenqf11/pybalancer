# pybalancer
**pybalancer** an simple load balancer for Python

## Features

English

* a simple load balancer
* consistent Hash Load Balance using **uhashring** ketama hash function
* periodly health checks, remove failed instance and add when it recovers
* manually call remove_instance when it fails.


## Installation
Using pip:

```
$ pip install pybalaner
```

## Basic usage

**pybalancer** is very simple and efficient to use:

```python
from pybalancer import LoadBalancer

# create a consistent hash ring of 3 nodes of weight 1
balancer = LoadBalancer(instances=['node1:port1', 'node2:port2', 'node3:port3'], interval=5)

# get the node name for the remote_addr key
target_instance = balancer.get_instance(remote_addr="host:port")

failed_times = 0
# call target_instance fails
if call(target_instance):
	failed_times += 1
	if failed_times > max_fails:
		balancer.remove_instance(target_instance)


alive_instances = balancer.get_alive_instances()
print(alive_instances)
```