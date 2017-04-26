# coding:utf8

"""
 Created by YR on 2017/4/10.

"""

import numpy as np
from PIL import Image


def binaral():
    """
         二值化
    """
    threshold = 140
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)


def printNpList(npData, outName="../sources/numpy2list.txt"):
    list1 = npData.tolist()

    fp = open(outName, "w")
    for x in list1:
        for y in x:
            fp.write(str(y))
            fp.write("\t")
        fp.write("\n")


def fixData(np_data, depth):
    cData1 = np_data
    if not depth: return cData1

    for x in range(cData1.shape[0] - 1):
        for y in range(cData1.shape[1] - 1):
            if cData1[x, y] == 255:
                num = 0
                if cData1[x - 1, y] < 225: num += 1
                if cData1[x + 1, y] < 225: num += 1
                if cData1[x, y - 1] < 225: num += 1
                if cData1[x, y + 1] < 225: num += 1
                if num >= 3:
                    cData1[x, y] = int((cData1[x - 1, y] + cData1[x + 1, y] + cData1[x, y - 1] + cData1[x, y + 1]) / 4)

                print cData1[x, y]
    printNpList(cData1, outName='../sources/fixList.txt')
    fixData(cData1, depth - 1)
    return cData1


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


def clearData(npData, depth):
    cData = npData

    if depth == 0: return cData
    maps[:, :] = np.zeros([50, 300], dtype=int)
    isProcess[:, :] = np.zeros([50, 300], dtype=int)
    # 将上下5个像素变为255
    cData[0:4, :] = 255
    cData[-5:, :] = 255
    # 将左右1个像素变为255
    cData[:, 0] = 255
    cData[:, -1] = 255
    # cData[cData > 180] = 255
    print cData.shape
    cData = fixData(cData, 2)
    (height, width) = cData.shape
    for x in range(height):
        for y in range(width):
            if isProcess[x, y] == 0 and cData[x, y] != 255:
                #                 print x,y
                #                 global flag
                # 局部标记表，每遇到一个符合条件的点，此表都会重置为0
                flags[:, :] = np.zeros([50, 300], dtype=int)
                maps[x, y] = floodFill(cData, x, y, height, width)
                #                 print maps[x,y]
                maps[flags == 1] = maps[x, y]
                #     print maps[:,11]
                #     printNpList(maps)
    cData[maps[:height, :width] < 40] = 255
    cData[cData > 200] = 255
    clearData(npData, depth - 1)
    return cData


def floodFill(cData, x, y, width, height):
    if x < 0 or y < 0 or x >= width or y >= height:
        return 0

    if isProcess[x, y] == 1:
        return 0

    if cData[x, y] != 255:
        # 全局标记表
        isProcess[x, y] = 1

        flags[x, y] = 1
        area = 1
        area += floodFill(cData, x - 1, y, width, height)
        area += floodFill(cData, x + 1, y, width, height)
        area += floodFill(cData, x, y - 1, width, height)
        area += floodFill(cData, x, y + 1, width, height)

        return area
    else:
        return 0


def cropImg(npData=None):
    #     npData = np.array([[1,2],[11,22],[33,44]])
    npData[npData != 255] = 1
    npData[npData == 255] = 0
    printNpList(npData, outName="../sources/sumImg.txt")
    sumData = npData.sum(0)
    # print sumData
    return sumData


def getSeq4Char(inputFile="../sources/mark4SingleChar.txt"):
    seq4Char = {}
    with open(inputFile, "r") as fp:
        txt = fp.readline().strip()
        while txt:
            k, v = txt.split("\t")
            if v != "N": seq4Char[k] = v
            txt = fp.readline().strip()
    return seq4Char


def getResultSeq(langSeq):
    maps = {}
    for k, v in seq4Char.items():
        la = len(langSeq)
        lb = len(v)
        i = 0
        while lb + i <= la:
            sub1 = langSeq[i:lb + i]
            res = lcs(sub1, v)
            if res >= int(lb * 0.8):
                maps[i] = k
                i += lb
                continue
            i += 1
    # print sorted(maps.keys())
    ans = ""
    for x in sorted(maps.keys()):
        ans += maps[x]
    return ans


def getNum2CharMap():
    ncMap = {}
    for num in range(38):
        if num < 10:
            ncMap[num] = str(num)
        else:
            ncMap[num] = chr(num + 87)
    return ncMap


if __name__ == '__main__':
    # seq4Char = getSeq4Char()
    # exit()

    #     im = Image.open("E:/codes/code%d.png" % 2)
    #     box = (0,0,20,37)
    #     im2 = im.crop(box)
    #     im2.show()
    #     print "finish!"
    seq4Char = getSeq4Char()
    num2CharMap = getNum2CharMap()
    for i in range(50, 101):
        maps = np.zeros([50, 300], dtype=int)
        flags = np.zeros([50, 300], dtype=int)
        isProcess = np.zeros([50, 300], dtype=int)
        #     print maps.shape
        im = Image.open("E:/codes/code%d.png" % i)  # the second one
        (w, h) = im.size
        data1 = im.getdata()
        npData1 = np.array(list(data1)).reshape((h, w))
        printNpList(npData1, outName="../sources/orgImg.txt")
        # 灰度处理
        im = im.convert("L")
        #     im.Image.point(140)
        #    二值化，使用默认阈值：将非0值统一转化为255
        #     im = im.convert("1")
        #     im.show()
        #     im.save('E:/RAcode3.png')

        data = im.getdata()
        npData = np.array(list(data)).reshape((h, w))
        sumData = cropImg(npData)

        allStr = ''.join([num2CharMap[x] for x in sumData.tolist()])
        # print "code%d:" % i
        # print allStr
        # exit()
        res = getResultSeq(allStr)
        print "code%d:%s" % (i, res)
        continue

        clData = clearData(npData, 1)
        # 打印查看
        printNpList(clData)

        # 矩阵转化为图片
        imNew = Image.fromarray(clData)  # ,mode="LAB"
        imNew.save('E:/RAcode3.png', "png")

        #     print npData
        #     im = im.convert("1")
        #         im2 = Image.open('E:/RAcode3.png')
        #         im2.save('E:/RAcode3.png')
        #         im2.convert("L")
        #         enhancer = ImageEnhance.Contrast(imNew)
        #         imNew = enhancer.enhance(3)
        imNew.show()
    # text = pytesseract.image_to_string(imNew)
    #         print "E:/codes/code%d.png=>%s" % (i,text)

    print "finish!"
