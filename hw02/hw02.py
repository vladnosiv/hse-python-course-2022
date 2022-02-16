import ast
from functools import reduce
from prettyAst.visualize_ast import visualize_ast


# Previous homework part
def get_function(tree, func_name):
    for node in tree.body:
        if type(node) == ast.FunctionDef and \
                node.name == func_name:
            return node
    return None


def visualize_fib():
    with open('fib.py', 'r') as f:
        code = f.read()
        module = ast.parse(code)
    fib_node = get_function(module, 'fibonacci')
    visualize_ast(fib_node, save_as='fib_ast.png')


# HW02 Part
def latex_table_operator(cell1, cell2) -> str:
    return str(cell1) + ' & ' + str(cell2)


def matrix_to_latex_table(matrix: list[list[str]]) -> str:
    return "\\begin{center}\n" \
           "\\begin{tabular}{ |" + ('c|' * len(matrix[0])) + " }\n" + \
           ''.join(
               "\\hline\n" + \
               reduce(latex_table_operator, row) + \
               " \\\\\n" \
               for row in matrix
           ) + \
           "\\hline\n" \
           "\\end{tabular}\n" \
           "\\end{center}\n"


def latex_header() -> str:
    return "\\documentclass{article}\n" \
           "\\usepackage[utf8]{inputenc}\n" \
           "\\usepackage{graphicx}\n" \
           "\\graphicspath{ {./} }\n" \
           "\\begin{document}\n"


def latex_footer() -> str:
    return "\\end{document}\n"


def matrix_to_latex_doc(matrix, without_footer=False) -> str:
    if len(matrix) == 0 or not all(len(row) == len(matrix[0]) for row in matrix):
        return 'Incorrect matrix.'
    return latex_header() + matrix_to_latex_table(matrix) + \
           ('' if without_footer else latex_footer())


def pic_to_latex(path_to_pic) -> str:
    return f"\\includegraphics[width=\\textwidth]{{ {path_to_pic} }}"


if __name__ == '__main__':
    visualize_fib()
    with open('artifacts/hw02.tex', 'w') as f:
        f.write(matrix_to_latex_doc([
            ['cell1', 'cell2', 'cell3'],
            ['cell4',  'cell5', 'cell6'],
            ['cell7', 'cell8', 'cell9']
        ], without_footer=True))
        f.write(pic_to_latex('artifacts/fib_ast.png'))
        f.write(latex_footer())
