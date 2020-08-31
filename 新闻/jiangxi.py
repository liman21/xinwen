# -*- coding: utf-8 -*-
import time, uuid, requests, json
from dao import Mysql
from lxml import etree
from selenium import webdriver
from datetime import datetime
from openpyxl import load_workbook
import re, os, shutil

from bs4 import BeautifulSoup
def ipmax():
    url = 'http://api.ip.data5u.com/dynamic/get.html?order=bd81442e74250355ff35a310705f13cb&json=1&sep=3'
    a = requests.get(url, timeout=5).text
    if not a.find('data') == -1:
        b = json.loads(a)['data']
        c = str(b[0]["ip"]) + ":" + str(b[0]["port"])
        ip = {"http": "http://" + c, "https": "https://" + c}
        return ip
    elif a.find('请控制好请求频率') != -1:
        time.sleep(1)
        return ipmax()
    else:
        return ipmax()
from urllib.request import urlopen
def deleteData(string: str, list: []):
    try:
        for i in list:
            if str(i) in string:
                string = string.replace(str(i), '')
    except Exception as e:
        return e
    return string
def qc_js(html):
    mio = []
    soup = BeautifulSoup(str(html), "html.parser")
    titles = soup.select("script")  # CSS 选择器
    for title in titles:
        mio.append(str(title))
    qc_cg = deleteData(str(soup), mio)

    return qc_cg
now = datetime.now()
def get_image(urls, pic_names):
    """
    基于selenium的长截图
    :param urls: 网站链接
    :param pic_names: 截图保存位置
    :return:
    """
    # 设置chrome开启的模式，headless就是无界面模式
    # 一定要使用这个模式，不然截不了全页面，只能截到你电脑的高度
    # lujing = 'D:\\zbbb\\chromedriver.exe'
    chromeOptions = webdriver.ChromeOptions()
    chromeOptions.add_argument('--headless')  # 隐藏浏览器
    # chromeOptions.add_argument(f'--proxy-server={ipmax()}')
    driver = webdriver.Chrome(options=chromeOptions,
                              executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    # chrome_options = Options()
    # chrome_options.add_argument('headless')
    # driver = webdriver.Chrome(options=chrome_options, executable_path=lujing)
    # 控制浏览器写入并转到链接
    driver.get(urls)
    # 接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法
    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    # 将浏览器的宽高设置成刚刚获取的宽高
    driver.set_window_size(width, height)
    # 截图并关掉浏览器
    driver.save_screenshot(pic_names)
    driver.close()
def mkdir(path):
    import os
    # function：新建文件夹
    # path：str-从程序文件夹要要创建的目录路径（包含新建文件夹名）
    # 去除首尾空格

    path = path.strip()  # strip方法只要含有该字符就会去除
    # 去除首尾\符号
    path = path.rstrip('\\')
    # 判断路径是否存在
    isExists = os.path.exists(path)

    # 根据需要是否显示当前程序运行文件夹
    # print("当前程序所在位置为："+os.getcwd())

    if not isExists:
        os.makedirs(path)
        return list
def fz_excel(pro, city):
    ''' 获取指定目录下的所有指定后缀的文件名 '''
    mkdir(rf'D:\lm\\xinwen\数据\\{pro}\\{city}')
    path = rf'D:\lm\\xinwen\数据\\{pro}\\{city}'
    f_list = os.listdir(path)
    if len(f_list) == 0:
        shutil.copy(rf'D:\lm\\xinwen\数据\列表.xlsx', rf'D:\lm\\xinwen\数据\\{pro}\\{city}\列表.xlsx')
def tj_excel(addr, shuju):
    """
    向excel添加数据
    :param addr: 路径
    :param shuju: 数据，例：['','']
    :return:
    """
    # 打开文件
    wb = load_workbook(addr)
    # 选择表单
    ws = wb["Sheet"]
    # 添加数据
    ws.append(shuju)
    # 保存，save（必须要写文件名（绝对地址）默认 py 同级目录下，只支持 xlsx 格式）
    wb.save(addr)

jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 7
gjzs = ['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子', '保险']
pro = '江西'

def chuli(publictime,href,driver,url,title,city,xpath1):
    try:
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if re.findall('http', href):
            link = href
        elif './' in href:
            link = url + href.replace('./', '')
        elif '../' in href:
            driver.find_element_by_xpath(f"{xpath1}/a").click()
            b_handle = driver.current_window_handle  # 获取当前页句柄
            handles = driver.window_handles  # 获取所有页句柄
            s_handle = None
            for handle in handles:
                if handle != b_handle:
                    s_handle = handle
            driver.switch_to.window(s_handle)  # 在新窗口操作
            link = driver.current_url  # 2级页面的url
            driver.close()
            driver.switch_to.window(b_handle)  # 在新窗口操作
        elif href[0] == '/':
            if re.findall(r'http(.*?)\.cn', url):
                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
            else:
                link = 'http' + re.findall(r'http(.*?)\.com', url)[0] + '.cn' + href
        else:
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/'+href
        uid = uuid.uuid4()
        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                           biaoti=title, tianjiatime=insertDBtime, zt='0')
        print(f'--{city}-【{title}】写入成功')

    except Exception as e:
        print('蚌埠\t', e)

# todo  江西  公共资源中心 | 发改委 (响应慢)|人民政府
def jiangxi(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.jxsggzy.cn/web/xwzx/007001/secondPage.html': 1,  # 公共资源中心 综合要闻
            'http://www.jxsggzy.cn/web/xwzx/007002/secondPage.html': 2,  # 公共资源中心 通知公告
            'http://www.jxsggzy.cn/web/xwzx/007003/secondPage.html': 3,  # 公共资源中心 地市动态
            'http://drc.jiangxi.gov.cn/col/col19282/index.html?uid=313784&pageNum=1': 16,  # 要闻
            'http://drc.jiangxi.gov.cn/col/col14585/index.html?uid=313784&pageNum=1': 15,  # 省发改动态
            'http://drc.jiangxi.gov.cn/col/col14590/index.html?uid=313784&pageNum=1': 28,  # 通知公告
            'http://www.jiangxi.gov.cn/col/col393/index.html?uid=45663&pageNum=1': 252,  # 人民政府 江西要闻
            'http://www.jiangxi.gov.cn/col/col396/index.html?uid=45663&pageNum=1': 11,  # 人民政府 最新发布
            'http://www.jiangxi.gov.cn/col/col398/index.html?uid=45663&pageNum=1': 154,  # 人民政府 部门资讯
            'http://www.jxcq.org/list.aspx?nid=83': 14,  # 产权交易中心 本所新闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jxcq' in url:
                xpath="//div[@class='m-ist-2']/ul/li/a"
            elif 'www.jxsggzy' in url:
                xpath="//div[@class='ewb-infolist']/ul/li/a"
            else:
                xpath = "//div[@class='default_pgContainer']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www.jiangxi' in url and i%7==0:
                        pass
                    else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        try:
                            title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip().replace('/','-')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                if 'jxcq' in url:
                                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                    link = 'http://www.jxcq.org' + href
                                    uid = uuid.uuid4()
                                    Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime,
                                                       url=link,
                                                       biaoti=title, tianjiatime=insertDBtime, zt='0')
                                    print(f'--{city}-【{title}】写入成功')
                                else:
                                    chuli(publictime, href, driver, url, title, city,xpath1)
                            else:
                                po += 1
                                break
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('江西\t', e)
        driver.close()
        return jiangxi(name)
# todo   江西(ij)  住建局
def jiangxi1(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.jxjst.gov.cn/col/col40686/index.html':2,  # 住建局 工作动态
            'http://zjt.jiangxi.gov.cn/col/col40683/index.html':1,  # 住建局 头条
            'http://zjt.jiangxi.gov.cn/col/col40684/index.html':7,  # 住建局 省厅信息
            'http://www.jxjst.gov.cn/col/col40687/index.html':17,  # 住建局 文件通知

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath="//div[@class='lucidity_pgContainer']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_2.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if  i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                except:
                                    driver.find_element_by_xpath(  "//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('江西1\t', e)
        driver.close()
        return jiangxi1(name)

# todo  南昌  公共资源中心| 行政审批局 | 发改委 |人民政府 | 住建局
def nanchang(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ncztb.nc.gov.cn/nczbw/xwzx/008001/MoreInfo.aspx?CategoryNum=008001': 2,  # 公共资源中心 综合新闻
            'http://ncztb.nc.gov.cn/nczbw/tzgg/MoreInfo.aspx?CategoryNum=009': 1,  # 公共资源中心 通知公告
            'http://xzspj.nc.gov.cn/ncspj/xwdt/nav_list.shtml': 36,  # 行政审批局 新闻动态
            'http://xzspj.nc.gov.cn/ncspj/dwdt/nav_list.shtml': 21,  # 行政审批局 单位动态
            'http://xzspj.nc.gov.cn/ncspj/xqdt/nav_list.shtml': 8,  # 行政审批局 区县动态
            'http://xzspj.nc.gov.cn/ncspj/mtbd/nav_list.shtml': 3,  # 行政审批局 媒体报道
            'http://xzspj.nc.gov.cn/ncspj/xxgg/nav_list.shtml': 5,  # 行政审批局 信息公告
            'http://fgw.nc.gov.cn/ncfzggw/tzgg/nav_list.shtml': 3,  # 发改委 通知公告
            'http://fgw.nc.gov.cn/ncfzggw/fgdt/nav_list.shtml': 34,  # 发改委 发展改革动态
            'http://www.nc.gov.cn/ncszf/ttxw/nav_list.shtml': 32,  # 人民政府 头条新闻
            'http://www.nc.gov.cn/ncszf/jrnc/nav_list.shtml': 134,  # 人民政府 今日南昌
            'http://www.nc.gov.cn/ncszf/bmdt/nav_list_bmdt.shtml': 110,  # 人民政府 部门动态
            'http://www.nc.gov.cn/ncszf/xqdt/nav_list.shtml': 42,  # 人民政府 县区动态
            'http://jw.nc.gov.cn/nccxjswyh/tzgg/nav_list.shtml': 7,  # 住建局 通知公告
            'http://jw.nc.gov.cn/nccxjswyh/tpxw/nav_list.shtml': 1,  # 住建局 图片新闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ncztb' in url:
                xpath="//tr[@class='liebiaobg']/td[2]/a"
            else:
                xpath="//ul[@class='item lh jt_dott f14']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]/').replace(']/td[', f'][{i}]/td[')
                    if 'ncztb' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t','').replace(
                                '\r', '')

                        publictime = html_1.xpath(f"{xpath1.replace('[2]/a','[3]')}/text()")[0].strip().replace('[','').replace(']','')
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        try:
                            title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('南昌\t', e)
        driver.close()
        return nanchang(name)

# todo  景德镇  公共资源中心 | 发改委 | 人民政府 | 住建局
def jingdezhen(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://jdzggzyjyzx.cn/xwzx/010002/about.html': 1,  # 公共资源中心 新闻中心 > 综合要闻 v
            'http://fg.jdz.gov.cn/zwgk/001001/001001001/list.html': 4,  # 发改委 工作动态
            'http://fg.jdz.gov.cn/zwgk/001001/001001002/list.html': 5,  # 发改委 公告公示
            'http://www.jdz.gov.cn/jrcd/second-page-son.html': 50,  # 人民政府 今日瓷都
            'http://www.jdz.gov.cn/xxgk/050006/second-page-son-moreleftmenu.html': 31,  # 人民政府 公告公示
            'http://www.jdz.gov.cn/xxgk/050026/second-page-son-moreleftmenu.html': 50,  # 人民政府 部门动态
            'http://www.jdz.gov.cn/xxgk/050025/second-page-son-moreleftmenu.html': 50,  # 人民政府 政务动态
            'http://zjj.jdz.gov.cn/nzcms_list_news.asp?id=734&sort_id=733': 9,  # 住建局 住建动态
            'http://zjj.jdz.gov.cn/nzcms_list_news.asp?id=737&sort_id=733': 1,  # 住建局 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fg' in url:
                xpath="//ul[@class='ewb-list-items']/li"
            elif 'www' in url:
                xpath="//ul/li[@class='clearfix']"
            elif 'zjj' in url:
                xpath="//td[2]/table[@class='dx']/tbody/tr/td[@class='p14']"
            else:
                xpath="//li[@class='wb-data-list']"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(16, length):
                    lengt = len(html_1.xpath(xpath))
                    if 'jdzggzyjyzx' in url:
                        xpath1 = xpath + f'[{i}]'
                        href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/div/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    elif 'zjj' in url:
                        xpath1 = xpath .replace("dx']/tbody/tr/td[@class='p14']",f"dx'][{i}]/tbody/tr/td")
                        href = html_1.xpath(f"{xpath1}[@class='p14']/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}[@class='p14']/a/@title")[0].strip().replace('标题：','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}[4]/text()")[0].strip().replace('发稿：','').replace('年','-').replace('月','-').replace('日','')
                    else:
                        xpath1 = xpath + f'[{i}]'
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        if i==18 and page==4:title=''
                        else:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()

                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('景德镇\t', e)
        driver.close()
        return jingdezhen(name)

# todo  萍乡   公共资源中心（无）| 发改委 | 人民政府 | 住建局
def pingxiang(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://pxdpc.pingxiang.gov.cn/list.asp?classid=15&p=1': 29,  # 发改委 工作动态
            'http://pxdpc.pingxiang.gov.cn/list.asp?classid=16&p=1': 1,  # 发改委 公告公示
            'http://www.pingxiang.gov.cn/xw/pxyw/zwyw1/index.html': 25,  # 人民政府 政务要闻
            'http://www.pingxiang.gov.cn/xw/pxyw/bmdt/': 25,  # 人民政府 部门动态
            'http://www.pingxiang.gov.cn/xw/pxyw/xqxw/': 25,  # 人民政府 县区新闻
            'http://zjj.pingxiang.gov.cn/list/?8.html': 6,  # 住建局 工作动态
            'http://zjj.pingxiang.gov.cn/list/?11.html': 9,  # 住建局 建设法规
            'http://zjj.pingxiang.gov.cn/aspcms/newslist/list-117-1.html': 1,  # 住建局 信息公开
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zjj' in url:
                xpath="//tr[2]/td[@class='jgg']/table/tbody/tr/td[2]"
            else:
                xpath="//td[@class='borderhui']/table/tbody/tr[1]/td[@class='font_hei14']"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if 'pxdpc' in url:
                    driver.get(url.replace('p=1',f'p={page}'))
                else:
                    pass
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace('le/t',f'le[{i}]/t')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'zjj' in url:
                        publictime=html_1.xpath(f"//tr[2]/td[@class='jgg']/table[{i}]/tbody/tr/td[@class='font2']/text()")[0].strip().replace('[','').replace(']','')
                    else:
                        publictime = html_1.xpath(f"{xpath1.replace('font_hei14','font_hui12')}/text()")[0].strip().replace('\n','').replace('[','').replace(']','').replace('/','-').replace('                    ','').replace('                ','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if 'pxdpc' in url:
                        pass
                    else:
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    if page != pages:
                                        try:
                                            try:
                                                driver.find_element_by_xpath('//tbody/tr/td/a[7]',html_2).click()
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
    except Exception as e:
        print('萍乡\t', e)
        driver.close()
        return pingxiang(name)


# todo  九江    公共资源中心(无法访问) |政务服务管理局 | 发改委
def jiujiang(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://zwfw.jiujiang.gov.cn/zwzx_206/tpbd/': 29,  # 政务服务管理局 图片报道
            'http://zwfw.jiujiang.gov.cn/zwzx_206/gzdt/': 7,  # 政务服务管理局 工作动态
            'http://zwfw.jiujiang.gov.cn/zwzx_206/gggs/': 2,  # 政务服务管理局 公告公示
            'http://fgw.jiujiang.gov.cn/zwzx_205/gzdt/': 21,  # 发改委 工作动态
            'http://fgw.jiujiang.gov.cn/zwzx_205/tpbd/': 1,  # 发改委 图片报道
            'http://fgw.jiujiang.gov.cn/zwzx_205/gggs/': 1,  # 发改委 公告公示
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath="//ul[@class='uli14 nowrapli list-date padding-hz-5 list-dashed']/li"
            else:
                xpath="//ul[@class='is-listnews']/li"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath+f'[{i}]'
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if 'pxdpc' in url:
                        pass
                    else:
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
    except Exception as e:
        print('九江\t', e)
        driver.close()
        return jiujiang(name)

# todo   九江(ij)  人民政府 | 住建局
def jiujiang1(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.jiujiang.gov.cn/zwzx/jrjj/':50,  # 人民政府 今日九江
            'http://www.jiujiang.gov.cn/zwzx/bmyw/':50,  # 人民政府 部门信息
            'http://www.jiujiang.gov.cn/zwzx/xqcz/':50,  # 人民政府 县区传真
            'http://www.jiujiang.gov.cn/zwzx/gggs/':7,  # 人民政府 公告公示
            'http://www.jiujiang.gov.cn/zwzx/szfdt/':16,  # 人民政府 江西时政
            'http://zjj.jiujiang.gov.cn/zwzx_208/xwbd/gzdt/':16,  # 住建局 工作动态
            'http://zjj.jiujiang.gov.cn/zwzx_208/xwbd/xtdt/':29,  # 住建局 系统动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'zjj' in url:
                xpath="//div[@class='clist_con']/ul/li"
            else:
                xpath = "//div[@class='contentRight']/ul/li"
            jj = 5
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, jj):
                    xpath2 = xpath.replace('l/li', f'l[{j}]/li')
                    ii=len(html_1.xpath(xpath2))+1
                    for i in range(1, ii):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace('l/li', f'l[{j}]/li[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            try:
                                publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                                publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            except:
                                publictime = html_1.xpath(f"{xpath1}span/a/text()")[0].strip()
                                publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1)
                            else:
                                po += 1
                                break
                        if (j - 1) * 5 + i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        if 'zjj' in url:pass
                                        else:
                                            b_handle = driver.current_window_handle  # 获取当前页句柄
                                            driver.close()
                                            handles = driver.window_handles  # 获取所有页句柄
                                            s_handle = None
                                            for handle in handles:
                                                if handle != b_handle:
                                                    s_handle = handle
                                            driver.switch_to.window(s_handle)  # 在新窗口操作
                                    except:
                                        driver.find_element_by_xpath(  "//a[@class='default_pgBtn default_pgNext']").click()
                            break
    except Exception as e:
        print('九江1\t', e)
        driver.close()
        return jiujiang1(name)

# todo  新余    发改委 | 人民政府 |住建局
def xinyu(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://fgw.xinyu.gov.cn/xyfgw/c102285/list.shtml': 2,  # 发改委 通知公告
            'http://fgw.xinyu.gov.cn/xyfgw/c102283/list.shtml': 27,  # 发改委 工作动态
            'http://fgw.xinyu.gov.cn/xyfgw/c102284/list.shtml': 4,  # 发改委 图片新闻
            'http://www.xinyu.gov.cn/xyywn2/list.shtml': 23,  # 人民政府 新余要闻
            'http://www.xinyu.gov.cn/swdtn/list.shtml': 23,  # 人民政府 工作动态 > 市委动态
            'http://www.xinyu.gov.cn/zfdtpm/list.shtml': 16,  # 人民政府 工作动态 > 政府动态
            'http://www.xinyu.gov.cn/qxdtn/list.shtml': 15,  # 人民政府 工作动态 > 县区动态
            'http://www.xinyu.gov.cn/zwgg/list.shtml': 4,  # 人民政府 公示公告 > 政务公告
            'http://zjw.xinyu.gov.cn/c101868/list.shtml': 8,  # 住建局 新闻中心
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath="//trs_documents[@id='owner']/ul/li"
            elif 'zjw' in url:
                xpath="//tr[3]//tr[2]//tr/td[2]"
            else:
                xpath="//ul[@class='lph_listnrqj']/li"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace('/li',f'/li[{i}]').replace('tr/t',f'tr[{i}]/t')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'fgw' in url:
                        publictime = html_1.xpath(f"{xpath1}/p/text()")[0].strip()
                    elif 'zjw' in url:
                        publictime = html_1.xpath(f"{xpath1.replace('td[2]', 'td[3]')}/text()")[0].strip()
                    else:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if 'pxdpc' in url:
                        pass
                    else:
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                            break
    except Exception as e:
        print('新余\t', e)
        driver.close()
        return xinyu(name)

# todo  鹰潭    发改委 |人民政府 |住建局
def yingtan(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://fgw.yingtan.gov.cn/zwgk/gzdt/sfgwdt/': 17,  # 发改委 市发改委动态
            'http://fgw.yingtan.gov.cn/zwgk/tztg/gztz/': 7,  # 发改委 工作通知
            'http://www.yingtan.gov.cn/dtxx/zwyw/': 25,  # 人民政府 政务要闻
            'http://www.yingtan.gov.cn/dtxx/tpxw/': 8,  # 人民政府 图片新闻
            'http://www.yingtan.gov.cn/dtxx/gggs/': 16,  # 人民政府 公告公示
            'http://www.yingtan.gov.cn/dtxx/gzdt/ztxq/': 25,  # 人民政府  县区、部门动态 >> 区（市）动态
            'http://www.yingtan.gov.cn/dtxx/gzdt/bmdt/': 25,  # 人民政府  县区、部门动态 >>部门动态
            'http://zjj.yingtan.gov.cn/zjdt/gzdt/': 7,  # 住建局  工作动态
            'http://zjj.yingtan.gov.cn/zjdt/tpxw/': 5,  # 住建局  图片新闻
            'http://zjj.yingtan.gov.cn/gsgg/': 4,  # 住建局  公告公示
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath="//table/tbody/tr[1]/td[@class='f12_h'][2]"
            elif 'zjj' in url:
                xpath="//div[@class='list_news_lb']/ul/li"
            else:
                xpath="//ul/li[@class='xxgk_tygl_news link12b']"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace("2b']",f"2b'][{i}]").replace('ble/tb',f'ble[{i}]/tb').replace(']/ul/li',f']/ul/li[{i}]')
                    if 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}/a[2]/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a[2]/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1.replace('[2]','[3]')}/text()")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'zjj' in url:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','')
                        else:
                            publictime = html_1.xpath(f"{xpath1.replace('xxgk_tygl_news','xxgk_tygl_time')}/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                except:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                        break
    except Exception as e:
        print('鹰潭\t', e)
        driver.close()
        return yingtan(name)

# todo  赣州   行政审批局 | 人民政府（响应慢）
def ganzhou(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://spj.ganzhou.gov.cn/gzdt/bsxw/zxxw/': 10,  # 行政审批局 新闻动态
            'http://spj.ganzhou.gov.cn/gzdt/bsxw/xsdt/': 5,  # 行政审批局 市县动态
            'http://spj.ganzhou.gov.cn/gzdt/tzgg/': 5,  # 行政审批局 通知公告
            'http://spj.ganzhou.gov.cn/gzdt/zcfg/sjzcfg/': 1,  # 行政审批局 市政策法规
            'https://www.ganzhou.gov.cn/c100022/list.shtml': 36,  # 人民政府 政务动态
            'https://www.ganzhou.gov.cn/c100023/list.shtml': 6,  # 人民政府 通知公告
            'https://www.ganzhou.gov.cn/c100024/list_bmqx.shtml': 36,  # 人民政府 部门动态
            'https://www.ganzhou.gov.cn/c100025/list_bmqx.shtml': 36,  # 人民政府 区县动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath="//div[@class='bd']/ul/li"
            else:
                xpath="//ul[@class='nynewslistul fl']/li"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/li',f']/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    try:
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    except:
                        title = html_1.xpath(f"{xpath1}/a/strong/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','').replace('时间：','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                except:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                        break
    except Exception as e:
        print('赣州\t', e)
        driver.close()
        return ganzhou(name)
# todo  赣州   发改委
def ganzhou1(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://dpc.ganzhou.gov.cn/n2339/n2347/n2383/index.html': 22,  # 发改委 本委
            'http://dpc.ganzhou.gov.cn/n2339/n2347/n2384/index.html': 28,  # 发改委 县（市、区）
            'http://dpc.ganzhou.gov.cn/n2339/n2348/index.html': 6,  # 发改委 通知公告
            'http://dpc.ganzhou.gov.cn/n3114/n3116/index.html': 1,  # 发改委 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath="//ul[@id='comp_42423']/li"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/li',f']/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    if './' in href:
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            driver.find_element_by_xpath(f"{xpath1}/a").click()
                            time.sleep(1)
                            b_handle = driver.current_window_handle  # 获取当前页句柄
                            handles = driver.window_handles  # 获取所有页句柄
                            s_handle = None
                            for handle in handles:
                                if handle != b_handle:
                                    s_handle = handle
                            driver.switch_to.window(s_handle)  # 在新窗口操作
                            link = driver.current_url  # 2级页面的url
                            con3 = driver.page_source
                            html_3 = etree.HTML(con3)
                            publictime = html_3.xpath("//div[@class='t']/p/text()")[0].replace("发布日期：", "")[:10]
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                                uid = uuid.uuid4()
                                go = 0
                                fo = 0
                                for gjz in gjzs:
                                    if gjz in title:
                                        print('含有关键字')
                                        reqcon = qc_js(con3)
                                        fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                        if fj > 0:
                                            fo += 1
                                            print(f'有附件{fj}个')

                                        go += 1
                                        driver.back()
                                        break

                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                                # if go > 0:
                                #     Mysql.update_xw_nr(biaoti=title, zt='1')
                                if fo > 0:
                                    Mysql.update_xw_xz(biaoti=title, xz='1')
                                else:
                                    Mysql.update_xw_xz(biaoti=title, xz='0')
                            else:
                                po += 1
                                break

                            driver.close()
                            driver.switch_to.window(b_handle)  # 在新窗口操作
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text(' > '))
                            break
    except Exception as e:
        print('赣州1\t', e)
        driver.close()
        return ganzhou1(name)
# todo   赣州(ij) 住建局
def ganzhou2(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://zjj.ganzhou.gov.cn/Category/Index/128/0/1/0':16,  # 住建局 本局动态
            'http://zjj.ganzhou.gov.cn/Category/Index/200/0/1/0':8,  # 人民政府 区县动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='content']/ul/li"
            jj = 6
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, jj):
                    xpath2 = xpath.replace('l/li', f'l[{j}]/li')
                    ii=len(html_1.xpath(xpath2))+1
                    for i in range(1, ii):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace('l/li', f'l[{j}]/li[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('· ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()[:10]
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1)
                            else:
                                po += 1
                                break
                        if (j - 1) * 5 + i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        if 'zjj' in url:pass
                                        else:
                                            b_handle = driver.current_window_handle  # 获取当前页句柄
                                            driver.close()
                                            handles = driver.window_handles  # 获取所有页句柄
                                            s_handle = None
                                            for handle in handles:
                                                if handle != b_handle:
                                                    s_handle = handle
                                            driver.switch_to.window(s_handle)  # 在新窗口操作
                                    except:
                                        driver.find_element_by_xpath(  "//a[@class='default_pgBtn default_pgNext']").click()
                            break
    except Exception as e:
        print('赣州2\t', e)
        driver.close()
        return ganzhou2(name)


# todo  吉安   行政服务中心 | 发改委 | 人民政府 | 住建局
def jian(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://xzfw.jian.gov.cn/news-list-zxdt.html': 1,  # 行政服务中心 中心动态
            'http://xzfw.jian.gov.cn/news-list-tupianxinwen.html': 1,  # 行政服务中心 图片新闻
            'http://xzfw.jian.gov.cn/news-list-gonggaoxinxi.html': 1,  # 行政服务中心 公告信息
            'http://fgw.jian.gov.cn/news-list-fgdt.html': 24,  # 发改委 工作动态
            'http://fgw.jian.gov.cn/news-list-ggtz.html': 4,  # 发改委 公告通知
            'http://www.jian.gov.cn/news-list-jinrijian.html': 142,  # 首页>政务>政务要闻
            'http://www.jian.gov.cn/news-list-bumendongtai.html': 36,  # 首页>政务>部门动态
            'http://www.jian.gov.cn/news-list-quxiankuaixun.html': 48,  # 首页>政务>区县快讯
            'http://www.jian.gov.cn/news-list-zhengfuwenjian.html': 7,  #首页>政务>决策公开>政府文件
            'http://zjj.jian.gov.cn/news-list-xwzx1.html': 3,  # 住建局 工作动态
            'http://zjj.jian.gov.cn/news-list-tupianxinwen.html': 2,  # 住建局 图片新闻
            'http://zjj.jian.gov.cn/news-list-tzgg.html': 7,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath="//div[@class='infodate infolist dot_02 p6_moreinfo moreinfo_list']/ul/li/a"
                ll = len(html_2.xpath(xpath)) *2
                tt=range(1, ll,2)
            elif 'www' in url:
                xpath="//ul[@class='list_list']/li/a"
                ll = len(html_2.xpath(xpath)) + 1
                tt = range(1, ll)
            else:
                xpath="//div[@class='pagingList']/ul/li/a"
                ll=len(html_2.xpath(xpath)) + 1
                tt = range(1, ll)
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in tt:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li/a',f'/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','').replace('时间：','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                except:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                        break
    except Exception as e:
        print('吉安\t', e)
        driver.close()
        return jian(name)

# todo  宜春   行政审批局 | 发改委  | 人民政府  | 住建局
def yichun(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://xzspj.yichun.gov.cn/news-list-gongzuodongtai.html': 22,  # 行政审批局 工作动态
            'http://xzspj.yichun.gov.cn/news-list-tongzhigonggao.html': 10,  # 行政审批局 通知公告
            'http://xzspj.yichun.gov.cn/news-list-zhengcefagui.html': 3,  # 行政审批局 政策法规
            'http://drc.yichun.gov.cn/news-list-gonggaogongshi.html': 2,  # 发改委 公告公示
            'http://drc.yichun.gov.cn/news-list-gongzuodongtai.html': 15,  # 发改委 工作动态
            'http://www.yichun.gov.cn/news-list-zwyw.html': 86,  # 人民政府 首页>公开>政务动态>政务要闻
            'http://www.yichun.gov.cn/news-list-xsqdt.html': 73,  # 人民政府 首页>公开>政务动态>县市区动态
            'http://www.yichun.gov.cn/news-list-bumenxinxi.html': 63,  # 人民政府 首页>公开>政务动态>部门信息
            'http://zjj.yichun.gov.cn/news-list-gongzuodongtai.html': 18,  # 住建局 工作动态
            'http://zjj.yichun.gov.cn/news-list-zhengcejiedu.html': 1,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath="//div[@id='all_list']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li/a',f'/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip()
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','').replace('时间：','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                except:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                        break
    except Exception as e:
        print('宜春\t', e)
        driver.close()
        return yichun(name)

# todo  抚州   发改委（响应慢） | 人民政府 | 住建局
def fuzhou(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://dpc.jxfz.gov.cn/col/col5809/index.html': 3,  # 发改委 工作动态
            'http://dpc.jxfz.gov.cn/col/col5810/index.html': 3,  # 发改委 通知公告
            'http://www.jxfz.gov.cn/col/col11/index.html': 3,  # 人民政府 抚州要闻
            'http://www.jxfz.gov.cn/col/col13/index.html': 3,  # 人民政府 部门动态
            'http://www.jxfz.gov.cn/col/col14/index.html': 3,  # 人民政府 区县动态
            'http://www.jxfz.gov.cn/col/col321/index.html': 3,  # 人民政府 通知公告
            'http://jsj.jxfz.gov.cn/col/col4268/index.html': 3,  # 住建局 工作动态
            'http://jsj.jxfz.gov.cn/col/col4265/index.html': 1,  # 住建局 政策法规
            'http://jsj.jxfz.gov.cn/col/col4286/index.html': 2,  # 住建局 公告公示
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath="//div[@class='bt-mod-wzpb-02']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li/a',f'/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span[@class='bt-data-time']/text()")[0].strip().replace('[','').replace(']','').replace('时间：','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                        break
    except Exception as e:
        print('抚州\t', e)
        driver.close()
        return fuzhou(name)

# todo  上饶   人民政府 |  住建局
def shangrao(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.zgsr.gov.cn/zwgk/zwzx/gsgg/index.shtml': 3,  # 人民政府 公告公示
            'http://www.zgsr.gov.cn/zwgk/zwzx/zwyw/index.shtml': 20,  # 人民政府 政务要闻
            'http://www.zgsr.gov.cn/zwgk/zwzx/bmdt/index.shtml': 20,  # 人民政府 部门动态
            'http://www.zgsr.gov.cn/zwgk/zwzx/qxdt/index.shtml': 20,  # 人民政府 区县动态
            'http://www.zgsr.gov.cn/zwgk/zwzx/tsxw/index.shtml': 5,  # 人民政府 图视新闻
            'http://www.zgsr.gov.cn/zwgk/zwzx/tbtt/index.shtml': 19,  # 人民政府 头版头条
            'http://zjj.zgsr.gov.cn/Web_Site/NewsMore.aspx?lmid=8D468D52509652E0': 19,  # 住建局 住建动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zjj' in url:
                xpath="//table[@class='t4']//li"
            else:
                xpath="//div[@class='rightLs']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li/a',f'/li[{i}]').replace('//li',f'//li[{i}]/')
                    if 'zjj' in url:
                        href = html_1.xpath(f"{xpath1}/span[2]/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span[2]/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span[1]/text()")[0].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
                            '时间：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','').replace('时间：','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.execute_script("arguments[0].click();",
                                                          driver.find_element_by_link_text('下一页'))

                                except:driver.find_element_by_xpath("//div[@class='nub channelpages']/p/input[3]").click()

                        break
    except Exception as e:
        print('上饶\t', e)
        driver.close()
        return shangrao(name)

def start():
    jiangxi1('江西')
    nanchang('南昌')
    jingdezhen('景德镇')
    pingxiang('萍乡')
    jiujiang('九江')
    jiujiang1('九江')
    xinyu('新余')
    yingtan('鹰潭')
    ganzhou1('赣州')
    ganzhou2('赣州')
    jian('吉安')
    yichun('宜春')
    shangrao('上饶')

from threading import Thread
t0 = Thread(target=jiangxi, args=("江西",))
t00 = Thread(target=ganzhou, args=("赣州",))
t10 = Thread(target=fuzhou, args=("抚州",))
t11= Thread(target=start)



def ready2():
    threadl = [
        t0,t00 ,t10,t11
    ]
    for x in threadl:
        x.start()
ready2()
# jingdezhen('景德镇')
# jiangxi('江西')
# nanchang('南昌')
#
