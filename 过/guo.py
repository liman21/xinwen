import time,html,uuid
from dao import Mysql
import requests,json,random,re,os,itertools
from lxml import etree
from urllib.request import urlretrieve

def guo():  # 国务院新闻
    url='http://sousuo.gov.cn/column/19423/0.htm'
    tt = requests.get(url).content.decode('utf-8')
    pages = re.findall('共(\d+)页', tt)[0]
    for page in range(int(pages)):
        url1=f'http://sousuo.gov.cn/column/19423/{page}.htm'
        tt1 = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
        contents = re.findall('<li><h4><a href="(.*?)" target="_blank">(.*?)</a><span class="date">(.*?)</span></h4></li>', tt1)
        for content in contents:
            linkurl = content[0]
            detail_res = requests.get(linkurl).content.decode('utf-8')
            Html = etree.HTML(detail_res)
            div = Html.xpath('/html/body/div[3]/div[2]/div[1]')[0]
            infocontent = html.unescape(etree.tostring(div, method='html').decode()).replace("'", " ").replace('"', ' ')
            title = content[1]
            publicTime = content[2]
            select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
            if len(select)==0:
                uid = uuid.uuid4()
                Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='000000', regionName='国务院', areaRegion='全国',
                                             publicTime=publicTime, linkurl=linkurl, title=title,
                                             dataResource='', yewuType='', infoType='', infoState='', isok='',
                                             isdeal='')
                Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
            else:
                print('标题存在')
guo()