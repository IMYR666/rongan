# coding:utf8

"""
 Created by YR on 2017/4/18.

"""
import numpy as np
from PIL import Image


class Code(object):
    def __init__(self):
        self.markFileName = "../sources/mark4SingleChar.txt"
        self.mark4CharMap = {}
        self.num2CharMap = {}
        # 验证码的长宽
        self.width = None
        self.height = None
        # 相似度阈值，默认为mark字符串长度的80%
        self.threshold = 0.8

        self.mark4CharMap = self.getMark4Char()
        self.num2CharMap = self.getNum2Char()

    def getMark4Char(self, inputFile=None):

        """
        读取并初始化每个字符对应的特征字符串
        :param inputFile:
        :return:
        """
        if inputFile is None:
            inputFile = self.markFileName

        with open(inputFile, "r") as fp:
            txt = fp.readline().strip()
            while txt:
                k, v = txt.split("\t")
                if v != "N":
                    self.mark4CharMap[k] = v
                txt = fp.readline().strip()
        return self.mark4CharMap

    def getNum2Char(self):
        """
        初始化数字到英文字母的映射表
        :return:
        """
        for num in range(38):
            if num < 10:
                self.num2CharMap[num] = str(num)
            else:
                self.num2CharMap[num] = chr(num + 87)

        return self.num2CharMap

    @staticmethod
    def printNpList(npData, outName="../numpy2list.txt"):
        """
        输出图片的像素矩阵
        :param npData:
        :param outName:
        """
        list1 = npData.tolist()

        fp = open(outName, "w")
        for x in list1:
            for y in x:
                fp.write(str(y))
                fp.write("\t")
            fp.write("\n")

    @staticmethod
    def lcs(x, y):
        """
        求两个字符串的最长公共子序列
        :param x:
        :param y:
        :return:
        """
        x = "%s%s" % ("0", x)
        y = "%s%s" % ("0", y)
        dp = np.zeros([len(x), len(y)], dtype=int)
        for i in range(1, len(x)):
            for j in range(1, len(y)):
                if x[i] == y[j]:
                    dp[i, j] = dp[i - 1, j - 1] + 1
                else:
                    dp[i, j] = max(dp[i - 1, j], dp[i, j - 1])

        return dp[len(x) - 1, len(y) - 1]

    @staticmethod
    def getColPixNum(npData=None):
        """
        得到每列中像素点的个数
        :param npData:
        :return:
        """
        # 标记非纯白像素点为1，方便后面统计总像素点个数
        npData[npData != 255] = 1
        npData[npData == 255] = 0

        colPixNum = npData.sum(0)
        return colPixNum

    def getResultStr(self, langSeq):
        maps = {}
        for char, mark in self.mark4CharMap.items():
            la = len(langSeq)
            lb = len(mark)
            i = 0
            while lb + i <= la:
                subStr = langSeq[i:lb + i]
                res = self.lcs(subStr, mark)
                if res >= int(lb * self.threshold):
                    maps[i] = char
                    i += lb
                    continue
                i += 1
        ans = ""
        for x in sorted(maps.keys()):
            ans += maps[x]
        return ans

    def identify(self, im=None):
        """
        识别荣安驾校官网的验证码
        :type im: Image object
        """
        if im is None:
            raise Exception("需要一个Image对象作为参数！")

        (self.width, self.height) = im.size
        # 灰度处理
        im = im.convert("L")
        pixelData = im.getdata()
        npData = np.array(list(pixelData)).reshape((self.height, self.width))
        colPixNum = self.getColPixNum(npData)

        imgStr = ''.join([self.num2CharMap[x] for x in colPixNum.tolist()])
        res = self.getResultStr(imgStr)

        return res


if __name__ == '__main__':
    for i in range(50, 59):
        im = Image.open("../sources/codeImgs/code%d.png" % i)
        code1 = Code()
        print code1.identify(im)