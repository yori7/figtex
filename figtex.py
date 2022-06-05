import subprocess
import os
import sys
from _argparse import parse
from pathlib import Path


def makeTexFile(tex, complete, preamble, addPreamble, texDir):
    if preamble == None:
        preamble = """ 
        \\documentclass{jsarticle}
        \\usepackage{otf,amssymb,amsmath,mathtools,graphicx,siunitx}

        \\pagestyle{empty}
        """

    if addPreamble:
        preamble = """ 
        \\documentclass{jsarticle}
        \\usepackage{otf,amssymb,amsmath,mathtools,graphicx,siunitx}

        \\pagestyle{empty}
        """ + preamble

    if not complete:
        tex = """
        \\begin{document}
        %s
        \end{document}
        """ % tex

    tex = '\n'.join([preamble, tex])
    texFile = os.path.join(texDir, 'tmp.tex')
    Path(texFile).write_text(tex, encoding='utf-8')

    return texFile

def makeDviFile(texFile, dviDir):
    subprocess.run(
            ['platex', '-interaction=nonstopmode', '--halt-on-error', texFile],
            stdout=sys.stdout, stderr=sys.stderr, cwd=dviDir)
    dviFile = os.path.join(dviDir, 'tmp.dvi')

    return dviFile

def makePngFile(dviFile, out, dpi=300):
    subprocess.run(['dvipng', '-bg', 'Transparent', '-D', str(dpi), '-T', 'tight', '-o', out, dviFile])

    return os.path.abspath(out)

def figtex(tex,complete, preamble, addpreamble, out, dpi):
    pwd = os.getcwd()
    texFile = makeTexFile(tex, complete, preamble, addpreamble, pwd)
    dviFile = makeDviFile(texFile, pwd)
    pngFile = makePngFile(dviFile, out, dpi)

    return pngFile

if __name__ == '__main__':
    tex, complete, preamble, addPre, out, dpi = parse(sys.argv[1:]) # method = fromCLI, fromFile or helpm
    fpath = figtex(tex, complete, preamble, addPre, out, dpi)
    print(fpath)

