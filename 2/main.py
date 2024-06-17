import tkinter as tk
from tkinter import ttk, messagebox
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
  

class MaxFlowGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Problema de Flujo Máximo")

        self.intro_label = tk.Label(master, text="Por favor ingresa los datos del problema:")
        self.intro_label.grid(row=0, column=0, columnspan=2)

        self.nodes = set()
        self.edges = []

        self.node_label = tk.Label(master, text="Nodo Origen:")
        self.node_label.grid(row=1, column=0)

        self.node_entry = tk.Entry(master)
        self.node_entry.grid(row=1, column=1)

        self.dest_label = tk.Label(master, text="Nodo Destino:")
        self.dest_label.grid(row=2, column=0)

        self.dest_entry = tk.Entry(master)
        self.dest_entry.grid(row=2, column=1)

        self.weight_label = tk.Label(master, text="Peso:")
        self.weight_label.grid(row=3, column=0)

        self.weight_entry = tk.Entry(master)
        self.weight_entry.grid(row=3, column=1)

        self.add_edge_button = tk.Button(master, text="Agregar Arista", command=self.add_edge)
        self.add_edge_button.grid(row=4, column=0)

        self.remove_edge_button = tk.Button(master, text="Quitar Arista", command=self.remove_edge)
        self.remove_edge_button.grid(row=4, column=1)

        self.treeview = ttk.Treeview(master, columns=('Nodo Origen', 'Nodo Destino', 'Peso'), show='headings')
        self.treeview.grid(row=5, column=0, columnspan=2)

        self.treeview.heading('Nodo Origen', text='Nodo Origen')
        self.treeview.heading('Nodo Destino', text='Nodo Destino')
        self.treeview.heading('Peso', text='Peso')

        self.origin_label = tk.Label(master, text="Nodo Origen del Problema:")
        self.origin_label.grid(row=6, column=0)

        self.origin_entry = tk.Entry(master)
        self.origin_entry.grid(row=6, column=1)

        self.destination_label = tk.Label(master, text="Nodo Destino del Problema:")
        self.destination_label.grid(row=7, column=0)

        self.destination_entry = tk.Entry(master)
        self.destination_entry.grid(row=7, column=1)

        self.solve_button = tk.Button(master, text="Resolver", command=self.solve_max_flow)
        self.solve_button.grid(row=8, column=0, columnspan=2)

    def add_edge(self):
        node = self.node_entry.get()
        dest = self.dest_entry.get()
        weight = self.weight_entry.get()

        if not node or not dest or not weight:
            messagebox.showwarning("Advertencia", "Por favor ingresa todos los campos.")
            return

        if not node.isdigit() or not dest.isdigit() or not weight.isdigit():
            messagebox.showwarning("Advertencia", "Los nodos y el peso deben ser números enteros.")
            return

        edge = (int(node), int(dest), int(weight))
        self.edges.append(edge)

        self.nodes.add(int(node))
        self.nodes.add(int(dest))

        self.treeview.insert('', 'end', values=edge)

        messagebox.showinfo("Arista Agregada", f"Arista ({node}, {dest}) con peso {weight} agregada correctamente.")

        self.node_entry.delete(0, tk.END)
        self.dest_entry.delete(0, tk.END)
        self.weight_entry.delete(0, tk.END)

    def remove_edge(self):
        selected_item = self.treeview.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor selecciona una arista para quitar.")
            return

        item = self.treeview.item(selected_item)
        edge = item['values']
        self.treeview.delete(selected_item)
        self.edges.remove(tuple(edge))
        
        messagebox.showinfo("Arista Quitada", f"Arista {edge} eliminada correctamente.")

    def solve_max_flow(self):
        if not self.edges:
            messagebox.showwarning("Advertencia", "No hay aristas para resolver el problema.")
            return

        origin = self.origin_entry.get()
        destination = self.destination_entry.get()

        if not origin or not destination:
            messagebox.showwarning("Advertencia", "Por favor ingresa el nodo origen y destino del problema.")
            return

        if not origin.isdigit() or not destination.isdigit():
            messagebox.showwarning("Advertencia", "Los nodos origen y destino deben ser números enteros.")
            return

        vertices = len(self.nodes) + 1
        g = Graph(vertices)
        for edge in self.edges:
            g.add_edge(int(edge[0]), int(edge[1]), int(edge[2]))
        source = int(origin)
        sink = int(destination)

        _ , _ = g.edmonds_karp(source, sink)
        # messagebox.showinfo("Datos Recolectados", f"Nodos: {self.nodes}\nAristas: {self.edges}\nNodo Origen del Problema: {origin}\nNodo Destino del Problema: {destination}")

def main():
    root = tk.Tk()
    app = MaxFlowGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
