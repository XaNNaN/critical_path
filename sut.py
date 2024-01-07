import networkx as nx
import matplotlib.pyplot as plt
import random

def calculate_early_start(graph):
    early_start = {node: 0 for node in graph.nodes}
    for node in nx.topological_sort(graph):
        for successor in graph.successors(node):
            early_start[successor] = max(early_start[successor], early_start[node] + graph[node][successor]['weight'])
    return early_start

def calculate_late_start(graph, early_start):
    late_start = {node: early_start[max(graph.nodes)] for node in graph.nodes}
    for node in reversed(list(nx.topological_sort(graph))):
        for predecessor in graph.predecessors(node):
            late_start[predecessor] = min(late_start[predecessor], late_start[node] - graph[predecessor][node]['weight'])
    return late_start

def calculate_slack(early_start, late_start):
    return {node: late_start[node] - early_start[node] for node in early_start}

def critical_path(graph):
    early_start = calculate_early_start(graph)
    late_start = calculate_late_start(graph, early_start)
    slack = calculate_slack(early_start, late_start)

    critical_path_nodes = [node for node in graph.nodes if slack[node] == 0]

    return critical_path_nodes, slack, early_start, late_start

# Создаем пустой граф
G = nx.DiGraph()

# Добавляем вершины (задачи)
tasks = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'T', 'K', 'X', 'U', 'V']
G.add_nodes_from(tasks)

# Добавляем направленные рёбра (зависимости между задачами) с случайными весами от 1 до 12
G.add_edge('A', 'B', weight=random.randint(1, 12))
G.add_edge('A', 'C', weight=random.randint(1, 12))
G.add_edge('A', 'D', weight=random.randint(1, 12))

G.add_edge('B', 'E', weight=random.randint(1, 12))
G.add_edge('B', 'F', weight=random.randint(1, 12))
G.add_edge('C', 'F', weight=random.randint(1, 12))
G.add_edge('C', 'E', weight=random.randint(1, 12))
G.add_edge('D', 'E', weight=random.randint(1, 12))
G.add_edge('D', 'F', weight=random.randint(1, 12))

G.add_edge('C', 'T', weight=random.randint(1, 12))

G.add_edge('E', 'H', weight=random.randint(1, 12))
G.add_edge('E', 'T', weight=random.randint(1, 12))
G.add_edge('E', 'K', weight=random.randint(1, 12))
G.add_edge('F', 'H', weight=random.randint(1, 12))
G.add_edge('F', 'T', weight=random.randint(1, 12))
G.add_edge('F', 'K', weight=random.randint(1, 12))

G.add_edge('H', 'U', weight=random.randint(1, 12))
G.add_edge('H', 'V', weight=random.randint(1, 12))
G.add_edge('T', 'V', weight=random.randint(1, 12))
G.add_edge('K', 'M', weight=random.randint(1, 12))
G.add_edge('K', 'V', weight=random.randint(1, 12))

G.add_edge('U', 'X', weight=random.randint(1, 12))
G.add_edge('V', 'X', weight=random.randint(1, 12))
G.add_edge('M', 'X', weight=random.randint(1, 12))

# Решение задачи критического пути
cp_nodes, slack_times, early_start, late_start = critical_path(G)


# Визуализация графа
plt.figure(figsize=(16, 10))
pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='C:/Program Files/Graphviz/bin/dot')
pos_horizontal = {node: (-pos[node][1], pos[node][0]) for node in G.nodes}
nx.draw(G, pos_horizontal, with_labels=True, node_size=350, node_color="skyblue", font_size=15, font_color="black", font_weight="bold",  arrowsize=1, node_shape="s", edge_color="gray")

# Выделение критического пути
edge_colors = ['red' if (u, v) in G.edges and u in cp_nodes and v in cp_nodes else 'blue' for u, v in G.edges]
nx.draw_networkx_edges(G, pos_horizontal, edgelist=G.edges, edge_color=edge_colors,  width=1, alpha=1, arrowstyle='-|>', arrowsize=15)

for node in G.nodes:
    plt.text(pos_horizontal[node][0], pos_horizontal[node][1] + 8, f"{early_start[node]}/{late_start[node]}", fontsize=12, color="black", fontweight="bold", ha='center')

plt.show()
