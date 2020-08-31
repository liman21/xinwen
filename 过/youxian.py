import time,html,uuid
from dao import Mysql
import requests,json,random,re
from lxml import etree
from selenium import webdriver
import urllib.request
from urllib.parse import quote
from datetime import datetime

# todo  萍乡市人民政府
def pingxiang1():
    try:
        url1s=[
            # 'http://www.pingxiang.gov.cn/xw/pxyw/zwyw1/',  # 政务要闻  25页
            # 'http://www.pingxiang.gov.cn/xw/pxyw/ldyl/',  # 领导言论  16页
            # 'http://www.pingxiang.gov.cn/xw/pxyw/zyhy/',  # 重要会议    18页
            # 'http://www.pingxiang.gov.cn/xw/pxyw/zyhy_44485/',  # 专题会议
            # 'http://www.pingxiang.gov.cn/xw/pxyw/bmdt/',    # 部门动态
            # 'http://www.pingxiang.gov.cn/xw/pxyw/xqxw/',    # 区县新闻
            # 'http://www.pingxiang.gov.cn/xw/pxyw/mrzw/',    # 每日政务
            'http://www.pingxiang.gov.cn/xw/pxyw/tpxw/',    # 图片新闻
        ]
        for url1 in url1s:
            print("程序已启动，稍等几秒")
            chromeOptions = webdriver.ChromeOptions()
            chromeOptions.add_experimental_option('w3c', False)
            chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
            chromeOptions.add_argument('--headless')  # 隐藏浏览器
            # chromeOptions.add_argument(f'--proxy-server={ipmax()}')
            driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
            driver.get(url=url1)
            aoo_11 = driver.page_source  # html
            pages=re.findall('总共(\d+)页',aoo_11)
            print(f'共{pages[0]}页')
            for aa in range(1, int(pages[0])):
                if driver.find_element_by_xpath("//td[@class='font_hei12']/input[@id='CP']"):
                    driver.find_element_by_xpath("//td[@class='font_hei12']/input[@id='CP']").clear()  # 清除文本框内容
                else:
                    driver.find_element_by_xpath("//input[@id='ctl00$ContentPlaceHolder1$AspNetPager1_input']").clear()  # 清除文本框内容
                driver.find_element_by_xpath("//tr[3]/td[@class='font_hei12']/input[@id='CP']").send_keys(aa)  # 搜索框输入内容
                driver.find_element_by_xpath("//tr[3]/td[@class='font_hei12']/input[2]").click()  # 点击一下按钮

                aoo_1 = driver.page_source  # html
                html_1 = etree.HTML(aoo_1)
                list_num = html_1.xpath(f"//table/tbody/tr[1]/td[@class='font_hei14']/a")  # 详情url
                for i in range(1, len(list_num)+1):  # 一页20条数据
                    link = html_1.xpath(f"//table[{i}]/tbody/tr[1]/td[@class='font_hei14']/a/@href")[0].strip()  # 详情url
                    title = html_1.xpath(f"//table[{i}]/tbody/tr[1]/td[@class='font_hei14']/a/text()")[0].strip()  # 标题
                    publicTime = html_1.xpath(f"//tr[2]/td[@class='borderhui']/table[{i}]/tbody/tr[1]/td[@class='font_hui12']/text()")[0].strip().replace('\n','') .replace('[','') .replace(']','') .replace('                ','')  # 时间
                    # tt = int(time.time())
                    s = publicTime.replace('/', '-')
                    t = int(datetime.strptime(s, '%Y-%m-%d').timestamp())
                    if t >= 1570896000:
                        if re.findall('xinhuan',link):
                            linkurl=link
                        else:
                            linkurl = url1 + link[1:]  # url
                        driver.find_element_by_xpath(f"//table[{i}]/tbody/tr[1]/td[@class='font_hei14']/a").click()
                        driver.switch_to.window(driver.window_handles[-1])
                        detail_res=driver.page_source
                        Html = etree.HTML(detail_res)
                        if Html.xpath("//table[3]/tbody/tr/td[@class='font_hui12']"):
                            div1 = Html.xpath("//table[3]/tbody/tr/td[@class='font_hui12']")[0]  # 当前栏目
                            div2 = Html.xpath("//table[@class='borderhui']/tbody/tr/td")[0]       # text
                        elif Html.xpath("//div/div/div[@class='news-position']"):
                            div1 = Html.xpath("//div/div/div[@class='news-position']")[0]  # 当前栏目
                            div2 = Html.xpath("//div/div/div[@id='p-detail']")[0]  # text
                        elif Html.xpath("//div[@class='padd']/div[@class='BreadcrumbNav']"):
                            div1 = Html.xpath("//div[@class='padd']/div[@class='BreadcrumbNav']")[0]  # 当前栏目
                            div2 = Html.xpath("//div[@class='article oneColumn pub_border']")[0]  # text
                        else:
                            div1 = Html.xpath("//div[@class='xl-main']/div[@class='container']")[0]  # 当前栏目
                            div2 = '' # text
                        try:
                            infocontent1 = html.unescape(etree.tostring(div1, method='html').decode()).replace("'", " ").replace(
                                '"', ' ')  # html
                            infocontent2 = html.unescape(etree.tostring(div2, method='html').decode()).replace("'", " ").replace(
                                                '"', ' ')  # html
                            infocontent=infocontent1+infocontent2
                        except:
                            infocontent1 = html.unescape(etree.tostring(div1, method='html').decode()).replace("'",  " ").replace( '"', ' ')  # html
                            infocontent=infocontent1
                        if re.findall('src="(.*?)" oldsrc=',infocontent):
                            infocontent=infocontent.replace('src=.\./',url1+link[1:7]+'/')
                        else:infocontent=infocontent
                        select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                        if len(select)==0:
                            uid = uuid.uuid4()
                            Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='360000', regionName='江西省', areaRegion='萍乡市',
                                                publicTime=publicTime, linkurl=linkurl, title=title,
                                                dataResource='', yewuType='人民政府', infoType='', infoState='', isok='',
                                                isdeal='')
                            Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                            print(f'标题【{title}】写入成功')

                        else:
                            print(f'标题【{title}】存在')
                        driver.back()  # 返回上一页
                        time.sleep(1)
                print('-' * 50 + f'萍乡第{aa}页已完成' + '-' * 50)
    except Exception as e:
        print('蚌埠\t', e)
        return pingxiang1()


# todo 萍乡市发改委
def pingxiang2():
    url='http://pxdpc.pingxiang.gov.cn/list.asp?classid=15'
    tt = requests.get(url).content.decode('utf-8')
    pages = re.findall('每页20条, 1/(\d+)页', tt)[0]
    print(f'共{pages}页')
    for page in range(1, int(pages) + 1):
        url1=url+f'&p={page}'
        tt = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
        contents = re.findall('&nbsp;                    <a href="(.*?)" target="_blank">(.*?)</a></td>                  <td width="11%" class="font_hui12">\[(.*?)\]</td>', tt)
        for content in contents:
            linkurl = 'http://pxdpc.pingxiang.gov.cn/' + content[0]
            detail_res = requests.get(linkurl).content.decode('utf-8').replace('/upload/','http://pxdpc.pingxiang.gov.cn/upload/')
            Html = etree.HTML(detail_res)
            # qufen = '发改委'+Html.xpath("//table[1]/tbody/tr/td[@class='font_hui12']/a[3]")[0]  # 当前栏目
            div1 = Html.xpath("/html/body/div[5]")[0]  # text
            infocontent = html.unescape(etree.tostring(div1, method='html').decode()).replace("'", " ").replace(
                '"', ' ')  # html
            title = content[1]
            publicTime = content[2].replace('                    ','')
            select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
            if len(select)==0:
                uid = uuid.uuid4()
                Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='360000', regionName='江西省', areaRegion='萍乡市',
                                             publicTime=publicTime, linkurl=linkurl, title=title,
                                             dataResource='', yewuType='发改委', infoType='', infoState='', isok='',
                                             isdeal='')
                Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
            else:
                print(f'第{page}页标题存在')
        print(f'第{page}页已爬完')

# todo 江西省公共交易中心
def pingxiang():
    try:
        for num in range(1,4):
            url=f'http://www.jxsggzy.cn/web/xwzx/00700{num}/1.html'
            tt = requests.get(url).content.decode('utf-8')
            pages = re.findall('id="index">1/(\d+)</span>', tt)[0]
            print(f'江西省公共交易中心共{pages}页')
            for page in range(1, int(pages) + 1):
                url1=url.replace('1.html',f'{page}.html')
                tt = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
                contents = re.findall('<li class="ewb-list-node clearfix">                            <a href="(.*?)"  title="(.*?)" target="_blank" class="ewb-list-name">(.*?)</a>                            <span class="ewb-list-date">(.*?)</span> ', tt)
                for con in range(1,len(contents)):
                    content=contents[con]
                    title = content[1]
                    publicTime = content[3]
                    linkurl = 'http://www.jxsggzy.cn' + content[0]
                    if re.findall('pdf|doc',content[0]):
                        infocontent='<embed src="'+linkurl+'" >'
                        urllib.request.urlretrieve(quote(linkurl, safe='/:?='), r'D:\lm\xinwen\江西省公共资源交易中心\\' + title + '.jpg')
                    else:
                        detail_res = requests.get(linkurl).content.decode('utf-8')
                        Html = etree.HTML(detail_res)
                        qufen='江西省公共交易中心'+Html.xpath("//p[@class='ewb-location-content']/span/text()")[0]
                        infocontent = html.unescape(etree.tostring(Html, method='html').decode()).replace("'", " ").replace(
                            '"', ' ')  # html
                    select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                    if len(select)==0:
                        uid = uuid.uuid4()
                        Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='360000', regionName='江西省', areaRegion='萍乡市',
                                                     publicTime=publicTime, linkurl=linkurl, title=title,
                                                     dataResource='', yewuType='江西省公共交易中心', infoType='', infoState='', isok='',
                                                     isdeal='')
                        Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                        print(f'{num} 标题【{title}】写入成功')
                    else:
                        print(f'{num} 标题【{title}】存在')
                print('-'*50+f'{num} 江西省公共交易中心第{page}页已写完'+'-'*50)
    except Exception as e:
        print('蚌埠\t', e)
        return pingxiang()

# todo 江西省产权交易中心
# 无

import threading
class MyThread(threading.Thread):
    def ready_go(self):
        try:
            pingxiang1()
            pingxiang2()
            pingxiang()
        except Exception as e:
            print('蚌埠\t', e)
            return MyThread.ready_go(self)
def test():
    for i in range(5):
        t = MyThread()
        t.ready_go()
if __name__=='__main__':
    test()

