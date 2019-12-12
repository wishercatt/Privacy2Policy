from lib.entity import VERB_USER_LIST, VERB_APP_LIST


class MatchResult:
    actor = ''
    verb = ''
    pi = None  # []
    purpose = ''
    line = ''

    def __init__(self, actor: str = '', verb: str = '', pi=None, purpose: str = '', line: str = ''):
        self.actor = actor
        self.verb = verb
        self.pi = []
        self.purpose = purpose
        self.line = line

        if pi is not None:
            if type(pi) == str:
                self.pi.append(pi)
            else:
                self.pi.extend(pi)

        pass

    def __str__(self):
        return self.toString()

    # 判断mr有效性
    def isVaild(self):
        if self.verb == '' or not self.pi:
            return False

        if self.actor in VERB_USER_LIST['alias'] and self.verb in VERB_USER_LIST['verb']:
            return True

        if self.actor in VERB_APP_LIST['alias'] and self.verb in VERB_APP_LIST['verb']:
            return True

        return False

    # 针对标注mr检验其有效性
    def isMarkValid(self):
        if self.actor == '' and self.verb == '' and self.purpose == '' and not self.pi:
            return False
        return True

    # 中间分析结果
    def toString(self):
        resstr = '(' + self.actor + ') ' if self.actor != '' else '(default) '
        resstr += '[' + self.verb + '] ' if self.verb != '' else '[default] '
        if self.pi:
            for pi in self.pi:
                resstr += '<' + pi + '> '
        else:
            resstr += '<default> '
        resstr += '{' + self.purpose + '}' if self.purpose != '' else '{default}'

        return resstr

    # 最终输出结果
    def toPrintString(self):
        if self.actor in VERB_USER_LIST['alias']:
            actor = '我们'
            verb = '收集'
        else:
            actor = self.actor if self.actor != '' else 'default'
            verb = self.verb if self.verb != '' else 'default'

        resstr = '(' + actor + ') '
        resstr += '[' + verb + '] '
        if self.pi:
            for pi in self.pi:
                resstr += '<' + pi + '> '
        else:
            resstr += '<default> '
        resstr += '{' + self.purpose + '}' if self.purpose != '' else '{default}'

        return resstr
