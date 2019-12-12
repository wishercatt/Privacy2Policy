from lib.core import MarkAnalyzeController
from lib.entity import MatchResult
from lib.log.Logger import LOGGER

log = LOGGER


# todo 拆成两个
class FileResult:
    __filelabel = ''
    __keywords = None
    __mark = False  # 是否为混合标记文件的结果
    __delmark = None
    '''no
    no : res = [mr]
    only mark : res = {'mark' : [mr], 'analyze':[mr], 'both':{'hash':[markmr, mr...]}
    '''
    __result = None

    # 带标记的必须用标记文件的结果初始化markres
    def __init__(self, filelabel: str = '', keywords=None, markres=None, mark: bool = False):
        if filelabel == '':
            log.warning('there no file label when fileresult init')
        self.__filelabel = filelabel
        self.__mark = mark

        if mark:
            if markres is not None and (type(markres) == 'list' or type(markres) != 'tuple'):
                self.__result = {'mark': list(markres), 'analyze': [], 'both': {}}
                self.__delmark = set()
            else:
                log.error('fr should be init by mark result list')
        else:
            self.__result = []

        pass

    def addMatchResult(self, mr: MatchResult = None):
        if mr is None:
            log.warning('addMatchResult with None mr')
            return
        if self.__mark:
            self.__addMatchResultWithMark(mr)
        else:
            self.__addMatchResult(mr)

        pass

    def __addMatchResult(self, mr: MatchResult):
        if self.__result is None:
            self.__result = []
        self.__result.append(mr)

        pass

    def __addMatchResultWithMark(self, mr: MatchResult):
        flag = False
        for i in range(len(self.__result['mark'])):
            if MarkAnalyzeController.getContentNoMark(self.__result['mark'][i].line.strip()) == mr.line.strip():
                hashid = hash(self.__result['mark'][i].line.strip())
                if hashid in self.__result['both'].keys():
                    self.__result['both'][hashid].append(mr)
                else:
                    self.__result['both'][hashid] = [self.__result['mark'][i], mr]
                self.__delmark.add(i)
                flag = True
                break
        if not flag:
            self.__result['analyze'].append(mr)

        pass

    def getResult(self):
        if self.__mark:
            if self.__delmark != set() or self.__delmark is not None:
                delmarklist = list(self.__delmark)
                delmarklist.sort(reverse=True)
                for i in delmarklist:
                    del self.__result['mark'][i]
                self.__delmark = set()

        return self.__result
