import networkx as nx
import matplotlib.pyplot as plt

def critical_path(graph):
    # Рассчитываем ранние и поздние сроки начала для каждой задачи
    early_start = {node: 0 for node in graph.nodes}
    for node in nx.topological_sort(graph):
        for successor in graph.successors(node):
            early_start[successor] = max(early_start[successor],
                                          early_start[node] + graph[node][successor]['weight'])

    late_start = {node: early_start[max(graph.nodes)] for node in graph.nodes}
    for node in reversed(list(nx.topological_sort(graph))):
        for predecessor in graph.predecessors(node):
            late_start[predecessor] = min(late_start[predecessor], late_start[node] - graph[predecessor][node]['weight'])

    # Рассчитываем резерв времени для каждой задачи
    slack = {node: late_start[node] - early_start[node] for node in graph.nodes}

    # Определяем критический путь
    critical_path_nodes = [node for node in graph.nodes if slack[node] == 0]

    return critical_path_nodes, slack, early_start, late_start

# Пример использования
G = nx.DiGraph()

# Добавление задач с указанием продолжительности (веса)
# Start
G.add_edge('A', 'B', weight=3)
G.add_edge('A', 'C', weight=2)
G.add_edge('A', 'D', weight=2)
# Layer 1
G.add_edge('B', 'E', weight=5)
G.add_edge('B', 'F', weight=5)
G.add_edge('C', 'F', weight=2)
G.add_edge('C', 'E', weight=4)
G.add_edge('D', 'E', weight=2)
G.add_edge('D', 'F', weight=4)

# Layer 2
G.add_edge('E', 'H', weight=1)
G.add_edge('E', 'T', weight=2)
G.add_edge('E', 'K', weight=3)
G.add_edge('F', 'H', weight=4)
G.add_edge('F', 'T', weight=3)
G.add_edge('F', 'K', weight=2)

# End
G.add_edge('H', 'X', weight=6)
G.add_edge('T', 'X', weight=1)
G.add_edge('K', 'X', weight=3)


# Решение задачи критического пути
cp_nodes, slack_times, early_start, late_start = critical_path(G)

# Визуализация графа
plt.figure(figsize=(6, 3))
pos = nx.drawing.nx_pydot.graphviz_layout(G, prog='C:/Program Files/Graphviz/bin/dot')
pos_horizontal = {node: (-pos[node][1], pos[node][0]) for node in G.nodes}
nx.draw(G, pos_horizontal, with_labels=True, node_size=400, node_color="green", font_size=8, font_color="blue", font_weight="bold", arrowsize=1)

# Выделение критического пути
edge_colors = ['red' if (u, v) in G.edges and u in cp_nodes and v in cp_nodes else 'blue' for u, v in G.edges]
nx.draw_networkx_edges(G, pos_horizontal, edgelist=G.edges, edge_color=edge_colors,  width=1, alpha=1, arrowstyle='-|>')

for node in G.nodes:
    plt.text(pos_horizontal[node][0] + 14, pos_horizontal[node][1] + 8, f"{early_start[node]}/{late_start[node]}", fontsize=12, color="black", fontweight="bold", ha='center')

plt.show()
