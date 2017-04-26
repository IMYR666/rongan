# coding:utf8
"""
Created on 2017年3月24日

@author: dict
"""

import requests
import time

from PIL import Image
from lxml import etree
from code import Code
import re


def downloadPic(picFullPath, picUrl):
    url = picUrl
    # print url
    res = requests.get(url, stream=True)
    with open(picFullPath, 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()


def getRequestHeaders():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
        Chrome/56.0.2924.87 Safari/537.36',
    }

    return headers


def getCodeUrl(url, loginUrl=None):
    resp = requests.get(loginUrl)
    html = etree.HTML(resp.text)
    # 验证码

    codeUrl = html.xpath(u'//*[@id="ctl00_ContentPlaceHolder1_DIV1"]/img')[0].attrib['src']
    codeUrl = url + codeUrl

    return codeUrl


def getFormData(url, loginUrl=None, useName=None, password=None, codeNum=1):
    codePath = "../sources/code%d.png" % codeNum
    resp = requests.get(loginUrl)
    html = etree.HTML(resp.text)
    # 验证码
    codeUrl = html.xpath(u'//*[@id="ctl00_ContentPlaceHolder1_DIV1"]/img')[0].attrib['src']
    codeUrl = url + codeUrl
    downloadPic(codePath, codeUrl)
    im = Image.open(codePath)
    iCode = Code()
    codeStr = iCode.identify(im)
    # codeStr = "test"
    # print codeStr
    # 其他参数
    VIEWSTATE = html.xpath(u"//input[@name='__VIEWSTATE']")[0].attrib['value']
    VIEWSTATEGENERATOR = html.xpath(u"//input[@name='__VIEWSTATEGENERATOR']")[0].attrib['value']
    EVENTVALIDATION = html.xpath(u"//input[@name='__EVENTVALIDATION']")[0].attrib['value']
    formData = {'__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                '__EVENTVALIDATION': EVENTVALIDATION,
                'ctl00$ContentPlaceHolder1$txtPupilNo': useName,
                'ctl00$ContentPlaceHolder1$txtWebPwd': password,
                'ctl00$ContentPlaceHolder1$txtCode': codeStr,
                'ctl00$ContentPlaceHolder1$ibtnLogin.x': '20',
                'ctl00$ContentPlaceHolder1$ibtnLogin.y': '18'
                }

    return formData


def readCode(codePath=None):
    code = ''
    return code


def readCodeSimple(picFullPath, codeUrl):
    downloadPic(picFullPath, codeUrl)
    print "验证码路径：" + picFullPath

    code = raw_input("请输入验证码：")
    return code


def downloadCodes(startNum, endNum):
    for i in range(startNum, endNum):
        codeUrl = getCodeUrl(rootUrl, loginUrl)
        time.sleep(1)
        downloadPic("../sources/codeImgs/code%d.png" % i, codeUrl)


def logIn(header, retries=10):
    if retries <= 0:
        raise Exception("多次尝试登录，验证码错误！")

    formData = getFormData(rootUrl, loginUrl, "07025089", "633706", 11 - retries)
    session = requests.Session()
    resp = session.post(loginUrl, data=formData, headers=header)
    # print resp.text
    html = etree.HTML(resp.text)
    if html.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblInfo"]'):
        wrongCode = html.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblInfo"]')[0].text
        if re.search(u"验证码.*不对", wrongCode):
            print "验证码(%s)错误，正在尝试再次登录..." % (formData["ctl00$ContentPlaceHolder1$txtCode"])

        time.sleep(1)
        logIn(header, retries - 1)

    return session


def getBookingFormData(session, url, trainDate, trainType=u"场外"):
    resp = session.get(url)
    html = etree.HTML(resp.text)
    VIEWSTATE = html.xpath(u'//*[@id="__VIEWSTATE"]')[0].attrib['value']
    formData = {'__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': "2DF6698D",
                'ctl00$ContentPlaceHolder2$ddlDLExam': u"----请选择----",
                'ctl00$ContentPlaceHolder2$ddlTrainType': trainType,
                'ctl00$ContentPlaceHolder2$txtBookingClassDate': trainDate,
                }

    return formData


def getCoachFormData(session, url, coachID):
    resp = session.get(url)
    html = etree.HTML(resp.text)
    VIEWSTATE = html.xpath(u'//*[@id="__VIEWSTATE"]')[0].attrib['value']
    # PREVIOUSPAGE = html.xpath(u'//*[@id="__PREVIOUSPAGE"]')[0].attrib['value']
    EVENTVALIDATION = html.xpath(u'//*[@id="__EVENTVALIDATION"]')[0].attrib['value']
    formData = {'__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEGENERATOR': "BF9C7FAF",
                '__EVENTVALIDATION': EVENTVALIDATION,
                'ctl00$ContentPlaceHolder2$ddlCoachInfo': coachID,
                'ctl00$ContentPlaceHolder2$btnSubmit': u"提  交"
                }

    return formData


def getCoachID(coachName):
    coachList = {u"王扣龙": "9007005431",
                 u"薛周来": "9016000673",
                 u"冯超": "9016001397",
                 u"钱伟杰": "9109015795",
                 u"张中良": "9110017853",
                 u"赵双华": "9110019169",
                 u"高海江": "9111019526",
                 u"赖庆华": "9111020289",
                 u"朱华亮": "9112022721",
                 u"黄嵩": "9112023752",
                 u"章波": "9112023768",
                 u"张胜蓉": "9112025325",
                 u"王大宁": "9113026121",
                 u"叶龙飞": "9114046451",
                 u"陈勇": "9114047311",
                 u"刘琼": "9115048481",
                 u"陆震宇": "9115049866",
                 u"胡田": "9115054839",
                 u"顾健侠": "9115055742",
                 u"周孝良": "9115056574",
                 u"施建国": "9212052724",
                 u"蔡亮": "9215052525",
                 u"金晓刚": "9215052583",
                 u"李玮": "9215054049",
                 u"胡晔": "9310056854",
                 u"范鸣亮": "9800000007",
                 }

    if coachList[coachName]:
        return coachList[coachName]
    else:
        return None


def getClassStatus(table):
    classStatus = {}
    for tr in table:  # 行
        tds = tr.xpath('./td')
        date = ""
        num = 0
        for td in tds:  # 列
            if num == 0:
                pass
            elif num == 1:
                date = td.xpath('./span')[0].text
            elif td.xpath('./a'):  # 可预约的课程
                href = re.search('"(Book.+?)"', td.xpath('./a[@href]')[0].attrib['href'])
                addDict(classStatus, date, allTime[num], href.group(1))
            num += 1

    return classStatus


def addDict(dict2D, key_a, key_b, val):
    if key_a in dict2D:
        dict2D[key_a].update({key_b: val})
    else:
        dict2D.update({key_a: {key_b: val}})


def bookingOneClass(session,url,bookingFormData):

    rp = session.post(rootUrl + url,data=bookingFormData,headers = header)
    print rp.text


def bookingCarStudy(session, trainType, coachName, trainDate, duration, hours):
    selectCoachUrl = rootUrl + '/Web11/logging/BookingCoachCW.aspx'
    coachID = getCoachID(coachName)
    if coachID is None:
        raise Exception("没有找到 %s 教练信息，请检查！" % coachName)

    coachFormData = getCoachFormData(session, selectCoachUrl, coachID)
    # print coachFormData
    rq = session.post(selectCoachUrl, data=coachFormData, headers=header)

    bookingFormData = getBookingFormData(session, userUrl, trainDate, trainType)
    resp1 = session.post(userUrl, data=bookingFormData, headers=header)
    # print resp1.text
    htl = etree.HTML(resp1.text)
    coachClassInfo = htl.xpath('//table[@id="ctl00_ContentPlaceHolder2_gvCoachInfo"]/tr')
    if not coachClassInfo:
        print resp1.text
        print "预约课程页面有误！"

    status = getClassStatus(coachClassInfo)
    print status

    if trainDate in status:
        print status[trainDate]
        for i in range(min(MAXCLASSOFONEDAY, len(hours))):
            if hours[i] in status[trainDate]:
                bookingOneClass(session,status[trainDate][hours[i]],bookingFormData)

    # print info.xpath('string(.)').replace('\n', '')
    # //*[@id="aspnetForm"]/table/tbody/tr/td[2]/table[2]/tbody/tr[3]


if __name__ == '__main__':
    rootUrl = "http://t1.ronganjx.com"
    loginUrl = rootUrl + '/Web11/logging/LoginUser.aspx'
    userUrl = rootUrl + '/Web11/logging/BookingCarStudy.aspx'
    trainType = u"场外"
    coach = u"胡晔"
    allTime = [0, 0, "07:00", "08:00", "09:00", "10:00", "11:00",
               "12:30", "13:30", "14:30", "15:30", "16:30",
               "17:30", "18:00", "19:00", "20:00", "21:00"]
    MAXCLASSOFONEDAY = 4
    trainDate = "2017-05-03"
    duration = 4
    hours = ["12:30"]
    # # downloadCodes(101, 110)
    header = getRequestHeaders()
    session = logIn(header)
    if session:
        print "登录成功！"
        # resp1 = session.post(homeUrl, headers=header)
        # bookingData = getBookingData(session, homeUrl)
        # resp1 = session.post(homeUrl, data=bookingData, headers=header)
        bookingCarStudy(session, trainType, coach, trainDate, duration, hours)
        # print resp1.text
