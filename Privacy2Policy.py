import os
from os.path import dirname, abspath
import Config

import lib.core.XMLAnalyzeController as XMLAnalyzeController
import lib.core.NlpAnalyzeController as NlpAnalyzeController
import lib.core.MarkAnalyzeController as MarkAnalyzeController
import lib.core.MHTMLFormatController as MHTMLFormatController
from lib.log.Logger import LOGGER
import lib.entity.FileResult as FileResult
import lib.tools.tools as tools
from lib.tools import mrtools
from lib.tools.cmdline import cmdLineParser

log = LOGGER
SOURCE_PATH = dirname(abspath(__file__))


def main():
    cmdLineParser()
    if Config.GlobalConfig.sentence != '':
        printSentenceAnalyze(Config.GlobalConfig.sentence)
    elif Config.GlobalConfig.htmlfilepath != '':
        outputMatchResultComByHtmlMark(inputpath=Config.GlobalConfig.htmlfilepath,
                                       markpath=Config.GlobalConfig.markfilepath,
                                       keywords=['商品展示', '搜索', '下单', '交付', '展示'])
    elif Config.GlobalConfig.xmlfilepath != '':
        outputMatchResultComByXmlMark(xmlpath=Config.GlobalConfig.htmlfilepath,
                                      markpath=Config.GlobalConfig.markfilepath,
                                      keywords=['商品展示', '搜索', '下单', '交付', '展示'])
    else:
        outputMatchResultComByHtmlMark(keywords=['商品展示', '搜索', '下单', '交付', '展示'])
    pass


def printSentenceAnalyze(input: str):
    nlpcon = NlpAnalyzeController.NlpAnalyzeController()
    nlpcon.parseInputs(input)
    mrlist = nlpcon.getAnalyzeMatchResult()
    print(nlpcon.getAnalyzeResult())
    for mr in mrlist:
        print(str(mr))
    pass


def outputMatchResultComByHtmlMark(inputpath: str = '', markpath: str = './input/markfiles/', keywords=None):
    if not _getXmlByMhtml(inputpath):
        return
    outputMatchResultComByXmlMark(markpath=markpath, keywords=keywords)
    pass


def outputMatchResultComByXmlMark(xmlpath: str = './output/xml/', markpath: str = './input/markfiles/', keywords=None):
    res = _getMatchResultComByXmlFlag(xmlpath=xmlpath, markpath=markpath, keywords=keywords)
    for label in res.keys():
        print(label + '\n')
        okcount = 0
        halfcount = 0
        notcount = 0
        markcount = 0
        outfilename = 'analyzeresult_' + label + '.txt'
        outfilepath = tools.getAbsPathFromRoot('/output/' + outfilename)
        fw = open(outfilepath, 'w', encoding='utf-8')
        print('相同句子结果:')
        reslabel = res[label].getResult()
        for b in reslabel['both'].keys():
            o = reslabel['both'][b]
            print('\n\t' + o[0].line)
            print('\t(m)' + o[0].toString())
            markcount += 1
            for a in o[1:]:
                m = mrtools.isMatchWithMark(a, o[0])
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
        print('未识别句子:')
        for i in range(len(reslabel['mark'])):
            markcount += 1
            print('\n\t' + reslabel['mark'][i].line)
            print('\t(m) ' + reslabel['mark'][i].toString())
        print()

        print('误识别句子:')
        nowstr = ''
        for b in reslabel['analyze']:
            if nowstr != b.line:
                print('\n\t' + b.line)
                nowstr = b.line
            print('\t(a) ' + b.toString())
            fw.write(b.toPrintString() + '\n')
            notcount += 1

        sumanacount = okcount + halfcount + notcount
        print('正确识别个数' + str(okcount), end=' ')
        print('部分识别正确个数' + str(halfcount), end=' ')
        print('错误识别个数' + str(notcount))
        print('标注个数' + str(markcount))
        print('正确百分比 ' + '{:.2%}'.format(okcount / sumanacount), end=' ')
        print('部分正确百分比 ' + '{:.2%}'.format(halfcount / sumanacount), end=' ')
        print('错误百分比 ' + '{:.2%}'.format(notcount / sumanacount))
        fw.close()

    pass


# return {'filea' : fr}
def _getMatchResultByXml(filepath: str = './output/xml/', keywords=None):
    if not tools.isAbsPath(filepath):
        filepath = tools.getAbsPathFromRoot(filepath)

    if not os.path.exists(filepath):
        log.error('cannot find dir or file : ' + filepath)
        return None

    xmlcon = XMLAnalyzeController.XMLAnalyzeController(filepath, keywords)
    nlpcon = NlpAnalyzeController.NlpAnalyzeController()

    res = {}
    for label in xmlcon.getAllLabel():

        if Config.GlobalConfig.parse:
            parsefilename = 'parseresult_' + label + '.txt'
            parsefilepath = tools.getAbsPathFromRoot('/output/' + parsefilename)
            fw = open(parsefilepath, 'w', encoding='utf-8')

        res[label] = FileResult.FileResult(filelabel=label)
        ppandsecs = xmlcon.getPpAndSection()
        for pplabel in ppandsecs.keys():
            for pp in ppandsecs[pplabel]:
                lines = tools.spiltSentence(ppandsecs[pplabel][pp])
                for l in lines:
                    nlpcon.parseInputs(l)
                    lists = nlpcon.getAnalyzeMatchResult(pp)

                    if Config.GlobalConfig.parse:
                        fw.write(nlpcon.getAnalyzeResult())
                        for mr in lists:
                            fw.write(str(mr) + '\n')
                        fw.write('\n')

                    for mr in lists:
                        if mr.isVaild():
                            res[label].addMatchResult(mr)
                    nlpcon.release()

        if Config.GlobalConfig.parse:
            fw.close()

    return res


# return {'filea' : [mr]}
def _getMatchResultByMark(filepath: str = './input/markfiles/'):
    if not tools.isAbsPath(filepath):
        filepath = tools.getAbsPathFromRoot(filepath)

    if not os.path.exists(filepath):
        log.error('cannot find dir or file : ' + filepath)
        return None

    markcon = MarkAnalyzeController.MarkAnalyzeController(filepath)

    return markcon.getMatchResList()


# return {'filea' : fr} fr:{'mark' : [], 'analyze' : [], 'both' : {hash:[markmr, mr...]}}}
def _getMatchResultComByXmlFlag(xmlpath: str = './output/xml/', markpath: str = './input/markfiles/', keywords=None):
    xmlres = _getMatchResultByXml(xmlpath, keywords)
    if xmlres is None or xmlres == {}:
        log.error('error in xml analyze')
        return None
    markres = _getMatchResultByMark(markpath)
    if markres is None or markres == {}:
        log.error('error in mark analyze')
        return None

    res = {}
    for label in xmlres.keys():
        if label in markres.keys():
            reslable = FileResult.FileResult(filelabel=label, markres=markres[label], mark=True)
            xmlreslabel = xmlres[label].getResult()
            for mr in xmlreslabel:
                reslable.addMatchResult(mr)
            res[label] = reslable
        else:
            log.warning('xml file has no mark file : ' + label)

    return res


def _getXmlByMhtml(inputpath: str = ''):
    htmcon = MHTMLFormatController.MHTMLFormatController(inputpath)
    res = htmcon.startFormatHtml()
    if res != 0:
        return False
    return True


def _getMatchResultByHtml(inputpath: str = '', keywords=None):
    if not _getXmlByMhtml(inputpath):
        return
    return _getMatchResultByXml(keywords=keywords)


def _getMatchResultComByHtmlFlag(inputpath: str = '', markpath: str = './input/markfiles/', keywords=None):
    if not _getXmlByMhtml(inputpath):
        return
    return _getMatchResultComByXmlFlag(keywords=keywords, markpath=markpath)


if __name__ == '__main__':
    main()
