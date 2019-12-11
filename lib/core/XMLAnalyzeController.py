import operator
import os

import lib.core
import re
import xml.dom.minidom
from queue import Queue
import lib.tools.tools as tools


def main():
    print(lib.core.SOURCE_PATH)
    a = XMLAnalyzeController()
    b = XMLAnalyzeController('./output/xml/shopping/淘宝网隐私权政策.mhtml.xml')
    res = b.getPpAndSectionByLabel('淘宝网隐私权政策.mhtml')
    for i in res:
        print(i)
        print(res[i])
    pass


class XMLAnalyzeController:
    __filepath = ''
    __xmlcontents = None  # {'filea' : 'contentdom'}
    __pptosec = None  # 业务于段落的映射,可能又多个文件{'filea':{'purpose' : 'section'}}
    __keywords = None  # todo 写到文件

    def __init__(self, filepath='/output/xml/', keywords=None):
        if type(keywords) == 'str':
            self.__keywords = [keywords]
        else:
            self.__keywords = keywords
        self.__xmlcontents = {}
        self.__pptosec = {}
        if tools.isAbsPath(filepath):
            self.__filepath = filepath
        else:
            self.__filepath = lib.core.SOURCE_PATH + filepath

        filelist = []
        if os.path.isdir(self.__filepath):
            for root, dirs, files in os.walk(self.__filepath, topdown=True):
                if root != self.__filepath:
                    break
                for file in files:
                    filelist.append(self.__filepath + str(file))
        else:
            filelist.append(self.__filepath)

        for file in filelist:
            if file.endswith('xml'):
                match = re.match(r'^.*[/\\](.*)\.xml', file, re.M)
                label = match.group(1)
                dom = xml.dom.minidom.parse(file)
                self.__xmlcontents[label] = dom
                self.__pptosec[label] = {}

        pass

    def __del__(self):
        self.__filepath = ''
        self.__xmlcontents = None
        self.__pptosec = None
        self.__keywords = None

        pass

    def release(self):
        for label in self.__pptosec:
            self.__pptosec[label] = {}
        self.__keywords = []

        pass

    def setKeyowords(self, keywords):
        self.release()
        self.__keywords = keywords

        pass

    def getKeyWords(self):
        return self.__keywords

    def hasKeywords(self):
        if self.__keywords is None or self.__keywords == []:
            return False
        return True

    def getAllLabel(self):
        return self.__xmlcontents.keys()

    def __hasElementChild(self, node):
        count = 0
        for child in node.childNodes:
            if child.nodeType == 1:
                count += 1
        return count

    def getPpAndSectionByLabel(self, label, keywords=None):

        if not operator.eq(self.__keywords, keywords):
            self.release()
            self.setKeyowords(keywords)

        if self.__pptosec[label]:
            return self.__pptosec[label]

        dom = self.__xmlcontents[label]
        if dom is None:
            return {}

        res = {}
        queue = Queue(maxsize=0)
        queue.put(dom.getElementsByTagName('title')[0])
        while not queue.empty():
            nownode = queue.get()
            if nownode.firstChild is None:  # 没有数据跳过该节点
                continue
            if self.__hasElementChild(nownode) > 0:
                for child in nownode.childNodes:
                    if child.nodeType == child.ELEMENT_NODE:
                        queue.put(child)
            else:
                parent = nownode.parentNode
                parentstr = parent.firstChild.data.strip()
                childstr = nownode.firstChild.data.strip()

                if not self.hasKeywords():
                    res[parentstr] = (res[parentstr] + childstr) if parentstr in res.keys() else childstr
                else:
                    for key in self.__keywords:
                        if key in parentstr:
                            res[parentstr] = (res[parentstr] + childstr) if parentstr in res.keys() else childstr
                            break
                        elif key in childstr:
                            res[parentstr] = (res[parentstr] + childstr) if parentstr in res.keys() else childstr
                            break

        self.__pptosec[label] = res
        return res

    def getPpAndSection(self, keywords=None):
        labels = self.getAllLabel()
        for label in labels:
            self.getPpAndSectionByLabel(label, keywords)

        return self.__pptosec


if __name__ == '__main__':
    main()
