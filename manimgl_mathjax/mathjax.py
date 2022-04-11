import os
import re
import sys
import inspect
import importlib
import subprocess

from manimlib.logger import log
from manimlib.mobject.svg.mtex_mobject import MTex
from manimlib.utils.config_ops import digest_config
from manimlib.utils.directories import get_tex_dir
from manimlib.utils.tex_file_writing import tex_hash


def get_mathjax_dir():
    module = importlib.import_module("manimgl_mathjax")
    directory = os.path.dirname(inspect.getabsfile(module))
    return os.path.abspath(os.path.join(directory, "index.js"))


def tex_content_to_svg_file_using_mathjax(tex_content, *args):
    svg_file = os.path.join(
        get_tex_dir(), tex_hash(tex_content) + ".svg"
    )
    if not os.path.exists(svg_file):
        # create pipe
        process = subprocess.Popen(
            ["node", get_mathjax_dir(), *args],
            stdout=subprocess.PIPE,
            stdin=subprocess.PIPE
        )
        process.stdin.write(bytes(tex_content, "utf-8"))
        stdout, stderr = process.communicate()

        # capture LaTeX error
        svg_str = str(stdout, "utf-8")
        error_match_obj = re.search(r"(?<=data\-mjx\-error\=\")(.*?)(?=\")", svg_str)
        if error_match_obj is not None:
            log.error("LaTeX Error!  Not a worry, it happens to the best of us.")
            log.debug(f"The error could be: `{error_match_obj.group()}`")
            sys.exit(2)

        # save svg file
        with open(svg_file, "wb") as out:
            out.write(stdout)
    return svg_file


class JTex(MTex):
    CONFIG = {
        "use_mathjax": True,
        "use_plain_file": True
    }

    def __init__(self, tex_string, **kwargs):
        digest_config(self, kwargs)
        self.alignment = ""
        super().__init__(tex_string)
        if self.use_mathjax:
            self.scale(0.01)

    @property
    def hash_seed(self):
        return (
            self.__class__.__name__,
            self.svg_default,
            self.path_string_config,
            self.base_color,
            self.use_plain_file,
            self.isolate,
            self.tex_string,
            self.tex_environment,
            self.tex_to_color_map,
            self.use_mathjax
        )

    def get_file_path_by_content(self, content):
        if not self.use_mathjax:
            return super().get_file_path_by_content(content)
        return tex_content_to_svg_file_using_mathjax(content)


class AM(JTex):
    def get_tex_file_body(self, am_string):
        return am_string

    def get_file_path(self):
        return tex_content_to_svg_file_using_mathjax(self.tex_string, "--am")
