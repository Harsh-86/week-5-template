import graphviz
from bokeh.plotting import figure, show


def plot_edge_weights(edge_names, edge_weights):
    """Plot a bar graph showing the weight of each edge using Bokeh."""
    if not edge_names:
        raise ValueError("No edges available to plot. Add edges to the graph first.")

    p = figure(x_range=edge_names, title="Edge Weights",
               toolbar_location=None, tools="")
    p.vbar(x=edge_names, top=edge_weights, width=0.9)
    p.xgrid.grid_line_color = None
    p.y_range.start = 0
    p.xaxis.major_label_orientation = "vertical"

    show(p)


class VersatileDigraph:
    """Defining a versatile directed graph with nodes and edges"""

    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.edge_names = set()  # To store unique edge names

    def add_edge(self, start_node_id, end_node_id, edge_name=None, edge_weight=1):
        """Add an edge between two nodes. Add nodes if they don't exist."""
        if (not isinstance(start_node_id, (int, str))
                or not isinstance(end_node_id, (int, str))):
            raise TypeError("Node IDs must be either an integer or string.")

        if not isinstance(edge_weight, (int, float)):
            raise TypeError("Edge weight must be a "
                            "numeric value (int or float).")

        if edge_weight <= 0:
            raise ValueError("Edge weight must be greater than 0.")

        if start_node_id not in self.nodes:
            self.add_node(start_node_id)
        if end_node_id not in self.nodes:
            self.add_node(end_node_id)

        # If the edge name is provided and already exists, raise a ValueError
        if edge_name is not None and edge_name in self.edge_names:
            raise ValueError(f"Edge with name "
                             f"'{edge_name}' already exists.")
        if edge_name is None:
            edge_name = f"edge_{start_node_id}_{end_node_id}"

        if start_node_id not in self.edges:
            self.edges[start_node_id] = {}

        self.edges[start_node_id][end_node_id] = (edge_weight, edge_name)
        self.edge_names.add(edge_name)

    def add_node(self, node_id, node_value=0):
        """Add a node with an optional numeric value to the graph."""
        if node_id in self.nodes:
            raise ValueError("Node '{node_id}' already exists.")
        if not isinstance(node_id, (int, str)):
            raise TypeError("Node ID must be an integer or string.")
        if not isinstance(node_value, (int, float)):
            raise TypeError("Node value must be a numeric value "
                            "(int or float).")
        self.nodes[node_id] = node_value

    def get_edge_weight(self, start_node_id, end_node_id):
        """Return the edge weight for a given start and end node."""
        if start_node_id not in self.edges:
            raise KeyError("No outgoing edges from node '{start_node_id}'.")
        if end_node_id not in self.edges[start_node_id]:
            raise KeyError("No edge from node '"
                           "{start_node_id}' to node '{end_node_id}'.")
        return self.edges[start_node_id][end_node_id][0]

    def get_node_value(self, node_id):
        """Return the value of the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return self.nodes[node_id]

    def print_graph(self):
        """Print all nodes and edges."""
        if not self.nodes:
            raise ValueError("The graph has no nodes to print.")
        print("Nodes in the graph:")
        for node_id, node_value in self.nodes.items():
            print(f"Node {node_id} with value {node_value}")

        print("\nEdges in the graph:")
        for start_node, connections in self.edges.items():
            for end_node, (weight, name) in connections.items():
                print(f"Edge '{name}' from node '{start_node}' "
                      f"to node '{end_node}' with weight {weight}")

    def predecessors(self, node_id):
        """Return a list of nodes that immediately precede the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return [start_node for start_node, connections in
                self.edges.items() if node_id in connections]


    def successors(self, node_id):
        """Return a list of nodes that immediately succeed the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return list(self.edges.get(node_id, {}).keys())

    def in_degree(self, node_id):
        """Return the number of edges that lead to the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return sum(1 for connections in
                   self.edges.values() if node_id in connections)

    def out_degree(self, node_id):
        """Return the number of edges that lead from the given node."""
        if node_id not in self.nodes:
            raise KeyError(f"Node '{node_id}' does not exist.")
        return len(self.edges.get(node_id, {}))

    def plot_graph(self):
        """Generate a visual representation of the graph using graphviz."""
        if not self.nodes:
            raise ValueError("Cannot plot the graph. No nodes exist.")
        dot = graphviz.Digraph()

        # add city_graph.png

        for node_id in self.nodes:
            dot.node(str(node_id), label=f"Node {node_id}")

        for start_node, connections in self.edges.items():
            for end_node, (weight, name) in connections.items():
                dot.edge(str(start_node),
                         str(end_node), label=f"{name} (Weight: {weight})")

        return dot

    def plot_edge_weights(self):
        """Plot the edge weights using the Bokeh library."""
        if not self.edges:
            raise ValueError("No edges to plot weights for. "
                             "Add edges to the graph first.")