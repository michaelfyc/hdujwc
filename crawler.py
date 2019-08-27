# @Author  : Michael
# @File    : crawler.py

import requests
from bs4 import BeautifulSoup as bs
import pymysql


#Forgive my awful python syntax...
#应该有不少可以优化的地方...

#Model/Entity
class TTL:
    def setTitle(self,title):
        self.title=title
    def setTime(self,time):
        self.time=time
    def setLink(self,link):
        self.link=link



class HDU():
    def __init__(self):
        self.__db_url = "localhost"
        self.__db_user = "#####"
        self.__db_password = "#####"
        self.__db_name = "local"


        self.base='http://jwc.hdu.edu.cn'
        # cxcy 创新创业
            # cxjy 创新教育
            # cyjy 创业教育
        # jwgl 教务管理
            # ksgl 考试管理
            # tzgg 通知公告
            # xjgl 学籍管理
            # pkxk 排课选课
            # cjgl 成绩管理
            # bygl 毕业管理
        # sj 实践教学
            # sjjx 实践教学
            # bysj 毕业设计
        self.section_no= {'cxcy': '400', 'jwgl': '394', 'sj': '399'}


    #获取指定页面内容
    def __get_page_content(self, url):
        response=requests.get(url=url,allow_redirects=True,timeout=10)
        return response.text

    #创建数据库链接
    def __createConnection(self):
        self.connection=pymysql.connect(self.__db_url, self.__db_user, self.__db_password, self.__db_name)
        self.cursor=self.connection.cursor(cursor=pymysql.cursors.DictCursor)

    # 关闭数据库连接
    def __closeConnection(self):
            self.connection.close()

    #根据指定模块返回该模块的链接,默认返回第一页
    def get_section_url(self,section='cxcy',page=1):
        if(type(page)!=type(1) or page<=0):
            print("page should be int greater than 0")
            raise ValueError
        if section in self.section_no.keys():
            node=self.section_no[section]
        else:
            print("No such section")
            raise ValueError
        if page==1:
            return self.base+"/node/"+node+".jspx"
        else:
            return self.base+"/node/"+node+"_"+str(page)+".jspx"

    #返回指定模块的公告的标题，发布时间和链接，返回对象列表
    def get_section_content(self,section='cxcy',page=1):
        content=self.__get_page_content(self.get_section_url(section=section, page=page))
        soup=bs(content,'lxml')
        ttls=[]

        for announcement in soup.find(name='div',attrs={"class":"newsList"}).findAll("li"):
            ttl=TTL()
            title = announcement.get_text()[:-10]
            time = announcement.get_text()[-10:]
            link = self.base + announcement.find(name="a")['href']
            ttl.setLink(link)
            ttl.setTime(time)
            ttl.setTitle(title)
            ttls.append(ttl)
        return ttls

    #获得所有模块的标题，发布时间和链接，返回列表，最后应该是[[]]形式，即列表列表
    def get_all_section_content(self):
        total=[]
        for section in self.section_no.keys():
            total.append(self.get_section_content(section=section))
        return total

    #将制定模块的内容批量插入数据库
    def __insert_section_batch(self,section='cxcy'):
        content=self.get_section_content(section=section)
        self.__createConnection()
        sql="insert ignore into jwc."+section+"(title,time,link) values(%s,%s,%s)"
        ttl=[]
        #print("正在插入"+section+"库中...")
        for li in content:
            temp=[]
            temp.append(li.title)
            temp.append(li.time)
            temp.append(li.link)
            ttl.append(temp)
        try:
            self.cursor.executemany(sql,ttl)
            self.connection.commit()
            #print("插入"+section+" 完毕！")
        except:
            print("插入"+section+" 失败！")
            self.connection.rollback()
        self.__closeConnection()


    #将爬取的所有模块的内容批量插入数据库
    def __insert_all_batch(self):
        total_content=self.get_all_section_content()
        self.__createConnection()
        sql = "insert ignore into jwc.together(title,time,link) values(%s,%s,%s)"

        ttl=[]
        #print("正在插入数据库...")
        #准备列表，批量插入
        for section_content in total_content:
            for li in section_content:
                temp = []
                temp.append(li.title)
                temp.append(li.time)
                temp.append(li.link)
                ttl.append(temp)

        try:
            self.cursor.executemany(sql,ttl)
            self.connection.commit()
            #print("插入together完毕！")
        except:
            print("插入together失败！")
            self.connection.rollback()
        self.__closeConnection()


    def __insert(self):
        for section in self.section_no.keys():
            self.__insert_section_batch(section=section)
        self.__insert_all_batch()

    #查询最新公告
    def __get__news(self,table='together',limit=10):
        self.__createConnection()
        sql="select title,time,link from jwc."+table+" order by time desc limit "+str(limit)
        ttls=[]
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            for announcement in results:
                ttl = TTL()
                ttl.setTitle(announcement['title'])
                ttl.setTime(announcement['time'].strftime("%Y-%m-%d"))
                ttl.setLink(announcement['link'])
                ttls.append(ttl)
        except:
            print("查询失败！")
        self.__closeConnection()
        return ttls

    #public方法，用户可以用来查询最近的几条内容
    def get_latest(self,section='together',latest=10):
        self.__insert()
        news=self.__get__news(table=section,limit=latest)

    #取消下面两行注释后，直接运行本python文件（python -W ignore crawler.py） 可以看到最新的10条公告
    #    for ttl in news:
    #        print(ttl.__dict__)

if __name__=="__main__":
    A=HDU()
    A.get_latest()