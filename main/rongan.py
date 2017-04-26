# coding:utf8

"""
 Created by YR on 2017/4/23.

"""
import requests
import time

from PIL import Image
from lxml import etree
from code import Code
import re


class Rongan:
    def __init__(self, userName, password):
        self.session = requests.session()
        self.header = {}
        self.name = userName
        self.password = password
        self.MAXCLASSOFONEDAY = 4
        self.rootUrl = "http://t1.ronganjx.com"
        self.loginUrl = self.rootUrl + '/Web11/logging/LoginUser.aspx'
        self.homeUrl = self.rootUrl + '/Web11/logging/BookingCarStudy.aspx'
        self.selectCoachUrl = self.rootUrl + '/Web11/logging/BookingCoachCW.aspx'
        self.header = self.getRequestHeaders()

        self.allTime = [0, 0, "07:00", "08:00", "09:00", "10:00", "11:00",
                        "12:30", "13:30", "14:30", "15:30", "16:30",
                        "17:30", "18:00", "19:00", "20:00", "21:00"]

    @staticmethod
    def getCoachID(coachName):
        """

        :param coachName: name of coach
        :return: id of coach
        """
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

    @staticmethod
    def downloadPic(picFullPath, picUrl):
        url = picUrl
        res = requests.get(url, stream=True)
        with open(picFullPath, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()

    @staticmethod
    def getRequestHeaders():
        """

        :rtype: object
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/56.0.2924.87 Safari/537.36',
        }

        return headers

    @staticmethod
    def addDict(dict2D, key_a, key_b, val):
        if key_a in dict2D:
            dict2D[key_a].update({key_b: val})
        else:
            dict2D.update({key_a: {key_b: val}})

    def downloadCodes(self, startNum, endNum):
        for i in range(startNum, endNum):
            codeUrl = self.getCodeUrl()
            time.sleep(1)
            self.downloadPic("../sources/codeImgs/code%d.png" % i, codeUrl)

    def getCodeUrl(self):
        resp = requests.get(self.loginUrl)
        html = etree.HTML(resp.text)
        codeUrl = self.rootUrl + html.xpath(u'//*[@id="ctl00_ContentPlaceHolder1_DIV1"]/img')[0].attrib['src']

        return codeUrl

    def getLogInFormData(self, codeNum=1):
        codePath = "../sources/code%d.png" % codeNum
        resp = requests.get(self.loginUrl)
        html = etree.HTML(resp.text)
        # 验证码
        codeUrl = html.xpath(u'//*[@id="ctl00_ContentPlaceHolder1_DIV1"]/img')[0].attrib['src']
        codeUrl = self.rootUrl + codeUrl
        self.downloadPic(codePath, codeUrl)
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
                    'ctl00$ContentPlaceHolder1$txtPupilNo': self.name,
                    'ctl00$ContentPlaceHolder1$txtWebPwd': self.password,
                    'ctl00$ContentPlaceHolder1$txtCode': codeStr,
                    'ctl00$ContentPlaceHolder1$ibtnLogin.x': '20',
                    'ctl00$ContentPlaceHolder1$ibtnLogin.y': '18'
                    }

        return formData

    def getCoachFormData(self, coachID):
        resp = self.session.get(self.selectCoachUrl)
        html = etree.HTML(resp.text)
        VIEWSTATE = html.xpath(u'//*[@id="__VIEWSTATE"]')[0].attrib['value']
        EVENTVALIDATION = html.xpath(u'//*[@id="__EVENTVALIDATION"]')[0].attrib['value']
        formData = {'__VIEWSTATE': VIEWSTATE,
                    '__VIEWSTATEGENERATOR': "BF9C7FAF",
                    '__EVENTVALIDATION': EVENTVALIDATION,
                    'ctl00$ContentPlaceHolder2$ddlCoachInfo': coachID,
                    'ctl00$ContentPlaceHolder2$btnSubmit': u"提  交"
                    }

        return formData

    def getBookingFormData(self, url, trainType, trainDate):
        resp = self.session.get(url)
        html = etree.HTML(resp.text)
        VIEWSTATE = html.xpath(u'//*[@id="__VIEWSTATE"]')[0].attrib['value']
        VIEWSTATEGENERATOR = html.xpath(u'//*[@id="__VIEWSTATEGENERATOR"]')[0].attrib['value']
        formData = {'__VIEWSTATE': VIEWSTATE,
                    '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                    'ctl00$ContentPlaceHolder2$ddlDLExam': u"----请选择----",
                    'ctl00$ContentPlaceHolder2$ddlTrainType': trainType,
                    'ctl00$ContentPlaceHolder2$txtBookingClassDate': trainDate,
                    }

        return formData

    def getOneClassFormData(self, url, bookingFormData):
        resp = self.session.post(self.rootUrl + "/Web11/logging/" + url, data=bookingFormData, headers=self.header)
        # print resp.text
        html = etree.HTML(resp.text)
        url2 = html.xpath('//*[@id="aspnetForm"]')[0].attrib['action']
        VIEWSTATE = html.xpath(u'//*[@id="__VIEWSTATE"]')[0].attrib['value']
        EVENTVALIDATION = html.xpath(u'//*[@id="__EVENTVALIDATION"]')[0].attrib['value']
        VIEWSTATEGENERATOR = html.xpath(u'//*[@id="__VIEWSTATEGENERATOR"]')[0].attrib['value']
        formData = {'__VIEWSTATE': VIEWSTATE,
                    '__EVENTVALIDATION': EVENTVALIDATION,
                    '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                    'ctl00$ContentPlaceHolder2$time': 'radio4',
                    '_EVENTTARGET': 'ctl00$ContentPlaceHolder2$ddlLine',
                    'ctl00$ContentPlaceHolder2$ddlLine': u"地铁7号线(2)",
                    'ctl00$ContentPlaceHolder2$ddlStationAndTime': u'---请选择---',
                    }
        # print formData
        # print self.rootUrl + "/Web11/logging/" + url2
        resp = self.session.post(self.rootUrl + "/Web11/logging/" + url2, data=formData, headers=self.header)
        html2 = etree.HTML(resp.text)

        VIEWSTATE = html2.xpath(u'//*[@id="__VIEWSTATE"]')[0].attrib['value']
        EVENTVALIDATION = html2.xpath(u'//*[@id="__EVENTVALIDATION"]')[0].attrib['value']
        VIEWSTATEGENERATOR = html2.xpath(u'//*[@id="__VIEWSTATEGENERATOR"]')[0].attrib['value']
        formData2 = {'__VIEWSTATE': VIEWSTATE,
                     '__EVENTVALIDATION': EVENTVALIDATION,
                     '__VIEWSTATEGENERATOR': VIEWSTATEGENERATOR,
                     '__EVENTTARGET': 'ctl00$ContentPlaceHolder2$btnSubmit',
                     'ctl00$ContentPlaceHolder2$time': 'radio4',
                     'ctl00$ContentPlaceHolder2$ddlLine': u"地铁7号线(2)",
                     'ctl00$ContentPlaceHolder2$ddlStationAndTime': u'潘广路站(2)  08:40',
                     }

        return formData2

    def logIn(self, retries=10):
        if retries <= 0:
            raise Exception("多次尝试登录，验证码错误！")

        formData = self.getLogInFormData(11 - retries)
        self.session = requests.Session()
        resp = self.session.post(self.loginUrl, data=formData, headers=self.header)
        # print resp.text
        html = etree.HTML(resp.text)
        if html.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblInfo"]'):
            wrongCode = html.xpath('//*[@id="ctl00_ContentPlaceHolder1_lblInfo"]')[0].text
            if re.search(u"验证码.*不对", wrongCode):
                print "验证码(%s)错误，正在尝试再次登录..." % (formData["ctl00$ContentPlaceHolder1$txtCode"])

            time.sleep(1)
            self.logIn(retries - 1)

    def getClassStatus(self, table):
        classStatus = {}
        for tr in table:  # 行
            tds = tr.xpath('./td')
            cDate = ""
            num = 0
            for td in tds:  # 列
                if num == 0:
                    pass
                elif num == 1:
                    cDate = td.xpath('./span')[0].text
                elif td.xpath('./a'):  # 可预约的课程
                    href = re.search('"(Book.+?)"', td.xpath('./a[@href]')[0].attrib['href'])
                    self.addDict(classStatus, cDate, self.allTime[num], href.group(1))

                num += 1

        return classStatus

    def bookingOneClass(self, url, bookingFormData):

        formData = self.getOneClassFormData(url, bookingFormData)
        rp = self.session.post(self.rootUrl + "/Web11/logging/" + url, data=formData, headers=self.header)
        if re.search(u"综合考核", rp.text):
            print "预约成功！"
        # print rp.text
        # print url

    def bookingCarStudy(self, trainType, coachName, trainDate, trainHours):
        coachID = self.getCoachID(coachName)
        if coachID is None:
            raise Exception("没有找到 %s 教练信息，请检查！" % coachName)

        coachFormData = self.getCoachFormData(coachID)
        self.session.post(self.selectCoachUrl, data=coachFormData, headers=self.header)

        bookingFormData = self.getBookingFormData(self.homeUrl, trainType, trainDate)
        resp1 = self.session.post(self.homeUrl, data=bookingFormData, headers=self.header)
        # print resp1.text
        htl = etree.HTML(resp1.text)
        coachClassInfo = htl.xpath('//table[@id="ctl00_ContentPlaceHolder2_gvCoachInfo"]/tr')
        if not coachClassInfo:
            print resp1.text
            print "预约课程页面有误！"

        status = self.getClassStatus(coachClassInfo)
        # print status

        # bookingFormData2 = self.getBookingFormData2(self.homeUrl, trainType, trainDate)
        if trainDate in status:
            # print status[trainDate]
            for i in range(min(self.MAXCLASSOFONEDAY, len(trainHours))):
                if trainHours[i] in status[trainDate]:
                    self.bookingOneClass(status[trainDate][trainHours[i]], bookingFormData)


if __name__ == '__main__':
    userName = 'test'
    password = '123456'

    tType = u"场外"
    coach = u"胡晔"
    date = "2017-05-04"
    hours = ["09:00", "12:30", "16:30"]

    stu = Rongan(userName, password)
    stu.logIn()
    if stu.session:
        print "登录成功！"
        stu.bookingCarStudy(tType, coach, date, hours)
