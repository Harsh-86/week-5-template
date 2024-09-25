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
    try:
        graph.add_node("B","b")
    except TypeError:
        print("you passed")
        return
    raise Exception("Adding a node with a string weight is not acceptable")

