import argparse
import os

# <Useage>
# figtex [-h] [-f] [-o OUT] [-p PREAMBLE | -pf PREAMBLE_FILE] [--add] [--addpre] [--dpi] [TEX_STRING]

# --help -h                 Show help message.
# --fromFile -f             Read tex string from file.
# --out -o                  Output file path.
# --preamble -p             Premable String or File Path.
# --preambleFile -pf        Preamble File.
# --complete -c             Tex string is complete main block.
# --addpre                  add PREAMBLE to end of default preamble string
# --dpi                     dpi of output png file.

def parse(args):
    kargs = [None, False, None, False, 'out.png', 300]

    parser = argparse.ArgumentParser(prog='figtex')

    parser.add_argument('--fromfile', '-f', action='store_true')
    preamble = parser.add_mutually_exclusive_group()
    preamble.add_argument('--preamble', '-p')
    preamble.add_argument('--preambleFile', '-pf')
    parser.add_argument('--complete', '-c', action='store_true')
    parser.add_argument('--addpre', action='store_true')
    parser.add_argument('--out', '-o')
    parser.add_argument('--dpi', default='300')
    parser.add_argument('tex')

    args = parser.parse_args(args)

    if args.fromfile:
        with open(args.tex) as f:
            kargs[0] = f.read()
    else:
        if os.path.exists(args.tex):
            with open(args.tex) as f:
                kargs[0] = f.read()
        else:
            kargs[0] = args.tex

    kargs[1] = args.complete

    if args.preamble:
        kargs[2] = args.preamble
    elif args.preambleFile:
        with open(args.preambleFile) as f:
            kargs[2] = f.read()

    kargs[3] = args.addpre

    if args.out:
        kargs[4] = args.out

    kargs[5] = int(args.dpi)

    return kargs

