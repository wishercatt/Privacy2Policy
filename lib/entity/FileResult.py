from lib.core import MarkAnalyzeController
from lib.log.Logger import LOGGER

log = LOGGER


class FileResult:
    filelabel = ''
    keywords = None
    mark = False
    '''
    no : res = [mr]
    only mark : res = {'mark' : [mr], 'analyze':[mr], 'both':{'hash':[markmr, mr...]}
    '''
    result = None
    __delmark = None

    def __init__(self, filelabel='', res=None, mark=False):
        self.filelabel = filelabel
        self.mark = mark
        if res is not None:
            if not self.mark and type(res) != 'list':
                log.error('type res is ' + type(res) + ' but without mark is should be list')
            elif self.mark:
                self.result = {'mark': res, 'analyze': [], 'both': {}}
                self.__delmark = set()
            else:
                self.result = res
        else:
            if self.mark:
                log.error('init filemr need maredmrs')
                return
            self.result = None

        pass

    def addMatchResult(self, mr=None):
        if mr is None:
            log.warning('addMatchResult with None mr')
            return
        if self.mark:
            self.__addMatchResult_Mark(mr)
        else:
            self.__addMatchResult(mr)

        pass

    def __addMatchResult(self, mr):
        if self.result is None:
            self.result = []
        self.result.append(mr)

        pass

    def __addMatchResult_Mark(self, mr):
        flag = False
        for i in range(len(self.result['mark'])):
            if MarkAnalyzeController.getContentNoMark(self.result['mark'][i].line.strip()) == mr.line.strip():
                hashid = hash(self.result['mark'][i].line.strip())
                if hashid in self.result['both'].keys():
                    self.result['both'][hashid].append(mr)
                else:
                    self.result['both'][hashid] = [self.result['mark'][i], mr]
                self.__delmark.add(i)
                flag = True
                break
        if not flag:
            self.result['analyze'].append(mr)

        pass

    def getDelList(self):
        if self.mark:
            return self.__delmark
        return []
