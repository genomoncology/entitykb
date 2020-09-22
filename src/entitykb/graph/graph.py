from .index import NodeIndex, EdgeIndex
from .model import Node, Edge


class Graph(object):
    def __init__(self):
        self.nodes = NodeIndex()
        self.edges = EdgeIndex()

    def __repr__(self):
        n, e = len(self.nodes), len(self.edges)
        return f"<Graph: {n} nodes, {e} edges>"

    def __iter__(self):
        return iter(self.nodes)

    def iterate_edges(self, tags=None, directions=None, nodes=None):
        yield from self.edges.iterate(
            tags=tags, directions=directions, nodes=nodes
        )

    def save_node(self, node: Node):
        self.nodes.save(node)

    def get_node(self, key: str):
        return self.nodes.get(key)

    def save_edge(self, edge: Edge):
        self.edges.save(edge)

    def connect(self, *, start: Node, tag: str, end: Node, **attrs):
        self.save_node(start)
        self.save_node(end)
        edge = Edge(start=start, tag=tag, end=end, attrs=attrs)
        self.save_edge(edge)
        return edge