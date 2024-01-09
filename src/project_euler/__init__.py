import os
import subprocess

import nbformat as nbf
import requests
from bs4 import BeautifulSoup

from ._utils import format_cells, md

FRONTMATTER = """
---
title: {title}
problem: {problem}
---
"""

SOLUTION = """
## Solution
"""


def get_problem(args):
    """This function will get the problem statement from the Project Euler website and convert it to a docstring and write it to a file.

    Args:
        problem (int): The problem number.
        args.output_dir (str): The output directory.

    Raises:
        Exception: If the problem is not found.
    """
    response = requests.get(f"https://projecteuler.net/problem={args.problem}")
    if response.status_code != 200:
        raise Exception("Problem not found")
    soup = BeautifulSoup(response.text, "html.parser")
    problem_title = soup.find("h2")
    problem_content = soup.find("div", {"class": ["problem_content"]})

    combine = str(problem_title) + str(problem_content)
    soup = BeautifulSoup(combine, "html.parser")

    problem_statement = md(soup)

    nb = nbf.v4.new_notebook()
    nb["cells"] = [
        nbf.v4.new_markdown_cell(
            FRONTMATTER.format(title=problem_title.text, problem=args.problem)
        ),
        nbf.v4.new_markdown_cell(problem_statement),
        nbf.v4.new_markdown_cell(SOLUTION),
    ]

    # If the output directory does not exist, create it
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    # If file already exists, then throw an error:
    if os.path.exists(f"{args.output_dir}/{args.problem}.ipynb"):
        raise Exception("File already exists")
    # Write the notebook to a file
    nbf.write(nb, f"{args.output_dir}/{args.problem}.ipynb")
    print(f"Problem {args.problem} written to {args.output_dir}/{args.problem}.ipynb")


def format_latex_for_katex(args):
    """This function will format the latex in the notebook for katex use.

    Args:
        filename (str): The filename of the notebook.
    """
    nb = nbf.read(open(args.filename, "r"), as_version=4)
    # format the markdown cells to be compatible with katex
    nb = format_cells(nb)

    # Write the notebook to a temporary file
    dir_name = os.path.dirname(args.filename)
    file_name = os.path.basename(args.filename)
    nbf.write(nb, f"{dir_name}/temp_{file_name}")

    # Run this command in the terminal to convert the notebook to markdown
    # jupyter nbconvert execute $(file) --to markdown --template=mdoutput
    subprocess.run(
        f"jupyter nbconvert {dir_name}/temp_{file_name} --to markdown --template=mdoutput",
        shell=True,
    )

    # delete the temporary notebook
    os.remove(f"{dir_name}/temp_{file_name}")
    # rename the markdown file
    os.rename(
        f"{dir_name}/temp_{file_name}.md".replace(".ipynb", ""),
        f"{dir_name}/{file_name}.md".replace(".ipynb", "").replace("temp_", ""),
    )


def runner():
    import argparse

    parser = argparse.ArgumentParser(
        description="Runner for the Project Euler package."
    )

    subparsers = parser.add_subparsers(
        help="sub-command help", title="subcommands", dest="subcommand"
    )

    parser_problem = subparsers.add_parser(
        "problem", help="Get the problem statement from the Project Euler website."
    )
    parser_problem.add_argument("problem", help="The problem number.")
    parser_problem.add_argument(
        "--output-dir",
        help="The output directory.",
        default="./",
    )
    parser_problem.set_defaults(func=get_problem)

    parser_md = subparsers.add_parser("md", help="Convert notebook to markdown.")
    parser_md.add_argument("filename", help="The filename of the notebook.")
    parser_md.set_defaults(func=format_latex_for_katex)

    args = parser.parse_args()
    args.func(args)
