# coding:utf8

"""
 Created by YR on 2017/4/16.

"""
import numpy as np
# from itertools import combinations

def lcs1(x, y):
    lx, ly = len(x), len(y)
    if lx == 0 or ly == 0: return 0

    if x[-1] != y[-1]:
        return max(lcs(x[:lx - 1], y), lcs(x, y[:ly - 1]))
    else:
        return lcs(x[:lx - 1], y[:ly - 1]) + 1


def lcs(x, y):
    x = "%s%s" % ("0", x)
    y = "%s%s" % ("0", y)
    dp = np.zeros([len(x), len(y)], dtype=int)
    for i in range(1, len(x)):
        for j in range(1, len(y)):
            if x[i] == y[j]:
                dp[i, j] = dp[i - 1, j - 1] + 1
            else:
                dp[i, j] = max(dp[i - 1, j], dp[i, j - 1])
    # print dp

    return dp[len(x) - 1, len(y) - 1]


def getReslutSeq(langSeq):
    maps = {}
    seq4Char = {'r':'656471112131111777766','k':'619192422810121413121312994','4':'2716171011111116161613131188'}
    for k, v in seq4Char.items():
        la = len(langSeq)
        lb = len(v)
        i = 0
        while lb + i <= la:
            sub1 = langSeq[i:lb + i]
            # print "======================"
            # print sub1
            # print v
            res = lcs(sub1, v)
            print res
            if res >= lb - 2:
                # print k
                maps[i] = k
                i += lb
                # exit()
                continue
            i += 1
    print maps
    print sorted(maps.keys())
    ans = ""
    for x in sorted(maps.keys()):
        ans += maps[x]
    return ans
def num2CharMap():
    ncMap = {}
    for num in range(38):
        if num < 10:ncMap[num] = str(num)
        else:ncMap[num] = chr(num+87)
    return ncMap

def addDict(dict2D, key_a, key_b, val):
  if key_a in dict2D:
    dict2D[key_a].update({key_b: val})
  else:
    dict2D.update({key_a:{key_b: val}})

def fun1(x):
    x = 2
    print x

def fun2(x):
    x = 2
    print x
if __name__ == '__main__':
    pass
    a = "224334461919242281012141312131299467777746565647111213111177776634465656471112131111777766342222716171011111116161613131088"
    b = '77120'
    # print lcs(a, b)
    la = len(a)
    lb = len(b)
    # print num2CharMap()
    # print getReslutSeq(a)
    a = {}
    print a
    addDict(a, 2, 3, 4)
    print a

    c = 4
    fun1(c)
    print  c