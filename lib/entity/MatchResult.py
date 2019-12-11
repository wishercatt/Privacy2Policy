from lib.entity import VERB_USER_LIST, VERB_APP_LIST


class MatchResult:
    actor = ''
    verb = ''
    pi = []
    purpose = ''
    line = ''

    def __init__(self, actor=None, verb=None, pi=None, purpose=None, line=None):
        self.actor = ''
        self.verb = ''
        self.pi = []
        self.purpose = ''
        self.line = ''

        if actor is not None:
            self.actor = actor
        if verb is not None:
            self.verb = verb
        if pi is not None:
            if type(pi) == list:
                self.pi = pi
            elif type(pi) == str:
                self.pi.append(pi)
        if purpose is not None:
            self.purpose = purpose
        if line is not None:
            self.line = line

        pass

    def __str__(self):
        return self.toString()

    # TODO 改一改
    def isVaild(self):

        if not self.isFlagValid():
            return False

        if self.verb == '' or not self.pi:
            return False

        if self.actor in VERB_USER_LIST['alias'] and self.verb in VERB_USER_LIST['verb']:
            return True

        if self.actor in VERB_APP_LIST['alias'] and self.verb in VERB_APP_LIST['verb']:
            return True

        return False

    # 针对标注mr检验其有效性
    def isFlagValid(self):
        if self.actor == '' and self.verb == '' and self.purpose == '' and not self.pi:
            return False
        return True

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
