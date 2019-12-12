import re
import Config
from lib.log.Logger import LOGGER
import lib.entity.MatchResult
import lib.core
import os.path
from pyltp import (
    Segmentor,
    Postagger,
    Parser,
)

from lib.tools import mrtools

log = LOGGER


def main():
    f = open(lib.core.SOURCE_PATH + Config.INPUT_FILE_NAME, 'r', encoding='utf-8')
    inputdata = f.read()
    inputs = re.split('[。；]', inputdata)

    ac = NlpAnalyzeController()
    for i in range(len(inputs)):
        print("".join("第%d句:" % i))
        print()
        ac.parseInputs(inputs[i] + '。')
        # 打印全部分析结果
        ac.printAnalyzeResult()

        l = ac.getAnalyzeMatchResult()
        for r in l:
            if r.toFilterString() != '':
                print('分析: ' + r.toFilterString())
        ac.release()
        print()

    pass


class NlpAnalyzeController:
    __line = ''
    __words = None
    __postTags = None
    __arcs = None
    __resultList = None  # []
    __length = 0

    __segMentor = None
    __postTagger = None
    __parser = None

    def __init__(self):
        self.__line = ''
        self.__words = []
        self.__postTags = []
        self.__arcs = []
        self.__resultList = []
        self.__length = 0

        if self.__segMentor is None:
            cwsmodelpath = os.path.join(lib.core.SOURCE_PATH + Config.CWS_MODEL_PATH)
            self.__segMentor = Segmentor()
            self.__segMentor.load_with_lexicon(cwsmodelpath, lib.core.SOURCE_PATH + Config.PERINFO_DICT_PATH)
        if self.__postTagger is None:
            posmodelpath = os.path.join(lib.core.SOURCE_PATH + Config.POS_MODEL_PATH)
            self.__postTagger = Postagger()
            self.__postTagger.load_with_lexicon(posmodelpath,
                                                lib.core.SOURCE_PATH + Config.POSTTAG_DICT_PATH)  # 词性这个好像不生效
        if self.__parser is None:
            parmodelpath = os.path.join(lib.core.SOURCE_PATH + Config.PAR_MODEL_PATH)
            self.__parser = Parser()
            self.__parser.load(parmodelpath)
        pass

    def __del__(self):
        self.__segMentor.release()
        self.__postTagger.release()
        self.__parser.release()
        pass

    def release(self):
        self.__line = ''
        self.__words = []
        self.__postTags = []
        self.__arcs = []
        self.__resultList = []
        self.__length = 0
        pass

    def parseInputs(self, inputs):
        # self.__line = mrtools.preProcessLine(inputs)
        self.__line = inputs
        self.__words = self.__segMentor.segment(self.__line)
        self.__length = len(self.__words)
        self.__postTags = self.__postTagger.postag(self.__words)
        self.__useForcePostTagDict()  # 强制改部分词性
        self.__arcs = self.__parser.parse(self.__words, self.__postTags)
        pass

    # TODO 强制改词性 写到文件里
    def __useForcePostTagDict(self):
        for i in range(self.__length):
            if self.__words[i] == '昵称':
                self.__postTags[i] = 'n'
        pass

    # 获取分析过程结果
    def getAnalyzeResult(self):
        resstr = '\n' + self.__line + '\n\t'
        resstr += "\t".join(
            "(%d)`%s`'%s'{%d:%s[%s->%s]}%s" % (i, self.__words[i], self.__postTags[i],
                                               self.__arcs[i].head - 1, self.__arcs[i].relation,
                                               self.__words[self.__arcs[i].head - 1],
                                               self.__words[i], '\n' if (i + 1) % 4 == 0 else '') for i in
            range(self.__length))
        resstr += '\n'

        return resstr

    # 获取分析结果
    def getAnalyzeMatchResult(self, purpose: str = 'default'):
        voblist = self.__getVOBList()

        for pair in voblist:
            mr = lib.entity.MatchResult.MatchResult(verb=self.__words[pair[1]], purpose=purpose, line=self.__line)
            mractorid = self.__getSBVStartByID(pair[1])
            if mractorid is not pair[1]:
                mr.actor = self.__words[mractorid]
            nlist = [pair[0]]
            nlist.extend(self.__getCOOListById(pair[0]))
            pis = []
            for n in nlist:
                perres = ''
                # start = self.__getATTStartById(n)
                start = self.__getChildStartbyId(n)
                end = self.__getChildEndById(n)
                while start <= end:
                    perres += self.__words[start]
                    start += 1
                pis.append(perres)
            mr.pi = pis
            if mr.isVaild():
                self.__resultList.append(mr)

        return self.__resultList

    def __getVOBList(self):
        voblist = []
        for i in range(self.__length):
            if self.__arcs[i].relation == 'VOB':
                pair = [i, self.__arcs[i].head - 1]
                voblist.append(pair)

        return voblist

    # TODO 获取主语
    def __getSBVStartByID(self, iid):
        start = self.__getSBVStartByIdUseRelation(iid)
        if start != iid:
            return start

        return self.__getSBVStartByIdUseSequence(iid)

    def __getSBVStartByIdUseSequence(self, iid):
        start = iid
        for i in range(iid, -1, -1):
            if self.__words[i] in lib.entity.VERB_USER_LIST.get('alias') or \
                    self.__words[i] in lib.entity.VERB_APP_LIST.get('alias'):
                start = i
                break

        return start

    def __getSBVStartByIdUseRelation(self, iid):
        start = iid
        for i in range(self.__length):
            if self.__arcs[i].relation == 'SBV' and self.__arcs[i].head - 1 == iid:
                start = i
                break
        return start

    def __getCOOListById(self, start):
        coolist = []
        for i in range(start, self.__length):
            if self.__arcs[i].relation == 'COO' and self.__arcs[i].head - 1 == start:
                coolist.append(i)

        return coolist

    def __getATTStartById(self, iid):
        start = iid
        for i in range(iid, -1, -1):
            if self.__arcs[i].relation == 'ATT' and \
                    (self.__arcs[i].head - 1 == start or self.__arcs[i].head - 1 == iid):
                start = i

        return start

    def __getChildStartbyId(self, iid):
        start = iid
        for i in range(iid, -1, -1):
            if self.__arcs[i].relation != 'COO' and self.__arcs[i].relation != 'WP' and\
                    self.__arcs[i].head - 1 == iid:
                start = i

        return start if start != -1 else iid

    def __getChildEndById(self, iid):
        end = iid
        for i in range(iid, self.__length):
            if self.__arcs[i].relation != 'COO' and self.__arcs[i].relation != 'WP' and\
                    self.__arcs[i].head - 1 == iid:
                end = i
        return end if end != self.__length else iid


if __name__ == '__main__':
    main()
