# 这是一个获取学校最新通知，实时群发通知到邮箱的小程序。
# 测试运行环境
# python3.5
# ubuntu16.04 LTS
# Intel® Core™ i5-5200U CPU @ 2.20GHz × 4

from urllib.request import urlopen,HTTPError
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

# 定义一个爬虫类
# 爬取公告内容并且判断出是否有新公告
# 输入：url:目标网页，oldNotice:已发送过的公告
# 输出：Isworng:是否网页有变动，newNotice:新公告，MSG:邮件发送的内容
class Spider(object):
    def __init__(self,url,oldNotice):
        self.url = url                       # 目标网页
        self.oldNotice = oldNotice           # 以发送的公告
        self.newNotice = []                  # 实时爬取的公告
        self.timeList = []                   # 爬取公告的时间列表
        self.contentList = []                # 爬取公告的内容列表
        self.linkList = []                   # 爬取公告的链接列表
        self.IsWrong = 0                     # 判断爬虫是否正常运行

    def GetNewNotice(self):
        # 获取网页
        try:
            html = urlopen(self.url)
        except HTTPError as e:
            print(e)
            self.IsWrong = 1
            return None
        try:
            bsObj = BeautifulSoup(html.read(),"html5lib")
        except AttributeError as e:
            print(e)
            self.IsWrong = 1
            return None
        # 获取网页的目标标签，将公告内容，时间，链接存在三个列表里面
        try:
            ul = bsObj.find("ul",{"class":"notice-ul"}).findAll("a")
            time = bsObj.find("ul", {"class": "notice-ul"}).findAll("span")
            for c in ul:
                tmp = c.attrs["title"]
                self.contentList.append(tmp)
            for t in time:
                self.timeList.append(t.get_text())
            for l in ul:
                tmp = l.attrs["href"]
                self.linkList.append(tmp)
        except AttributeError as e:
            print(e,"tag is changed!")
            self.IsWrong = 1
            return None
        # 判断是否有新公告
        self.newNotice = self.contentList
        boolList = []
        for i,notice in enumerate(self.newNotice):
            if notice not in self.oldNotice:
                boolList.append(1)
            else:
                boolList.append(0)
        MSG = ''
        for index,b, in enumerate(boolList):
            if b == 1:
                MSG = MSG + '\n' + self.timeList[index] + ' ' + self.contentList[index] + '\n' + self.linkList[index]
        return self.newNotice,MSG,self.IsWrong

# 定义一个发送邮件的类
# 将新的公告内容群发到选定好的邮箱
# 输入：to:选定好的发送邮箱 MSG:邮件内容
class SendEmail(object):
    def __init__(self,to):
        self._user = "2054855317@qq.com"
        self._pwd = "rsijgrxkrjwkchad"             # passwd为qq邮箱授权码
        self._to = to

    # 发送邮件函数
    def Send(self,MSG):
        msg = MIMEText(MSG)
        msg["Subject"] = "new notice from xtu!"
        msg["From"]    = self._user
        for cumster in self._to:
            msg["To"] = cumster
            try:
                s = smtplib.SMTP_SSL("smtp.qq.com", 465)
                s.login(self._user, self._pwd)
                s.sendmail(self._user, self._to, msg.as_string())
                s.quit()
                print(cumster)
                print("\n")
                print("Success!")
            except smtplib.SMTPException as e:
                print("Falied,%s",e)

if __name__ == "__main__":
    url = 'http://www.xtu.edu.cn/'
    oldNoice = [0,0,0]
    to = ["2054855317@qq.com", "z.x.j@foxmail.com"]
    while 1:
            spider = Spider(url,oldNoice)
            send = SendEmail(to)
            spiderResponse = spider.GetNewNotice()
            oldNoice = spiderResponse[0]
            MSG = spiderResponse[1]
            # 判断是否有新公告
            if len(MSG) != 0:
                send.Send(MSG)
            time.sleep(3600)
            # 判断爬虫是否正常运行
            if spiderResponse[2] == 1:
                send.Send("something wrong happened,you need to check your code!")
                break








