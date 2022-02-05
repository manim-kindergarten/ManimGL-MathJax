import os
import sys
import inspect
import argparse
import importlib
from manimgl_mathjax import __version__

def get_mathjax_dir():
    module = importlib.import_module("manimgl_mathjax")
    directory = os.path.dirname(inspect.getabsfile(module))
    return os.path.abspath(directory)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--version",
        action="store_true",
        help="Display the version of manimgl-mathjax"
    )
    parser.add_argument(
        "install",
        nargs="?",
        help="Install npm package"
    )
    args = parser.parse_args()
    if args.version:
        print(f"ManimGL-MathJax \033[32mv{__version__}\033[0m")
    if args.install == "install":
        os.chdir(get_mathjax_dir())
        os.system("npm install")
    elif not args.version:
        parser.print_help()
        sys.exit(1)
        