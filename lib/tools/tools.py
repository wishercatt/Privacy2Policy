import os
import re
import lib.tools


def spiltSentence(line: str):
    p = re.compile(r'[。；]')
    lines = p.split(line)
    return lines


def isAbsPath(path: str):
    if os.path.isabs(path) and not re.match(r'^[\\/\.].*', path):
        return True
    return False


def getAbsPathFromRoot(path: str):
    if not isAbsPath(path):
        path = lib.tools.SOURCE_PATH + re.sub(r'(^(\./)?)|(^(\.\\)?)|[\\/]', '\\\\', path)
        if not path.endswith('.xml') and not path.endswith('.txt') and not path.endswith('.jar'):
            path = path if path.endswith('\\') else path + '\\'
    return path
