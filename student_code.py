from graphviz import Digraph
from bokeh.plotting import figure, show

class VersatileDigraph:
    'Class for versatile digraph implementation'

    def __init__(self):
        self.__node_dict = {}
        self.__edge_dict = {}
        self.__graph = Digraph()

    def add_edge(self, start_node_id, end_node_id, node_value=5, **varargs):
        'For adding the edges to the graph'

        if start_node_id not in self.__node_dict or end_node_id not in self.__node_dict:
            raise ValueError("Both start and end nodes must exist in the graph")

        if "edge_name" not in varargs:
            raise KeyError("Please provide an 'edge_name' in the varargs")

        count = sum(1 for i, j in self.__edge_dict.items() if i[0] == start_node_id and varargs["edge_name"] == j["edge_name"])
        if count >= 1:
            raise ValueError("Please provide another name to the edge")

        self.__edge_dict[(start_node_id, end_node_id)] = varargs

    def add_node(self, node_id, node_value=1):
        'For adding node'
        if not isinstance(node_value, int):
            raise TypeError("Node value must be an integer")
        self.__node_dict[node_id] = node_value

    def get_nodes(self):
        'For retrieving the nodes'
        return list(self.__node_dict.keys())

    def get_edge_wt(self, start_node_id, end_node_id):
        'For getting the edge weights'
        if (start_node_id, end_node_id) not in self.__edge_dict:
            raise KeyError(f"No edge between {start_node_id} and {end_node_id}")
        return self.__edge_dict[(start_node_id, end_node_id)]["edge_weight"]

    def get_node_value(self, node_id):
        'For getting the node values'
        if node_id not in self.__node_dict:
            raise KeyError(f"No such node with ID {node_id}")
        return self.__node_dict[node_id]

    def print_graph(self):
        'For printing the edges of the graph'
        for i, j in self.__edge_dict.items():
            if j == {}:
                print(f"An edge from {i[0]} to {i[1]} with no weight and name")
            else:
                print(f"An edge from {i[0]} to {i[1]}, weight={j['edge_weight']}, name={j['edge_name']}")

    def predecessors(self, node_id):
        'Gives list of nodes that immediately precede the given node'
        return [i[0] for i in self.__edge_dict if i[1] == node_id]

    def successors(self, node_id):
        'Gives list of nodes that immediately succeed that node'
        return [i[1] for i in self.__edge_dict if i[0] == node_id]

    def successor_on_edge(self, start_node_id, edge_name):
        'Gives the end node, given start node and the edge name'
        for i, j in self.__edge_dict.items():
            if i[0] == start_node_id and j["edge_name"] == edge_name:
                headnode = i[1]
                break
        else:
            raise KeyError(f"No edge with name {edge_name} starting from {start_node_id}")
        return headnode

    def indegree(self, node_id):
        'Gives the number of edges that lead to the given node'
        return len([i[0] for i in self.__edge_dict if i[1] == node_id])

    def outdegree(self, node_id):
        'Gives the number of edges that lead from the given node'
        return len([i[1] for i in self.__edge_dict if i[0] == node_id])

    def plot(self):
        'To make the plot of the object'
        for i, j in self.__edge_dict.items():
            self.__graph.edge(str(i[0]), str(i[1]), label=f"{j['edge_name']}:{j['edge_weight']}")
        self.__graph.view()

    def edge_weight_plot(self):
        'Bar graph for showing the weight of each edge'
        x_list = []
        top = []
        width = 0.5

        # Use a set to store unique edge names
        unique_edge_names = set()

        for i, j in self.__edge_dict.items():
            edge_name = j["edge_name"]

            # Check if the edge name is already in the set
            if edge_name in unique_edge_names:
                # Modify the edge name to make it unique
                suffix = 1
                while f"{edge_name}_{suffix}" in unique_edge_names:
                    suffix += 1
                edge_name = f"{edge_name}_{suffix}"

            # Add the modified edge name to the set
            unique_edge_names.add(edge_name)

            x_list.append(str(edge_name))
            top.append(j["edge_weight"])

        graph = figure(x_range=x_list, title="Bokeh Bar Graph")
        graph.xaxis.axis_label = "Edge Names"
        graph.yaxis.axis_label = "Edge Weights"
        graph.vbar(x=x_list, top=top, width=width)  # Plotting the graph
        show(graph)  # Displaying the graph

# console
c = VersatileDigraph()

c.add_node("Allentown:66", node_value=66)
c.add_node("Easton:74", node_value=74)
c.add_node("Bethlehem:70", node_value=70)
c.add_edge("Allentown", "Easton", edge_name="US22E", edge_weight=17)
c.add_edge("Easton", "Allentown", edge_name="US22W", edge_weight=17)
c.add_edge("Easton", "Bethlehem", edge_name="Freemansburg", edge_weight=12)
c.add_edge("Bethlehem", "Easton", edge_name="US22E", edge_weight=12)
c.add_edge("Bethlehem", "Allentown", edge_name="Hanover", edge_weight=6)
c.add_edge("Allentown", "Bethlehem", edge_name="Hanover", edge_weight=6)

c.plot()
c.edge_weight_plot()