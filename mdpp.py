import sys
import MarkdownPP

mdpp = open("readme.mdpp","r")
md = open("readme","w")

classdef = MarkdownPP.modules["include"]
module = classdef()

pp = MarkdownPP.Processor()
#pp.register(module)

pp.input(mdpp)
pp.process()
pp.output(md)

