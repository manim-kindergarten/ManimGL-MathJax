from manimlib import *
from manimgl_mathjax import *

class Test(Scene):
    def construct(self):
        tex = JTex("test^a")
        self.add(tex)