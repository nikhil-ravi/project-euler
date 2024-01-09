import ast
import re

import nbformat as nbf
from markdownify import MarkdownConverter


# Create shorthand method for conversion
def md(soup, **options):
    return MarkdownConverter(**options).convert_soup(soup)


class DocstringWriter(ast.NodeTransformer):
    def __init__(self, problem_statement):
        super().__init__()
        self.problem_statement = problem_statement

    def visit_FunctionDef(self, node):
        new_docstring_node = ast.Expr(value=ast.Constant(self.problem_statement))
        node.body.insert(0, new_docstring_node)
        return node


def format_cells(nb: nbf.NotebookNode) -> nbf.NotebookNode:
    """This function will format the markdown cells in the notebook.

    Args:
        nb (nbf.NotebookNode): The notebook.

    Returns:
        nbf.NotebookNode: The notebook with formatted markdown cells.
    """
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            cell.source = replace_display_math_syntax(cell.source)
            cell.source = replace_latex_environments(cell.source)
    return nb


def replace_display_math_syntax(text):
    # Define the regular expression pattern
    pattern = r"\$\$(.*?)\$\$"

    # Define the replacement string
    replacement = r"```math\n\1\n```"

    # Use re.sub() to replace all occurrences of $$text$$ with ```math\n{text}\n```
    modified_text = re.sub(pattern, replacement, text)

    return modified_text


def replace_latex_environments(text):
    # Define the regular expression pattern for equation and align
    pattern_latex = r"(\\begin{([a-zA-Z]+(?:\*)?)}.*?\\end{\2})"

    # Define the replacement string
    replacement_latex = r"```math\n\1\n```"

    # Use re.sub() to replace LaTeX environments with the desired format
    modified_text = re.sub(pattern_latex, replacement_latex, text, flags=re.DOTALL)

    return modified_text
