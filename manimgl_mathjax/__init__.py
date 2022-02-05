import pkg_resources

__version__ = pkg_resources.get_distribution("manimgl_mathjax").version

from .mathjax import JTex