import simpy
import random

# Define the leaf node process
def leaf_node(env, node_id, spine_connections):
    while True:
        # Wait for some time before sending data
        yield env.timeout(random.expovariate(1/10))

        # Generate a random destination leaf node
        dest = random.randint(0, len(spine_connections)-1)

        # Request a connection from a spine node
        with spine_connections[dest].request() as req:
            yield req

            # Simulate sending data
            yield env.timeout(random.expovariate(1/100))

# Define the spine node process
def spine_node(env, node_id, leaf_connections):
    while True:
        # Wait for a leaf node to request a connection
        yield simpy.events.AnyOf(env, [leaf_connections[i].request() for i in range(len(leaf_connections))])

        # Find the first available connection
        for i in range(len(leaf_connections)):
            if leaf_connections[i].count == 1:
                conn = leaf_connections[i]
                break

        # Simulate the connection
        yield env.timeout(random.expovariate(1/100))

        # Release the connection
        yield simpy.events.AnyOf(env, [leaf_connections[i].request() for i in range(len(leaf_connections))])

# Set up the simulation environment
env = simpy.Environment()

# Create the nodes and connections
num_spine_nodes = 4
num_leaf_nodes = 16
spine_connections = [simpy.Resource(env, capacity=num_leaf_nodes/num_spine_nodes) for i in range(num_spine_nodes)]
leaf_connections = [simpy.Resource(env, capacity=1) for i in range(num_leaf_nodes)]
leaf_nodes = [env.process(leaf_node(env, i, spine_connections)) for i in range(num_leaf_nodes)]
spine_nodes = [env.process(spine_node(env, i, leaf_connections)) for i in range(num_spine_nodes)]

# Run the simulation
env.run(until=1000)

# Collect statistics
# ...
