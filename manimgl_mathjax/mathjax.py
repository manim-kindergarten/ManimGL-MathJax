import os
import re
import sys
import inspect
import importlib
from manimlib.logger import log
from manimlib.utils.directories import get_tex_dir
from manimlib.mobject.svg.mtex_mobject import _TexSVG, MTex
from manimlib.utils.tex_file_writing import tex_hash


def get_mathjax_dir():
    module = importlib.import_module("manimgl_mathjax")
    directory = os.path.dirname(inspect.getabsfile(module))
    return os.path.abspath(os.path.join(directory, "index.js"))


def tex_content_to_svg_file_using_mathjax(tex_content):
    svg_file = os.path.join(
        get_tex_dir(), tex_hash(tex_content) + ".svg"
    )
    if not os.path.exists(svg_file):
        tex_content_to_svg_using_mathjax(tex_content, svg_file)
    return svg_file


def tex_content_to_svg_using_mathjax(tex_file_content, svg_file):
    commands = [
        "node",
        f"\"{get_mathjax_dir()}\"",
        f"\"{svg_file}\"",
        f"\"{tex_file_content}\"",
        ">",
        os.devnull
    ]
    exit_code = os.system(" ".join(commands))
    with open(svg_file, "r", encoding="utf-8") as file:
        error_match_obj = re.search(r"(?<=data\-mjx\-error\=\")(.*?)(?=\")", file.read())
    if exit_code != 0 or error_match_obj is not None:
        log.error("LaTeX Error!  Not a worry, it happens to the best of us.")
        if error_match_obj is not None:
            log.debug(f"The error could be: `{error_match_obj.group()}`")
        os.remove(svg_file)
        sys.exit(2)
    return svg_file


class JTex(MTex):
    CONFIG = {
        "use_mathjax": True,
        "use_plain_tex": True
    }

    def __init__(self, tex_string, **kwargs):
        super().__init__(tex_string, **kwargs)
        if self.use_mathjax:
            self.scale(0.75)

    def get_tex_file_content(self, tex_string):
        if not self.use_mathjax:
            return super().get_tex_file_content(tex_string)
        return tex_string.replace("\n", " ")

    def tex_content_to_glyphs(self, tex_content):
        if not self.use_mathjax:
            return super().tex_content_to_glyphs(tex_content)
        filename = tex_content_to_svg_file_using_mathjax(tex_content)
        return _TexSVG(filename)
