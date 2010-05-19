import sys
import MarkdownPP

mdpp = open("readme.mdpp","r")
md = open("readme","w")

module = MarkdownPP.Module()

pp = MarkdownPP.Process()
pp.register(module)

pp.input(mdpp)
pp.process()
pp.output(md)

