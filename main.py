import tkinter as tk
from tkinter import ttk, messagebox
from FlujoMaximo import Graph


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
