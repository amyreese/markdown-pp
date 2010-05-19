import sys
import MarkdownPP

mdpp = open("readme.mdpp","r")
md = open("readme","w")

MarkdownPP.MarkdownPP(input=mdpp, output=md, modules=["tableofcontents"])

