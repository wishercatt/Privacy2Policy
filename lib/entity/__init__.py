import Config
from os.path import dirname, abspath

SOURCE_PATH = dirname(abspath(__file__ + '/../../'))
VERB_APP_LIST = {'alias': [], 'verb': []}
VERB_USER_LIST = {'alias': [], 'verb': []}


def main():
    readActorVerbList()
    # print(VERB_APP_LIST)
    # print(VERB_USER_LIST)
    pass


# TODO 有空再说 这个格式有问题
def readActorVerbList():
    file = open(SOURCE_PATH + Config.ACTOR_VERB_LIST_PATH, 'r', encoding='utf-8')
    line = file.readline()
    while line:
        if line.startswith('#'):
            continue
        if 'user alias' in line:
            alist = VERB_USER_LIST['alias']
        elif 'user verbs' in line:
            alist = VERB_USER_LIST['verb']
        elif 'app alias' in line:
            alist = VERB_APP_LIST['alias']
        elif 'app verbs' in line:
            alist = VERB_APP_LIST['verb']
        else:
            alist = None
        if alist is not None:
            line = file.readline()
            while line and line != '\n':
                alist.append(line.strip('\n'))
                line = file.readline()
        line = file.readline()

    file.close()
    pass


readActorVerbList()

if __name__ == '__main__':
    main()
