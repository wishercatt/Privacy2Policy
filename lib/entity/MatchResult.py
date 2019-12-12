from lib.entity import VERB_USER_LIST, VERB_APP_LIST


class MatchResult:
    actor = ''
    verb = None
    pi = None  # []
    purpose = ''
    line = ''

    def __init__(self, actor: str = '', verb=None, pi=None, purpose: str = '', line: str = ''):
        self.actor = actor
        self.verb = []
        self.pi = []
        self.purpose = purpose
        self.line = line

        if verb is not None:
            if type(verb) == str:
                self.verb.append(verb)
            else:
                self.verb.extend(verb)

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

        # todo p2 非"我们"提供
        if (self.actor == '' or self.actor not in VERB_USER_LIST['alias']) and '提供' in self.verb:
            return False

        return True

    # 针对标注mr检验其有效性
    def isMarkValid(self):
        if self.actor == '' and self.verb == [] and self.purpose == '' and not self.pi:
            return False
        return True

    # 中间分析结果
    def toString(self):
        resstr = '(' + self.actor + ') ' if self.actor != '' else '(default) '

        if self.verb:
            resstr += '['
            for verb in self.verb:
                resstr += verb + '|'
            resstr = resstr[:-1]
            resstr += '] '
        else:
            resstr += '[default] '

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
            verb = ['收集']
        else:
            actor = self.actor if self.actor != '' else 'default'
            verb = self.verb if self.verb != '' else 'default'

        resstr = '(' + actor + ') '

        if verb:
            resstr += '['
            for v in verb:
                resstr += v + '|'
            resstr = resstr[:-1]
            resstr += '] '
        else:
            resstr += '[default] '

        if self.pi:
            for pi in self.pi:
                resstr += '<' + pi + '> '
        else:
            resstr += '<default> '
        resstr += '{' + self.purpose + '}' if self.purpose != '' else '{default}'

        return resstr
