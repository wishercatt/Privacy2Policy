import os
from os.path import dirname, abspath

import lib.core.XMLAnalyzeController as XMLAnalyzeController
import lib.core.NlpAnalyzeController as NlpAnalyzeController
import lib.core.MarkAnalyzeController as MarkAnalyzeController
from lib.log.Logger import LOGGER
import lib.entity.FileResult as FileResult
import lib.tools.tools as tools

log = LOGGER
SOURCE_PATH = dirname(abspath(__file__))


def main():
    outputMatchResultComByXmlMark(xmlpath='./output/xml/shopping/淘宝网隐私权政策.mhtml.xml',
                                  flagpath='./input/flagfiles', )
    pass


# return {'filea' : fr}
def getMatchResultByXml(filepath='./output/xml/', keywords=None):
    if not tools.isAbsPath(filepath):
        filepath = tools.getAbsPathFromRoot(filepath)

    if not os.path.exists(filepath):
        log.error('cannot find dir or file : ' + filepath)
        return None

    xmlcon = XMLAnalyzeController.XMLAnalyzeController(filepath, keywords)
    nlpcon = NlpAnalyzeController.NlpAnalyzeController()

    res = {}
    for label in xmlcon.getAllLabel():
        log.info('start analyze file : ' + label)
        res[label] = FileResult.FileResult(filelabel=label)
        ppandsecs = xmlcon.getPpAndSection()
        for pplabel in ppandsecs.keys():
            for pp in ppandsecs[pplabel]:
                lines = tools.spiltSentence(ppandsecs[pplabel][pp])
                for l in lines:
                    nlpcon.parseInputs(l)
                    lists = nlpcon.getAnalyzeMatchResult(pp)
                    for mr in lists:
                        if mr.isVaild():
                            res[label].addMatchResult(mr)
                    nlpcon.release()

    return res


# return {'filea' : [mr]}
def getMatchResultByMark(filepath='./input/flagfiles/'):
    if not tools.isAbsPath(filepath):
        filepath = tools.getAbsPathFromRoot(filepath)

    if not os.path.exists(filepath):
        log.error('cannot find dir or file : ' + filepath)
        return None

    markcon = MarkAnalyzeController.MarkAnalyzeController(filepath)

    return markcon.getMatchResList()


# return {'filea' : {'flag' : [mr]}, 'analyze':[mr], 'both':{flagmr:[mr]}}
def getMatchResultComByXmlFlag(xmlpath='./output/xml/', markpath='./input/flagfiles/', keywords=None):
    xmlres = getMatchResultByXml(xmlpath, keywords)
    if xmlres is None or xmlres == {}:
        log.error('error in xml analyze')
        return None
    markres = getMatchResultByMark(markpath)
    if markres is None or markres == {}:
        log.error('error in mark analyze')
        return None

    res = {}
    for label in xmlres.keys():
        if label in markres.keys():
            reslable = FileResult.FileResult(filelabel=label, res=markres[label], mark=True)
            for mr in xmlres[label].result:
                reslable.addMatchResult(mr)
            res[label] = reslable
        else:
            log.warning('xml file has no mark file : ' + label)

    return res


def outputMatchResultComByXmlMark(xmlpath='./output/xml/', flagpath='./input/flagfiles/', keywords=None):
    res = getMatchResultComByXmlFlag(xmlpath=xmlpath, markpath=flagpath, keywords=keywords)
    for label in res.keys():
        print(label + '\n')
        okcount = 0
        halfcount = 0
        notcount = 0
        markcount = 0
        fw = open(SOURCE_PATH + '/output/analyzeresult_' + label + '.txt', 'w')
        print('相同句子结果:')
        for b in res[label].result['both'].keys():
            o = res[label].result['both'][b]
            print('\t' + o[0].line)
            print('\t(m)' + o[0].toString())
            for a in o[1:]:
                m = isMatch(a, o[0])
                if m == 2:
                    print('\t(a)[ok] ' + a.toString())
                    okcount += 1
                elif m == 1:
                    print('\t(a)[half] ' + a.toString())
                    halfcount += 1
                else:
                    print('\t(a)[not] ' + a.toString())
                    notcount += 1
                fw.write(a.toPrintString() + '\n')
            print()
        print()
        print('未识别句子:')
        dellist = res[label].getDelList()
        for i in range(len(res[label].result['mark'])):
            markcount += 1
            if i in dellist:
                continue
            print('\t' + res[label].result['mark'][i].line)
            print('\t(m) ' + res[label].result['mark'][i].toString())
            print()
        print()

        print('误识别句子:')
        for b in res[label].result['analyze']:
            print('\t' + b.line)
            print('\t(a) ' + b.toString())
            fw.write(b.toPrintString() + '\n')
            print()
            notcount += 1

        print('正确识别个数' + str(okcount), end=' ')
        print('部分识别正确个数' + str(halfcount), end=' ')
        print('错误识别个数' + str(notcount))
        print('标注个数' + str(markcount))
        print('正确百分比 ' + '{:.2%}'.format(okcount / (okcount + halfcount + notcount)), end=' ')
        print('部分正确百分比 ' + '{:.2%}'.format(halfcount / (okcount + halfcount + notcount)), end=' ')
        print('错误百分比 ' + '{:.2%}'.format(notcount / (okcount + halfcount + notcount)), end=' ')
        fw.close()

    pass


def isMatch(mr, markmr):
    matchcount = 0
    for a in mr.pi:
        for b in markmr.pi:
            if a == b:
                matchcount += 1
                continue
    if matchcount == len(markmr.pi):
        matchflag = 2
    elif matchcount == 0:
        matchflag = 0
    else:
        matchflag = 1

    return matchflag


# todo
def getXmlByMhtml():
    pass


def getMatchResultByMhtml():
    pass


if __name__ == '__main__':
    main()
