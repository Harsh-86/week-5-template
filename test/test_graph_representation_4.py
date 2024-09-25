import subprocess
import re
import pytest

@pytest.fixture
def graph():
    from student_code import VersatileDigraph
    return VersatileDigraph()

def test_predecessors(graph):
    '''Test adding node'''
    graph.add_node("A", 10)
    graph.add_node("B",20)
    try:
        graph.add_edge("A","B",edge_weight=-1)
    except ValueError:
        print("you passed")
        return
    raise Exception("Adding a edge with negative edge weight did not produce and excception")

