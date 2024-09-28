import graphviz
from bokeh.plotting import figure, show
from bokeh.io import output_notebook

class VersatileDigraph:
    """Defining a versatile directed graph with nodes and edges"""

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.edge_names = set()  # To store unique edge names

    def add_edge(self, start_node_id, end_node_id, start_node_value=0,
                 end_node_value=0, edge_name=None, edge_weight=1):
        """Add an edge between two nodes. Add nodes if they don't exist."""
        if not isinstance(start_node_id, str) or not isinstance(end_node_id, str):
            raise TypeError("start_node_id and end_node_id must be strings.")
        
        if not isinstance(edge_weight, (int, float)):
            raise TypeError("edge_weight must be a number.")
        
        if edge_weight < 0:
            raise ValueError("Edge weight cannot be negative.")
        
        if start_node_id not in self.nodes:
            self.add_node(start_node_id, start_node_value)
        if end_node_id not in self.nodes:
            self.add_node(end_node_id, end_node_value)

        # If the edge name is provided and already exists, raise a ValueError
        if edge_name is not None and edge_name in self.edge_names:
            raise ValueError(f"Edge with name '{edge_name}' already exists.")

        # Add the edge with its weight and name
        if start_node_id not in self.edges:
            self.edges[start_node_id] = {}

        if edge_name is None:
            edge_name = f"edge_{start_node_id}_{end_node_id}"

        self.edges[start_node_id][end_node_id] = (edge_weight, edge_name)

        # Add the edge name to the set of edge names
        self.edge_names.add(edge_name)

    def add_node(self, node_id, node_value=0):
        """Add a node with an optional value to the graph."""
        if not isinstance(node_id, str):
            raise TypeError("node_id must be a string.")
        
        if not isinstance(node_value, (int, float)):
            raise TypeError("node_value must be a number.")
        
        if node_id not in self.nodes:
            self.nodes[node_id] = node_value
        else:
            raise ValueError(f"Node with id '{node_id}' already exists.")

    def get_nodes(self):
        """Return a list of nodes in the graph."""
        return list(self.nodes.keys())

    def get_edge_weight(self, start_node_id, end_node_id):
        """Return the edge weight given a start and end node."""
        if start_node_id in self.edges and end_node_id in self.edges[start_node_id]:
            edge_weight, _ = self.edges[start_node_id][end_node_id]
            return edge_weight
        raise KeyError(f"No edge exists between '{start_node_id}' and '{end_node_id}'.")

    def get_node_value(self, node_id):
        """Return the value of the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return self.nodes.get(node_id)

    def predecessors(self, node_id):
        """Return a list of nodes that immediately precede the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return [start_node for start_node, connections in self.edges.items() if node_id in connections]

    def successors(self, node_id):
        """Return a list of nodes that immediately succeed the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        if node_id in self.edges:
            return list(self.edges[node_id].keys())
        return []

    def successor_on_edge(self, node_id, edge_name):
        """Return the successor of the given node on the specified edge name."""
        if node_id not in self.edges:
            raise KeyError(f"Node '{node_id}' does not exist.")
        for end_node, (_, name) in self.edges[node_id].items():
            if name == edge_name:
                return end_node
        raise KeyError(f"No successor found on edge '{edge_name}' for node '{node_id}'.")

    def in_degree(self, node_id):
        """Return the number of edges that lead to the given node."""
        return len(self.predecessors(node_id))

    def out_degree(self, node_id):
        """Return the number of edges that lead from the given node."""
        if node_id in self.edges:
            return len(self.edges[node_id])
        return 0

    def plot_graph(self, filename="graph"):
        """Generate and display a graph plot using Graphviz."""
        dot = graphviz.Digraph()

        # Add nodes
        for node in self.nodes:
            dot.node(node, label=f"{node}\nValue: {self.nodes[node]}")

        # Add edges
        for start_node, connections in self.edges.items():
            for end_node, (weight, name) in connections.items():
                dot.edge(start_node, end_node, label=f"{name} (Weight: {weight})")
        
        dot.render(filename, view=True)
        
    def plot_edge_weights(self):
        """Generate a bar graph showing the weight of each edge using Bokeh."""
        output_notebook()  # Enable rendering in Jupyter Notebooks

        edge_names = []
        edge_weights = []

        for start_node, connections in self.edges.items():
            for end_node, (weight, name) in connections.items():
                edge_names.append(f"{start_node}->{end_node} ({name})")
                edge_weights.append(weight)

        # Create a bar plot
        p = figure(x_range=edge_names, title="Edge Weights", plot_height=350, plot_width=800)
        p.vbar(x=edge_names, top=edge_weights, width=0.9)

        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.xaxis.major_label_orientation = 1.2  # Rotate labels for better readability

        show(p)

    def print_graph(self):
        """Print all nodes and edges."""
        print("Nodes in the graph:")
        for node_id, node_value in self.nodes.items():
            print(f"Node {node_id} with value {node_value}")

        print("\nEdges in the graph:")
        for start_node, connections in self.edges.items():
            for end_node, (weight, name) in connections.items():
                print(f"Edge from {start_node} to {end_node} with weight {weight} and name {name}")


# Example usage:
Graph = VersatileDigraph()
Graph.add_edge("A", "B", edge_weight=5, edge_name="edge1")
Graph.add_edge("A", "C", edge_weight=3, edge_name="edge2")
Graph.add_edge("B", "C", edge_weight=2, edge_name="edge3")
Graph.add_node("D", node_value=10)

Graph.print_graph()

print("Nodes in graph:", Graph.get_nodes())
print("Weight of edge A -> B:", Graph.get_edge_weight("A", "B"))
print("Value of node D:", Graph.get_node_value("D"))
print("Predecessors of C:", Graph.predecessors("C"))
print("Successors of A:", Graph.successors("A"))
print("Successor of A on edge 'edge1':", Graph.successor_on_edge("A", "edge1"))
print("Indegree of C:", Graph.in_degree("C"))
print("Outdegree of A:", Graph.out_degree("A"))

# Plot the graph using Graphviz
Graph.plot_graph()

# Plot edge weights using Bokeh
Graph.plot_edge_weights()