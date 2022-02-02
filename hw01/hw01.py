import ast
from prettyAst.visualize_ast import visualize_ast


# Easy Task
def fibonacci(n: int) -> list[int]:
    fib = [0, 1]
    for i in range(1, n - 1):
        fib.append(fib[i - 1] + fib[i])
    return fib[:n]  # Slice for n == 0 and n == 1 cases


# Medium/Hard Task
def get_function(tree, func_name):
    for node in tree.body:
        if type(node) == ast.FunctionDef and \
                node.name == func_name:
            return node
    return None


def visualize_fib():
    with open('hw01.py', 'r') as f:
        code = f.read()
        module = ast.parse(code)
    fib_node = get_function(module, 'fibonacci')
    visualize_ast(fib_node)


visualize_fib()
