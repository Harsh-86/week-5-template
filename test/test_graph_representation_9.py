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
    assert hasattr(graph, 'plot_graph') and callable(getattr(graph, 'plot_graph'))
