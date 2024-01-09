# Project Euler

[Project Euler](https://projecteuler.net/about), named after the renowned mathematician Leonhard Euler, offers a series of intriguing mathematical and programming problems that go beyond traditional curriculum boundaries. While mathematical insights pave the way for elegant solutions, the use of computer programming skills becomes imperative for tackling most challenges.

I am using this page to document my solutions to the problems I have solved so far. Unless otherwise stated, all solutions are written in Python 3.11 and up.

## Package

I created a small package to scrape the problems from the Project Euler website. It exposes a single command line interface (CLI) command, `euler-project`, which can be used to create a new problem jupyter notebook and to convert the notebook to a markdown file. The package can be installed from PyPI using the following command:

```bash
pip install euler-project
```

### Command Line Interface

The CLI exposes two subcommands, `problem` and `md`. The `problem` subcommand can be used to create a new problem notebook. The `md` subcommand can be used to convert a notebook to a markdown file. The CLI can be invoked using the following command:

```ansi
usage: project-euler [-h] {problem,md} ...

Runner for the Project Euler package.

options:
  -h, --help    show this help message and exit

subcommands:
  {problem,md}  sub-command help
    problem     Get the problem statement from the Project Euler website.
    md          Convert notebook to markdown.
```

#### Problem Subcommand

The `problem` subcommand can be used to create a new problem notebook. The subcommand takes a single positional argument, `problem`, which is the problem number. The subcommand also takes an optional argument, `--output-dir`, which is the output directory. The default output directory is the current working directory. The subcommand can be invoked using the following command:

```ansi
usage: project-euler problem [-h] [--output-dir OUTPUT_DIR] problem

positional arguments:
  problem               The problem number.

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        The output directory.
```

#### Md Subcommand

The `md` subcommand can be used to convert a notebook to a markdown file. The subcommand takes a single positional argument, `filename`, which is the filename of the notebook. The subcommand can be invoked using the following command:

```ansi
usage: project-euler md [-h] filename

positional arguments:
  filename    The filename of the notebook.

options:
  -h, --help  show this help message and exit
```