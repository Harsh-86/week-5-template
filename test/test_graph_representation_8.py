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
    graph.add_edge("A","B")
    try:
        graph.predecessors("D")
    except KeyError:
        print("you passed")
        return
    raise Exception("Trying to get predecessors of a node if the node does not exist should raise a KeyError")

