import getopt
import os
import sys

# todo
def cmdLineParser(argv=None):
    if not argv:
        argv = sys.argv

    opts, args = getopt.getopt(argv[1:], 'i:m:', ['ih=', 'im='])
    return opts
