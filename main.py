import simpy
import random


# Define the leaf node process
def leaf_node(env, node_id, spine_connections, num_messages_sent):
  while True:
    # Wait for some time before sending data
    yield env.timeout(random.expovariate(1 / 10))

    # Generate a random destination leaf node
    dest = random.randint(0, len(spine_connections) - 1)

    # Request a connection from a spine node
    with spine_connections[dest].request() as req:
      yield req

      # Simulate sending data
      yield env.timeout(random.expovariate(1 / 100))
      num_messages_sent[node_id] += 1


# Define the spine node process
def spine_node(env, node_id, leaf_connections, num_messages_received):
  while True:
    # Wait for a leaf node to request a connection
    reqs = [
      leaf_connections[i].request() for i in range(len(leaf_connections))
    ]
    req = yield simpy.events.AnyOf(env, reqs)

    # Find the first available connection
    for i in range(len(leaf_connections)):
      if leaf_connections[i].count == 1:
        conn = leaf_connections[i]
        break

    # Simulate the connection
    yield env.timeout(random.expovariate(1 / 100))

    # Increment the number of messages received
    num_messages_received[node_id] += 1

    # Release the connection
    yield conn.release(req)


# Set up the simulation environment
env = simpy.Environment()

# Create the nodes and connections
num_spine_nodes = 4
num_leaf_nodes = 16
spine_connections = [
  simpy.Resource(env, capacity=num_leaf_nodes / num_spine_nodes)
  for i in range(num_spine_nodes)
]
leaf_connections = [
  simpy.Resource(env, capacity=1) for i in range(num_leaf_nodes)
]
num_messages_sent = [0 for i in range(num_leaf_nodes)]
num_messages_received = [0 for i in range(num_spine_nodes)]
leaf_nodes = [
  env.process(leaf_node(env, i, spine_connections, num_messages_sent))
  for i in range(num_leaf_nodes)
]
spine_nodes = [
  env.process(spine_node(env, i, leaf_connections, num_messages_received))
  for i in range(num_spine_nodes)
]

# Run the simulation
env.run(until=1000)

# Collect statistics
total_messages_sent = sum(num_messages_sent)
total_messages_received = sum(num_messages_received)
avg_messages_per_leaf_node = total_messages_sent / num_leaf_nodes
avg_messages_per_spine_node = total_messages_received / num_spine_nodes
print(f"Total messages sent: {total_messages_sent}")
print(f"Total messages received: {total_messages_received}")
print(f"Avg. messages per leaf node: {avg_messages_per_leaf_node}")
print(f"Avg. messages per spine node: {avg_messages_per_spine_node}")
""" To simulate leaf and spine architecture, we can model the network topology using SimPy's Process-oriented approach. Here is an example of how to simulate a leaf and spine network architecture:

    Model the nodes:
    We will create two types of nodes - leaf nodes and spine nodes.

    Leaf nodes represent the end hosts that connect to the network, and spine nodes represent the switches that interconnect the leaf nodes. We can model each node as a SimPy Process.

    Model the connections:
    We will create connections between the leaf and spine nodes. Each leaf node will connect to one or more spine nodes, and each spine node will connect to multiple leaf nodes.

    We can model each connection as a SimPy Resource. When a leaf node needs to send data, it requests a connection from a spine node. The spine node grants the connection if it is available and denies it if not.

    Simulate the traffic:
    We will simulate traffic by creating SimPy events that represent data packets sent between leaf nodes. We can use the SimPy environment's scheduler to schedule these events at specific times.

    Run the simulation:
    We will run the simulation for a specific amount of time and collect statistics about the network's performance.

Here is some sample code that implements this simulation: """
