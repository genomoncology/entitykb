from typing import Tuple

from entitykb.models import Node, Edge, Registry
from .index import NodeIndex, EdgeIndex


class Graph(object):
    def __len__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def iterate_edges(self, tags=None, directions=None, nodes=None):
        raise NotImplementedError

    def save_node(self, node: Node):
        raise NotImplementedError

    def get_node(self, key: str):
        raise NotImplementedError

    def save_edge(self, edge: Edge):
        raise NotImplementedError

    def remove_node(self, key: str) -> bool:
        raise NotImplementedError

    def connect(self, *, start: Node, tag: str, end: Node, data: dict = None):
        raise NotImplementedError

    def info(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError

    def put_data(self, data):
        raise NotImplementedError

    def clear_data(self):
        raise NotImplementedError


class InMemoryGraph(Graph):
    def __init__(self):
        self.nodes = NodeIndex()
        self.edges = EdgeIndex()

    def __repr__(self):
        n, e = len(self.nodes), len(self.edges)
        return f"<Graph: {n} nodes, {e} edges>"

    def __len__(self):
        return len(self.nodes)

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
        return edge

    def remove_node(self, key: str) -> bool:
        edges = [edge for _, edge in self.edges.iterate(nodes=[key])]
        for edge in edges:
            self.edges.remove(edge)

        success = self.nodes.remove(key)
        return success

    def connect(self, *, start: Node, tag: str, end: Node, data: dict = None):
        registry = Registry.instance()
        self.save_node(start)
        self.save_node(end)
        edge = registry.create(Edge, data, start=start, tag=tag, end=end)
        self.save_edge(edge)
        return edge

    def info(self):
        return {
            "nodes": len(self.nodes),
            "edges": len(self.edges),
        }

    def get_data(self) -> Tuple[NodeIndex, EdgeIndex]:
        return self.nodes, self.edges

    def put_data(self, data: Tuple[NodeIndex, EdgeIndex]):
        self.nodes, self.edges = data

    def clear_data(self):
        self.nodes = NodeIndex()
        self.edges = EdgeIndex()
