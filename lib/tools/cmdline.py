import getopt
import os
import sys
import Config


# todo
def cmdLineParser(argv=None):
    if not argv:
        argv = sys.argv

    opts, args = getopt.getopt(argv[1:], 'l:x:m:ps:o:', ['html=', 'xml=', 'markfile=', 'parse', 'sentence=', 'output='])
    for opt, arg in opts:
        if opt in ('-s', '--sentence'):
            Config.GlobalConfig.sentence = arg
            break
        elif opt in ('-x', '--xml'):
            Config.GlobalConfig.xmlfilepath = arg
            pass
        elif opt in ('-l', '--html'):
            Config.GlobalConfig.htmlfilepath = arg
            pass
        elif opt in ('-m', '--markfile'):
            Config.GlobalConfig.markfilepath = arg
            pass  # mark 目录指定
        elif opt in ('-p', '--parse'):
            Config.GlobalConfig.parse = True
            pass

    return opts
