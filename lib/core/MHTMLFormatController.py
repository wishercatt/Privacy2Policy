import os

import Config
import lib.tools.tools as tools
from lib.log.Logger import LOGGER

log = LOGGER


class MHTMLFormatController:
    __inputpath = ''
    __outputpath = ''
    __jarpath = ''

    def __init__(self, inputpath: str = ''):
        self.__outputpath = tools.getAbsPathFromRoot(Config.OUTPUT_XML_PATH)
        self.__jarpath = tools.getAbsPathFromRoot(Config.PRIVACY_POLICY_JAR_PATH)
        if inputpath != '':
            if not tools.isAbsPath(inputpath):
                inputpath = tools.getAbsPathFromRoot(inputpath)
            self.__inputpath = inputpath
        else:
            self.__inputpath = tools.getAbsPathFromRoot(Config.INPUT_MHTML_PATH)

        pass

    def startFormatHtml(self):
        jarpath = self.__jarpath
        inputpath = self.__inputpath
        outputpath = self.__outputpath
        cmd = 'java -jar -Dfile.encoding=utf-8 ' + jarpath + ' -i ' + inputpath + ' -o ' + outputpath
        renum = os.system(cmd)
        if renum != 0:
            log.error("err in format mhtml, the state num =", renum)

        return renum
