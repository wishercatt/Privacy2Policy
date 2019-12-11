# 句子预处理
def preProcessLine(line):
    # TODO 预处理表
    line = line.replace('您的', '')
    return line


'''
    比较两个四元组
    return  1 部分相等
            2 完全相等
            0 完全不相等
'''
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
