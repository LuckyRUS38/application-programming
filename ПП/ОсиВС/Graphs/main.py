import random
import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout

node_id = 1
nodes = [0]
edges = []


def build_tree(level_now, level_max, node):
    global node_id
    global nodes
    global edges

    if level_now == level_max:
        return
    level_now += 1

    if random.random() < (1 - level_now / level_max) + 0.1:
        node['left'] = {'id': node_id, 'left': None, 'right': None}
        nodes.append(node['left']['id'])
        edges.append((node['id'], node['left']['id']))
        node_id += 1
        build_tree(level_now, level_max, node['left'])

    if random.random() < (1 - level_now / level_max) + 0.1:
        node['right'] = {'id': node_id, 'left': None, 'right': None}
        nodes.append(node['right']['id'])
        edges.append((node['id'], node['right']['id']))
        node_id += 1
        build_tree(level_now, level_max, node['right'])


build_tree(1, 8, {'id': 0, 'left': None, 'right': None})

graph = nx.Graph()
graph.add_nodes_from(nodes)
graph.add_edges_from(edges)

plt.figure(figsize=(10, 10))
pos = graphviz_layout(graph, prog="dot")
nx.draw(graph, pos, with_labels=True, font_size=22)
plt.show()
