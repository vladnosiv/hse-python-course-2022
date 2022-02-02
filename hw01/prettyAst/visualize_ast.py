import ast
import networkx as nx
import matplotlib.pyplot as plt
from typing import Any


def visualize_ast(node):
    walker = PrettyAstWalker()
    walker.visit(node)
    artist = PrettyAstArtist(walker.graph, walker.node_specs)
    artist.draw()
    plt.show()


def get_type(node: ast.AST):
    return str(type(node))[12:-2]


def get_label(node: ast.AST):
    return get_type(node)


class PrettyAstWalker:
    def __init__(self):
        self.graph = nx.Graph()
        self.node_specs = {}

    def visit(self, node: ast.AST):
        self.__visit(node, -1)

    def __visit(self, node: ast.AST, parent_id: int) -> Any:

        node_id = self.graph.number_of_nodes()
        self.graph.add_node(node_id)

        self.node_specs[node_id] = (get_label(node), get_type(node))

        if parent_id != -1:
            self.graph.add_edge(parent_id, node_id)

        self.generic_visit(node, node_id)

    def generic_visit(self, node: ast.AST, parent_id: int) -> Any:
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.__visit(item, parent_id)
            elif isinstance(value, ast.AST):
                self.__visit(value, parent_id)


class PrettyAstArtist:
    def __init__(self, graph, node_specs):
        self.graph = graph
        self.node_specs = node_specs

    def get_colors(self):
        colors = {
            'FunctionDef': '#1f78b4',
            'For': '#FED766',
            'Expr': '#009fb7',
            'Return': '#696773',
            'Assign': '#5DFDCB',
            'List': '#7CC6FE',
            'Name': '#8789C0',
            'arguments': '#C19AB7',
            'arg': '#9C95DC',
            'Load': '#228CDB',
            'Store': '#0B7189',
            'Constant': '#7BC950',
            'Sub': '#B6EFD4',
            'BinOp': '#A0CCDA',
            'Subscript': '#B76D68',
            'Call': '#FFC6AC',
            'Attribute': '#AFD5AA',
            'Add': '#A69F98',
            'Slice': '#FCFF4B'
        }
        return [colors[typ] for label, typ in self.node_specs.values()]

    def draw(self):
        plt.figure(1, figsize=(40, 40))
        labels = {}
        for key in self.node_specs:
            labels[key] = self.node_specs[key][0]

        nx.draw(
            G=self.graph,
            pos=nx.drawing.nx_pydot.graphviz_layout(self.graph, prog='dot'),
            node_size=5500,
            node_shape='s',
            node_color=self.get_colors(),
            arrows=True,
            with_labels=True,
            labels=labels
        )

