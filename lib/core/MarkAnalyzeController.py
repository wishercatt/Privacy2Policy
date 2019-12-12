import os
import re

import lib.core
import lib.entity.MatchResult
import lib.tools.tools as tools
from lib.tools import mrtools


def main():
    fc = MarkAnalyzeController()
    d = fc.getMatchResList()
    for key in d:
        print(key)
        for l in d[key]:
            print(l.line)
            print(l.toString())
            print()
    pass


def getContentNoMark(line):
    return re.sub(r'[\(\)\[\]<>{}]', '', line)


class MarkAnalyzeController:
    __filepath = ''  # dir or file
    __contents = None  # {'filea': ''}
    __matchreslist = None  # {'filea':[mr]}

    def __init__(self, filepath='./input/markfiles/'):

        if tools.isAbsPath(filepath):
            self.__filepath = filepath
        else:
            self.__filepath = tools.getAbsPathFromRoot(filepath)
        self.__matchreslist = {}
        self.__contents = {}

        filelist = []
        if os.path.isdir(self.__filepath):
            for root, dirs, files in os.walk(self.__filepath):
                if root != self.__filepath:
                    break
                for file in files:
                    filelist.append(self.__filepath + str(file))
        else:
            filelist.append(self.__filepath)

        for filename in filelist:
            if filename.endswith('txt'):
                match = re.match(r'^.*[/\\](.*)\.txt', filename, re.M)
                filelabel = match.group(1)
                file = open(filename, encoding='utf-8')
                self.__contents[filelabel] = file
                self.__matchreslist[filelabel] = []
        pass

    def __del__(self):
        self.__filepath = ''
        self.__contents = None
        self.__matchreslist = None

        pass

    def getAllLabel(self):
        return self.__contents.keys()

    def getMatchResListByLabel(self, label):
        if self.__matchreslist[label]:
            return self.__matchreslist[label]

        filecontent = self.__contents[label]
        if filecontent is None:
            return []

        reslist = []
        for line in self.__contents[label]:
            p = re.compile(r'[。；]')
            # line = mrtools.preProcessLine(line)
            line = line
            splines = p.split(line)
            for l in splines:
                mr = lib.entity.MatchResult.MatchResult(line=l)
                pppattern = re.compile(r'{(.*?)}')
                actorpattern = re.compile(r'\((.*?)\)')
                verbpattern = re.compile(r'\[(.*?)\]')
                pipattern = re.compile(r'<(.*?)>')
                ppobj = pppattern.findall(l)
                acobj = actorpattern.findall(l)
                verbobj = verbpattern.findall(l)
                piobj = pipattern.findall(l)
                if ppobj:
                    for i in ppobj:
                        mr.purpose += i + '|'
                    mr.purpose = mr.purpose[:-1]
                if acobj:
                    for i in acobj:
                        mr.actor += i + '|'
                    mr.actor = mr.actor[:-1]
                if verbobj:
                    for i in verbobj:
                        mr.verb += i + '|'
                    mr.verb = mr.verb[:-1]
                if piobj:
                    mr.pi.extend(piobj)
                if not mr.isMarkValid():
                    continue
                reslist.append(mr)
            self.__matchreslist[label] = reslist
        return reslist

    def getMatchResList(self):
        labels = self.getAllLabel()
        for label in labels:
            self.getMatchResListByLabel(label)

        return self.__matchreslist


if __name__ == '__main__':
    main()
