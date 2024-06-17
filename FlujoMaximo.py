import matplotlib.pyplot as plt
import networkx as nx
from collections import deque
import pandas as pd
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button

class Graph:
    def __init__(self, vertices):
        self.graph = [[0] * vertices for _ in range(vertices)]
        self.ROW = vertices
        self.original_graph = [[0] * vertices for _ in range(vertices)]
        self.G = nx.DiGraph()
        self.fig = None
        self.gs = None
        self.ax0 = None
        self.ax1 = None
        self.button = None
        self.current_iteration = 0
        self.flag = False
        self.fig_pos = (100, 100)  # Posición deseada de la ventana gráfica


    def add_edge(self, u, v, w):
        self.graph[u][v] = w
        self.original_graph[u][v] = w
        self.G.add_edge(u, v, capacity=w)

    def bfs(self, s, t, parent):
        visited = [False] * self.ROW
        queue = deque()
        queue.append(s)
        visited[s] = True

        while queue:
            u = queue.popleft()

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return visited[t]

    def edmonds_karp(self, source, sink):
        parent = [-1] * self.ROW
        max_flow = 0
        iteration = 0
        table = []

        while self.bfs(source, sink, parent):
            iteration += 1
            path_flow = float("Inf")
            s = sink
            path = []

            while s != source:
                path_flow = min(path_flow, self.graph[parent[s]][s])
                path.append((parent[s], s))
                s = parent[s]

            v = sink
            while v != source:
                u = parent[v]
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow
            path.reverse()
            table.append((iteration, path, path_flow, max_flow))
            self.plot_graph(iteration, path, path_flow, max_flow, table)

        self.flag = True
        self.plot_graph(iteration + 1, [], 0, max_flow, table)
        return max_flow, table

    def plot_graph(self, iteration, path, path_flow, max_flow, table):
        if self.fig is None:
            self.fig = plt.figure(figsize=(14, 8))
            self.fig.canvas.manager.window.wm_geometry("+{}+{}".format(self.fig_pos[0], self.fig_pos[1]))  # Establecer la posición de la ventana gráfica
            self.gs = GridSpec(2, 1, height_ratios=[3, 1])
            self.ax0 = plt.subplot(self.gs[0])
            self.ax1 = plt.subplot(self.gs[1])
            if not self.flag:
                self.button = Button(plt.axes([0.5, 0.05, 0.1, 0.075]), 'Siguiente Iteration')
            else:
                self.button = Button(plt.axes([0.5, 0.05, 0.1, 0.075]), 'Terminar')
            self.button.on_clicked(self.next_iteration)

        self.ax0.clear()
        self.ax1.clear()

        pos = nx.spring_layout(self.G)

        # Dibujar aristas con capacidades
        edge_labels = {(u, v): f"{self.original_graph[u][v] - self.graph[u][v]}/{self.original_graph[u][v]}" for u, v in self.G.edges}
        if not self.flag:
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax0)
        else:
            nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=self.ax0, font_color='blue', font_weight='bold', font_size= 12)
        # Dibujar el grafo
        nx.draw(self.G, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=12, font_weight="bold", arrowsize=20, ax=self.ax0)
        
        # Resaltar el camino
        path_edges = [(u, v) for u, v in path]
        nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color="red", width=2, ax=self.ax0)

        if not self.flag:
            self.ax0.set_title(f"Iteración {iteration}\nPath Flow: {path_flow}\nFlujo Total: {max_flow}")
        else:
            self.ax0.set_title(f"Resultado final\n\nFlujo Total: {max_flow}")

        # Tabla
        self.ax1.axis('tight')
        self.ax1.axis('off')

        col_labels = ['Iteración', 'Camino', 'Path Flow', 'Flujo Total']
        table_data = [[iter, ' -> '.join(["1"] + [f"{v}" for u, v in path]), pf, tf] for iter, path, pf, tf in table]
        table_df = pd.DataFrame(table_data, columns=col_labels)
        
        self.ax1.table(cellText=table_df.values, colLabels=col_labels, cellLoc='center', loc='center')
        
        if self.flag:
            self.flag = False

        plt.show()

    def next_iteration(self, event):
        self.current_iteration += 1
        plt.close(self.fig)
        self.fig = None
        self.gs = None
        self.ax0 = None
        self.ax1 = None
        self.button = None

    def get_flows(self):
        flows = []
        for u in range(self.ROW):
            for v in range(self.ROW):
                if self.original_graph[u][v] > 0:
                    actual_flow = self.original_graph[u][v] - self.graph[u][v]
                    flows.append((u, v, actual_flow))
        return flows
    
# g.add_edge(1, 2, 6)
# g.add_edge(1, 3, 2)
# g.add_edge(2, 3, 1)
# g.add_edge(2, 4, 3)
# g.add_edge(4, 3, 3)
# g.add_edge(3, 5, 7)
# g.add_edge(4, 6, 2)
# g.add_edge(5, 6, 7)

