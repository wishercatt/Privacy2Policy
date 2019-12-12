"""
    ltp模块配置
"""
LTP_DATA_DIR = './data/model/'

CWS_MODEL_NAME = 'cws.model'
CWS_MODEL_PATH = LTP_DATA_DIR + CWS_MODEL_NAME

POS_MODEL_NAME = 'pos.model'
POS_MODEL_PATH = LTP_DATA_DIR + POS_MODEL_NAME

PAR_MODEL_NAME = 'parser.model'
PAR_MODEL_PATH = LTP_DATA_DIR + PAR_MODEL_NAME

# 外部词典路径
PERINFO_DICT_PATH = './dicts/specificdict.txt'
# 外部词性词典路径 //TODO 不生效
POSTTAG_DICT_PATH = './dicts/posttagdict.txt'

"""
    匹配文件路径
"""
ACTOR_VERB_LIST_PATH = './data/match/actor_verb_list.txt'  # actor verb 映射

"""
    mhtml转xml依赖
"""
PRIVACY_POLICY_JAR_PATH = './data/dependencies/JarPrivacyPolicy.jar'
INPUT_MHTML_PATH = './input/mhtml'
OUTPUT_XML_PATH = './output/xml'

"""
    全局配置
"""
class GlobalConfig:
    htmlfilepath = ''
    xmlfilepath = ''
    sentence = ''
    markfilepath = ''
    parse = False
