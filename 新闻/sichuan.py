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

# jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 7
jiezhi_time = int(time.mktime(time.strptime(now.strftime("2019-01-01"), "%Y-%m-%d")))
gjzs = ['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子', '保险']
pro = '四川'

def chuli(publictime,href,driver,url,title,city,xpath1):
    try:

        if re.findall('http', href):
            link = href
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

        elif './' in href:
            link = url + href.replace('./', '')
        elif href[0] == '/':
            if re.findall(r'http(.*?)\.cn', url):
                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
            else:
                link = 'http' + re.findall(r'http(.*?)\.com', url)[0] + '.cn' + href
        else:
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/'+href
        uid = uuid.uuid4()
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                           biaoti=title, tianjiatime=insertDBtime, zt='0')
        print(f'--{city}-【{title}】写入成功')

    except Exception as e:
        print('处理\t', e)


def chuli1(publictime,href,url,title,city):
    try:
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if re.findall('http', href):
            link = href
        elif './' in href:
            link = url + href.replace('./', '')
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
        print('处理\t', e)

# todo  四川  公共资源中心 | 发改委 |人民政府 |住建局
def sichuan(name):
    global driver
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
            'http://ggzyjy.sc.gov.cn/xwzx/001001/001001002/moreinfomenu.html': 6,  # 公共资源中心 省级新闻
            'http://ggzyjy.sc.gov.cn/xwzx/001001/001001003/moreinfomenu.html': 3,  # 公共资源中心 市级新闻
            'http://ggzyjy.sc.gov.cn/xwzx/001001/001001004/moreinfomenu.html': 3,  # 公共资源中心 工作交流
            'http://ggzyjy.sc.gov.cn/xwzx/001003/noticemore.html': 10,  # 公共资源中心 通知公告
            'http://fgw.sc.gov.cn/sfgw/gzdt/list.shtml': 35,  # 发改委 发展改革动态
            'http://fgw.sc.gov.cn/sfgw/tzgg/list.shtml': 9,  # 发改委 通知公告
            'http://fgw.sc.gov.cn/sfgw/zcwj/list.shtml': 3,  # 发改委 政策文件
            'http://fgw.sc.gov.cn/sfgw/zcjd/list.shtml': 2,  # 发改委 政策解读
            'http://fgw.sc.gov.cn/sfgw/fgyw/list.shtml': 11,  # 发改委 发改要闻
            'http://fgw.sc.gov.cn/sfgw/szdt/list.shtml': 68,  # 发改委 发改要闻
            'http://www.sc.gov.cn/10462/10464/10797/jrsc_list.shtml': 31,  # 人民政府 今日四川
            'http://www.sc.gov.cn/10462/12771/list_ft.shtml': 16,  # 人民政府 热点关注
            'http://www.sc.gov.cn/10462/10464/10465/10574/list_ft.shtml': 16,  # 人民政府 部门动态
            'http://www.sc.gov.cn/10462/10464/10465/10595/list_ft.shtml': 16,  # 人民政府 市州动态
            'http://jst.sc.gov.cn/scjst/c101451/article_list.shtml': 73,  # 住建局  要闻播报
            'http://jst.sc.gov.cn/scjst/c101448/article_list.shtml': 23,  # 住建局  住建动态
            'http://jst.sc.gov.cn/scjst/c101429/article_list.shtml': 60,  # 住建局  公示通告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath="//li[@class='pb-30 b-b-1 list-img clear mb20']/div/h1"
            elif 'www' in url:
                xpath='//*[@id="dash-table"]/tbody/tr/td[2]/span/font/a'
            elif 'jst' in url:
                xpath="//ul/li[@class='clearfix']"
            else:
                xpath = "//ul[@id='moreinfomenulist']/li/p/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i%6==0:
                        pass
                    else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('li/p/a', f'li[{i}]/p').replace(']/di', f'][{i}]/di').replace('tr/td', f'tr[{i}]/td').replace("ix']", f"ix'][{i}]")
                        if 'fgw' in url:
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')
                        elif 'www' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            cc=href.split('/')
                            if len(cc)==10:
                                publictime =cc[6] +'-'+cc[7]+'-'+cc[8]
                            elif len(cc)==8:
                                publictime =cc[4] +'-'+cc[5]+'-'+cc[6]
                            elif len(cc)>8:
                                publictime =cc[5] +'-'+cc[6] +'-'+cc[7]
                            else:
                                publictime =cc[3] + '-' + cc[4]+ '-'+ cc[5]
                        else:

                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('四川\t', e)
        driver.close()
        return sichuan(name)
# todo  攀枝花  公共资源中心 | 发改委 |住建局
def panzhihua(name):
    global driver
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

            'http://ggzy.panzhihua.gov.cn/tzgg': 4,  # 公共资源中心  通知公告
            'http://ggzy.panzhihua.gov.cn/zxdt?area=001': 10,  # 公共资源中心  工作动态
            'http://fgw.panzhihua.gov.cn/zwgk/gzdt/index.shtml': 15,  # 发改委  工作动态
            'http://fgw.panzhihua.gov.cn/zwgk/tzgg/index.shtml': 4,  # 发改委  通知公告
            'http://fgw.panzhihua.gov.cn/zwgk/rdgz/index.shtml': 21,  # 发改委  热点关注
            'http://zjj.panzhihua.gov.cn/zwgk/gzdt/index.shtml': 21,  # 住建局  工作动态
            'http://zjj.panzhihua.gov.cn/zwgk/tzgg/index.shtml': 21,  # 住建局  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath= "//table[@id='p2']/tbody/tr/td[2]"
                length = len(html_2.xpath(xpath)) + 2
                ii=2
            else:
                xpath = "//div[@class='new-box']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
                ii=1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(ii, length):
                    if 'www' in url and i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td', f'tr[{i}]/td')
                        if 'ggzy' in url:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1.replace('[2]','[3]')}/text()")[0].strip().replace('/', '-')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('攀枝花\t', e)
        driver.close()
        return panzhihua(name)
# todo   攀枝花(ij)  人民政府(响应慢)
def panzhihua1(name):
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
            'http://www.panzhihua.gov.cn/zwgk/gzdt/bdyw/index.shtml':21,  # 人民政府 工作动态
            'http://www.panzhihua.gov.cn/zwgk/gzdt/gggs/index.shtml':21,  # 人民政府 公告公示
            'http://www.panzhihua.gov.cn/zwgk/gzdt/rdgz/index.shtml':21,  # 人民政府 热点关注
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='boxPzh15_con']/ul/li"
            xpathj = "//div[@class='boxPzh15_con']/ul/li[1]"
            jj = len(html_2.xpath(xpathj)) + 1
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, 6):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul[{j}]/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
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
                                    except:
                                        driver.find_element_by_xpath(  "//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('攀枝花\t',e)
        driver.close()
        return panzhihua1(name)

# todo  泸州  公共资源中心 | 发改委 |人民政府 |住建局
def luzhou(name):
    global driver
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

            'http://zjj.luzhou.gov.cn/xwzx/zxdt': 32,  # 住建局  新闻中心>最新动态
            'http://zjj.luzhou.gov.cn/xwzx/qxzw': 8,  # 住建局  新闻中心>区县政务
            'http://www.luzhou.gov.cn/xw/jrxx': 256,  # 人民政府  今日泸州
            'http://www.luzhou.gov.cn/xw/zwyw': 91,  # 人民政府  政务要闻
            'http://www.luzhou.gov.cn/xw/qxdt': 256,  # 人民政府  区县动态
            'http://www.luzhou.gov.cn/xw/bmdt122': 140,  # 人民政府  部门动态
            'http://www.luzhou.gov.cn/xw/jjfz': 220,  # 人民政府  经济发展
            'http://www.luzhou.gov.cn/xw/bmgg': 79,  # 人民政府  通知公告
            'https://www.lzsggzy.com/tzgg/010001/list.html': 8,  # 公共资源中心  通知公告
            'https://www.lzsggzy.com/zwgk/001002/001002001/list_gz.html': 17,  # 公共资源中心  工作动态
            'http://fgw.luzhou.gov.cn/tzgg': 7,  # 发改委  通知公告
            'http://fgw.luzhou.gov.cn/gzdt': 30,  # 发改委  工作动态
            'http://fgw.luzhou.gov.cn/zwgk/zcwj/wjfb': 2,  # 发改委  文件发布
            'http://fgw.luzhou.gov.cn/zwgk/zcwj/zcjd': 2,  # 发改委  政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zjj' in url or 'fgw' in url:
                xpath= "//div[@class='mBd']/ul/li/a"
                length = len(html_2.xpath(xpath)) +1
                ii=1
            elif 'xw/bmgg' in url:
                xpath= "//ul[@class='newsList']/li"
                length = len(html_2.xpath(xpath)) + 1
                ii=1
            elif 'lzsggzy' in url:
                xpath= "//ul[@id='jingtai']/li"
                length = len(html_2.xpath(xpath)) + 2
                ii=2
            else:
                xpath = '//*[@id="content"]/div[2]/div/div[2]/ul/li'
                length = len(html_2.xpath(xpath)) + 1
                ii=1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(ii, length):
                    if ('zjj' in url or 'xw/bmgg' in url or 'fgw' in url )and i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li/a', f'ul/li[{i}]').replace(']/li', f']/li[{i}]').replace('[2]/ul/li', f'[2]/ul/li[{i}]')
                        if 'www.luzhou' in url and 'xw/bmgg' not in url:
                            href = html_1.xpath(f"{xpath1}/div[1]/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div[1]/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            try:
                                publictime = html_1.xpath(f"{xpath1}/div[3]/div[2]/span/text()")[0].strip().replace('/', '-')
                            except:
                                publictime = html_1.xpath(f"{xpath1}/div[2]/div[2]/span/text()")[0].strip().replace('/', '-')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('泸州\t', e)
        driver.close()
        return luzhou(name)

# todo  德阳  公共资源中心（响应慢） | 发改委 |人民政府 |住建局
def deyang(name):
    global driver
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

            'http://ggzyxx.deyang.gov.cn/pub/generic_list_tzgg.html': 8,  # 公共资源中心 通知公告
            'http://www.deyang.gov.cn/info/iList.jsp?cat_id=10004': 279,  # 人民政府 部门动态
            'http://www.deyang.gov.cn/info/iList.jsp?cat_id=10003': 142,  # 人民政府 德阳动态
            'http://www.deyang.gov.cn/info/iList.jsp?cat_id=10005': 182,  # 人民政府 县市区动态
            'http://dyzww.deyang.gov.cn/info/iList.jsp?cat_id=12256': 36,  # 德阳政务网 公示公告
            'http://dyzww.deyang.gov.cn/info/iList.jsp?cat_id=12258': 30,  # 德阳政务网 工作动态
            'http://zhujian.deyang.gov.cn/index.php?c=category&id=71': 8,  # 住建局 建设要闻
            'http://zhujian.deyang.gov.cn/index.php?c=category&id=72': 15,  # 住建局 工作动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url :
                xpath= "//div[@id='list_content']/ul/li"
            elif 'dyzww' in url :
                xpath= "//div[@class='div_left']/ul/li"
            elif 'zhujian' in url :
                xpath= "/html/body/div[1]/div/div[2]/div[2]/ul/li/a"
            else:
                xpath ="//div[@id='listDiv']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if ('zjj' in url )and i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                        if 'zhujian' in url :
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/div/div[2]/div[2]/text()")[0].strip().replace('/', '-').replace('[', '').replace(']', '')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            try:
                                publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-')
                            except:
                                publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('德阳\t', e)
        driver.close()
        return deyang(name)

# todo  绵阳  公共资源中心 | 发改委 |人民政府 |住建局
def mianyang(name):
    global driver
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

            'http://ggzy.my.gov.cn/xwdt/index.html': 4,  # 公共资源中心 新闻动态
            'http://ggzy.my.gov.cn/tzgg/index.html': 3,  # 公共资源中心 通知公告
            'http://www.my.gov.cn/ywdt/snyw/index.html': 56,  # 人民政府 市内要闻
            'http://www.my.gov.cn/zwyw/bmdt/index.html': 40,  # 人民政府 部门动态
            'http://fgw.my.gov.cn/gzdt/index.html': 34,  # 发改委 工作动态
            'http://fgw.my.gov.cn/zwgk/zcwjyjd/index.html': 2,  # 发改委 政策文件与解读
            'http://zjw.my.gov.cn/xwdt/gzdt/index.html': 19,  # 住建局 工作动态
            'http://zjw.my.gov.cn/xwdt/wjtz/index.html': 17,  # 住建局 文件通知
            'http://zjw.my.gov.cn/flfg/zcjd/index.html': 2,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url :
                xpath= "//div[@class='navjz clearfix']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'fgw' in url :
                xpath= "//ul[@class='doc_list list-4774691']/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'zjw' in url :
                xpath= "//div[@class='navjz clearfix']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath ="//div[@class='navjz']/ul/li"
                length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if ('www' in url or 'zjw' in url )and i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                        if 'zhujian' in url :
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/div/div[2]/div[2]/text()")[0].strip().replace('/', '-')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('绵阳\t', e)
        driver.close()
        return mianyang(name)


# todo  广元  公共资源中心 | 发改委（响应慢） |人民政府 |住建局
def guangyuan(name):
    global driver
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

            'http://www.gyggzyjy.cn/gzdt/010001/about.html': 5,  # 公共资源中心 工作动态
            'http://www.gyggzyjy.cn/gzdt/010002/about.html': 2,  # 公共资源中心 区县动态
            'http://www.gyggzyjy.cn/tzgg/about.html': 2,  # 公共资源中心 通知公告
            'http://drc.cngy.gov.cn/new/list/20190301171428737.html': 3,  # 发改委  视频聚焦
            'http://drc.cngy.gov.cn/new/list/20190117111432773.html': 3,  # 发改委  政策解读
            'http://drc.cngy.gov.cn/new/list/20190301171428627.html': 4,  # 发改委  县区工作
            'http://drc.cngy.gov.cn/new/list/20190301171428378.html': 17,  # 发改委  发改要闻
            'http://drc.cngy.gov.cn/new/list/20190301171428534.html': 7,  # 发改委  高层传递
            'http://www.cngy.gov.cn/artic/list/20160708142414442.html': 219,  # 人民政府 广元要闻
            'http://www.cngy.gov.cn/govop/list/jb/40016.html': 19,  # 人民政府 公示公告
            'http://www.cngy.gov.cn/govop/list/jb/40008.html': 22,  # 人民政府 文件解读
            'http://www.cngy.gov.cn/govop/list/department.html': 266,  # 人民政府 部门动态
            'http://jsj.cngy.gov.cn/Category_1641/Index.aspx': 14,  # 住建局 热点关注
            'http://jsj.cngy.gov.cn/Category_1642/Index.aspx': 9,  # 住建局 工作动态
            'http://jsj.cngy.gov.cn/Category_1643/Index.aspx': 15,  # 住建局 区县动态
            'http://jsj.cngy.gov.cn/Category_2137/Index.aspx': 3,  # 住建局 新闻头条
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'gyggzyjy' in url :
                xpath= "//div[@class='ewb-right']/ul/li"
            elif 'jsj' in url :
                xpath= "//div[@class='mBd']/ul/li"
            elif 'drc' in url :
                xpath= "//div[@class='box']/div[@class='id-list']/ul/li"
            elif 'cngy' in url :
                xpath= "//div[@class='id-list id-list-page']/ul/li"
            else:
                xpath ="//div[@class='navjz']/ul/li"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if ( 'zjw' in url or 'jsj' in url )and i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                        if 'gyggzyjy' in url :
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            try:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/font/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')
                        if re.findall('http', href):
                            link = href
                        elif './' in href:
                            link = url + href.replace('./', '')
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn/', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall(r'http(.*?)\.cn/', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime,
                                                   url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')

                            else:
                                po += 1
                                break
                        else:
                            Mysql.update_xw_url(url=link, biaoti=title)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('广元\t', e)
        driver.close()
        return guangyuan(name)

# todo  遂宁  公共资源中心(无响应) | 发改委 |人民政府 |住建局
def suining(name):
    global driver
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

            'http://www.suining.gov.cn/web/sn/snzx': 220,  # 人民政府 遂宁资讯
            'http://www.suining.gov.cn/web/sn/qxdt': 220,  # 人民政府 县区动态
            'http://www.suining.gov.cn/web/sn/bmdt': 42,  # 人民政府 部门动态
            'http://www.suining.gov.cn/tzgg': 19,  # 人民政府 公告公示
            'http://sfzggw.suining.gov.cn/fgdt': 17,  # 发改委 发改动态
            'http://sfzggw.suining.gov.cn/tzgg': 5,  # 发改委 通知公告
            'http://sfzggw.suining.gov.cn/zwgkall': 6,  # 发改委 政务公开
            'http://sfzggw.suining.gov.cn/fzgh': 4,  # 发改委 发展规划
            'http://sfzggw.suining.gov.cn/tbzb': 2,  # 发改委 投标招标
            'http://snjsj.suining.gov.cn/web/szjj/zxdt': 14,  # 住建局  最新动态
            'http://snjsj.suining.gov.cn/gcjs': 6,  # 住建局  工程建设
            'http://snjsj.suining.gov.cn/web/szjj/qxdt': 4,  # 住建局  区县动态
            'http://snjsj.suining.gov.cn/tzgg': 9,  # 住建局  通知公告
            'http://snjsj.suining.gov.cn/gztl': 2,  # 住建局  规范性文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'dd' in url :
                xpath= "//div[@id='_cms2_WAR_CMSportlet_main_container_id0892878415016132']/ul/li"
            elif 'jsj' in url :
                xpath= "//div[@class='mBd']/ul/li"
            elif 'cngy' in url :
                xpath= "//div[@class='id-list id-list-page']/ul/li"
            else:
                xpath ="//div[@class='portlet-body']/div/ul/li"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                        if 'gyggzyjy' in url :
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('遂宁\t', e)
        driver.close()
        return suining(name)

# todo  内江  公共资源中心| 发改委 |人民政府
def neijiang(name):
    global driver
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

            'http://ggzy.neijiang.gov.cn/zwgk/002004/moreinfo.html': 4,  # 公共资源中心 动态新闻
            'http://ggzy.neijiang.gov.cn/zwgk/002001/moreinfo.html': 2,  # 公共资源中心 中心公告
            'http://www.neijiang.gov.cn/news/list/%E6%9C%AC%E5%9C%B0%E8%A6%81%E9%97%BB': 50,  # 人民政府 本地要闻
            'http://www.neijiang.gov.cn/news/list/%E5%8C%BA%E5%8E%BF%E5%8A%A8%E6%80%81': 50,  # 人民政府 区县动态
            'http://www.neijiang.gov.cn/news/list/%E9%83%A8%E9%97%A8%E5%8A%A8%E6%80%81': 50,  # 人民政府 部门动态
            'http://www.neijiang.gov.cn/news/list?id=%E6%94%BF%E7%AD%96%E8%A7%A3%E8%AF%BB&parent=%E6%94%BF%E5%8A%A1%E5%85%AC%E5%BC%80&xs=false': 5,  # 人民政府 政策解读
            'http://fgw.neijiang.gov.cn/flist?id=%E5%8F%91%E6%94%B9%E6%96%B0%E9%97%BB': 13,  # 发改委 发改新闻
            'http://fgw.neijiang.gov.cn/flist?id=%E6%94%BF%E7%AD%96%E5%BF%AB%E8%AE%AF': 2,  # 发改委 政策快讯
            'http://fgw.neijiang.gov.cn/flist?id=%E5%85%AC%E5%91%8A%E5%85%AC%E7%A4%BA': 6,  # 发改委 公告公示
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url :
                xpath= "//div[@class='list list_1 list_2']/ul/li/h4"
            elif 'fgw' in url :
                xpath= "//div[@class='wznr1']/ul/li"
            else:
                xpath ="//div[@class='ewb-colmn-bd']/ul/li"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'fgw' in url and  i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                        if 'gyggzyjy' in url :
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            if 'ggzy' in url:
                                title = html_1.xpath(f"{xpath1}/a/text()")[1].strip().replace('\n','').replace('\t','').replace('\r','')
                            else:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-').replace('.', '-')

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
                                    if 'ggzy' in url:
                                        try:
                                            driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                        except:
                                            pass
                                    else:
                                        try:
                                            driver.find_element_by_xpath(f"//a[@class='nextLink']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('内江\t', e)
        driver.close()
        return neijiang(name)
# todo   内江(ij)   住建局
def neijiang1(name):
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

            'http://zjj.neijiang.gov.cn/list/%E5%B7%A5%E4%BD%9C%E5%8A%A8%E6%80%81': 17,  # 住建局 工作动态
            'http://zjj.neijiang.gov.cn/list/%E5%85%AC%E7%A4%BA%E5%85%AC%E5%91%8A': 29,  # 住建局 公示公告
            'http://zjj.neijiang.gov.cn/list?id=%E6%94%BF%E7%AD%96%E8%A7%A3%E8%AF%BB': 2,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='list_lbnr']/ul/li"
            xpathj = "//div[@class='list_lbnr']/ul/li[1]"
            jj = len(html_2.xpath(xpathj)) + 1
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, 6):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul[{j}]/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('.','-').replace('\t','').replace('\r','')
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
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('内江\t',e)
        driver.close()
        return neijiang1(name)


# todo  乐山  公共资源中心| 发改委 |人民政府 |住建局
def leshan(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {

            'http://www.lsggzy.com.cn/pub/TZGG/list.html?menuCode=TZGG&typeCode=TZGG': 5,  # 公共资源中心 通知公告
            'https://www.leshan.gov.cn/lsswszf/bmdt/qxdtlist.shtml': 68,  # 人民政府 部门动态
            'https://www.leshan.gov.cn/lsswszf/qxdt/qxdtlist.shtml': 68,  # 人民政府 区县动态
            'https://www.leshan.gov.cn/lsswszf/zwyw/qxdtlist.shtml': 11,  # 人民政府 区县动态
            'https://sfgw.leshan.gov.cn/fgwa/gzdt/list.shtml': 4,  # 发改委 工作动态
            'https://sfgw.leshan.gov.cn/fgwa/gsgg/list.shtml': 3,  # 发改委 公示公告
            'https://sfgw.leshan.gov.cn/fgwa/yjdt/list.shtml': 3,  # 发改委 政策文件
            'https://sfgw.leshan.gov.cn/fgwa/ghjh/list.shtml': 1,  # 发改委 发展规划和年度计划
            'https://szjj.leshan.gov.cn/szjj/bmwj/list.shtml': 31,  # 住建局 部门动态
            'https://szjj.leshan.gov.cn/szjj/gsgat/list.shtml': 8,  # 住建局 公示公告
            'https://szjj.leshan.gov.cn/szjj/zcfg/list.shtml': 3,  # 住建局  政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'lsggzy' in url :
                xpath= "//div[@id='info-content']/ul/li"
            elif 'leshan' in url :
                xpath= "//div[@class='listlist2 qxlist2']/ul/li"
            elif 'szjj' in url :
                xpath= "//div[@class='con-r']/ul/li"
            else:
                xpath ="/html/body/div/div/div[2]/div[2]/div[1]/ul/li"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('乐山\t', e)
        driver.close()
        return leshan(name)

# todo  南充  公共资源中心| 发改委 |人民政府 |住建局
def nanchong(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {

            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=070001': 5,  # 公共资源中心  综合新闻
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=070002': 1,  # 公共资源中心  中心文件
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=070003': 1,  # 公共资源中心  中心动态
            'http://www.scncggzy.com.cn/TPFront/ShowInfo/Jyxxsearch.aspx?area=&category=070004': 3,  # 公共资源中心  图片新闻
            'http://www.scncggzy.com.cn/TPFront/front_tzgg/': 3,  # 公共资源中心  通知公告
            'http://fzggw.nanchong.gov.cn/html/jryw/': 28,  # 发改委  今日要闻
            'http://fzggw.nanchong.gov.cn/html/tzgg/Index.html': 5,  # 发改委  通知公告
            'http://fzggw.nanchong.gov.cn/html/ywjj/Index.html': 11,  # 发改委  要闻聚焦
            'http://fzggw.nanchong.gov.cn/html/photos/Index.html': 11,  # 发改委  图片新闻
            'http://fzggw.nanchong.gov.cn/html/zcjd/Index.html': 9,  # 发改委  政策解读
            'http://www.nanchong.gov.cn/news/list/e6efd6e2-3d3c-4584-8ccb-d27bba4fb175.html': 222,  # 人民政府  南充要闻
            'http://www.nanchong.gov.cn/news/list/a019ba74-cbf1-4154-aa16-5b495705e436.html': 42,  # 人民政府  公示公告
            'http://www.nanchong.gov.cn/news/list/68db9d9b-788d-41b8-91b5-527b2ff93ea2.html': 27,  # 人民政府  部门动态
            'http://www.nanchong.gov.cn/news/list/b0004abe-55a6-4e35-8fe2-6bbdfeffda28.html': 53,  # 人民政府  县市区动态
            'http://zfcxjsj.nanchong.gov.cn/webcenter/webarticlelist?id=11': 21,  # 住建局  工作动态
            'http://zfcxjsj.nanchong.gov.cn/webcenter/webarticlelist?id=6': 12,  # 住建局  公示公告
            'http://zfcxjsj.nanchong.gov.cn/webcenter/webarticlelist?id=7': 11,  # 住建局  公文公报
            'http://zfcxjsj.nanchong.gov.cn/webcenter/webarticlelist?id=9': 7,  # 住建局  行业信息

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'scncggzy' in url and 'front_tzgg'  not in url :
                xpath= "//div[@class='ewb-list_bd']/ul/li"
            elif 'front_tzgg' in url :
                xpath= "//div[@id='heghtnormal']/ul/li/a"
            elif 'fzggw' in url :
                xpath= "//div[@class='gglbinfo']/ul/li"
            elif 'zfcxjsj' in url :
                xpath= "//div[@class='r_list']/ul/li"
            else:
                xpath ="//div[@class='id-list id-list-qj02']/ul/li"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')

                        if 'scncggzy' in url and 'front_tzgg'  not in url :
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace(
                                '/', '-').replace('.', '-')
                        elif 'front_tzgg'  in url :
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/span[@class='list-con']/text()")[0].strip().replace('\n','').replace(
                                '\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/a/span[@class='time']/text()")[0].strip().replace('[','').replace(
                                ']', '').replace('/', '-').replace('.', '-')
                        elif 'zfcxjsj' in url:
                            href = html_1.xpath(f"{xpath1}/span[1]/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/span[1]/a/text()")[0].strip().replace('\n', '').replace(
                                '\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span[2]/text()")[0].strip().replace('[', '').replace(
                                ']', '').replace('/', '-').replace('.', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            try:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                        except:

                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('南充\t', e)
        driver.close()
        return nanchong(name)

# todo  眉山  公共资源中心| 发改委（无） |人民政府 |住建局（无）
def meishan(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.msggzy.org.cn/front/zxdt/': 3,  # 公共资源中心  中心动态
            'http://www.msggzy.org.cn/front/tzgg/': 3,  # 公共资源中心  通知公告
            'http://www.ms.gov.cn/zwyw/msyw.htm': 11,  # 人民政府  眉山要闻
            'http://www.ms.gov.cn/zfxxgk/fdzdgknr/gzdt.htm': 11,  # 人民政府  工作动态
            'http://www.ms.gov.cn/zfxxgk/fdzdgknr/gsgg.htm': 21,  # 人民政府  公示公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'msggzy' in url :
                xpath= "//div[@class='ewb-comp-bd']/div[1]/table/tbody/tr/td[1]"
            elif 'zfxxgk' in url:
                xpath = "//div[@class='govnewslista245277']/table/tbody/tr/td[1]"
            elif 'ms' in url :
                xpath= "//div[@class='list-con']/ul/li"
            else:
                xpath =""
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'fgw' in url and  i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[1]', f"tr[{i}]/td[1]").replace('ul/li', f"ul/li[@id='line_u13_{i - 1}']")
                        if 'msggzy' in url or 'zfxxgk' in url :
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            try:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            publictime = html_1.xpath(xpath1.replace('td[1]','td[2]')+f"/text()")[0].replace('\n', '').replace('\t', '').replace(
                                '\r', '').strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()

                                    except:
                                        try:
                                            driver.find_element_by_xpath(f'//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                        except:

                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('眉山\t', e)
        driver.close()
        return meishan(name)

# todo  宜宾  公共资源中心| 发改委
def yibin(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'https://ggzy.yibin.gov.cn/Jyweb/XinXiGongKaiList.aspx?type=%e4%bf%a1%e6%81%af%e5%af%bc%e8%88%aa&subtype=60': 11,  # 公共资源中心  工作动态
            'https://ggzy.yibin.gov.cn/Jyweb/XinXiGongKaiList.aspx?Type=%e4%bf%a1%e6%81%af%e5%af%bc%e8%88%aa&SubType=70&SubType2=70010': 9,  # 公共资源中心 通知公告 --> 网站公告
            'https://ggzy.yibin.gov.cn/Jyweb/XinXiGongKaiList.aspx?Type=%e4%bf%a1%e6%81%af%e5%af%bc%e8%88%aa&SubType=70&SubType2=70020': 1,  # 公共资源中心 通知公告 --> 漂浮信息
            'https://ggzy.yibin.gov.cn/Jyweb/XinXiGongKaiList.aspx?Type=%e4%bf%a1%e6%81%af%e5%af%bc%e8%88%aa&SubType=30&SubType2=30020': 1,  # 公共资源中心 政策法规 --> 政策文件
            'http://fg.yibin.gov.cn/zxgzdt/': 3,  # 发改委 最新工作动态
            'http://fg.yibin.gov.cn/fzjs/zcwj/': 4,  # 发改委 政策文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            time.sleep(12)
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url :
                xpath= '//*[@id="ctl00_Content_GridView1"]/tbody/tr/td[2]/a'
                length = len(html_2.xpath(xpath)) + 2
                ii=2
            else:
                xpath ="//table[3]/tbody/tr/td[1]/a"
                length = len(html_2.xpath(xpath)) + 1
                ii = 1
            po = 0
            for page in range(1, pages+1):
                time.sleep(8)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(ii, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f"tr[{i}]/td[")
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        try:
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        except:
                            title = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        if 'ggzy' in url:
                            publictime = html_1.xpath(f"{xpath1.replace('[2]/a','[3]')}/text()")[0].replace('\n', '').replace('\t', '').replace('\r', '').strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')
                        else:
                            publictime = html_1.xpath(f"{xpath1.replace('[1]/a','[2]/span')}/text()")[0].replace('\n', '').replace('\t', '').replace('\r', '').strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('宜宾\t', e)
        driver.close()
        return yibin(name)
# todo   宜宾(ij)   人民政府 | 住建局
def yibin1(name):
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
            'http://www.yibin.gov.cn/xxgk/jryb/': 5,  # 人民政府 今日宜宾
            'http://www.yibin.gov.cn/xxgk/qxbm/qxdt/': 5,  # 人民政府 区县动态
            'http://www.yibin.gov.cn/xxgk/qxbm/bmdt/': 5,  # 人民政府  部门动态
            'http://www.yibin.gov.cn/xxgk/rdgz/': 5,  # 人民政府  热点关注
            'http://jsj.yibin.gov.cn/gzdt_4318/': 5,  # 住建局  工作动态
            'http://jsj.yibin.gov.cn/tzgg/': 5,  # 住建局  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'jsj' in url:
                xpath = "//div[@class='gl-content']/ul/li"
            else:
                xpath = "//div[@class='gl-list rt']/ul/li"
            xpathj = f"{xpath}[1]"
            jj = len(html_2.xpath(xpathj)) + 1
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, 6):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul[{j}]/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('.','').replace('\t','').replace('\r','')
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
                                    except:
                                        driver.find_element_by_xpath(  "//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('宜宾\t',e)
        driver.close()
        return yibin1(name)

# todo  达州  公共资源中心| 发改委 |人民政府 |住建局
def dazhou(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {

            'http://www.dzggzy.cn/dzsggzy/gzdt/': 6,  # 公共资源中心  工作动态
            'http://www.dzggzy.cn/dzsggzy/wjtz/': 3,  # 公共资源中心  文件通知
            'http://www.dzggzy.cn/dzsggzy/zcfg/019001/': 1,  # 公共资源中心  政策法规 > 工程建设
            'http://fgw.dazhou.gov.cn/index.php?m=content&c=index&a=lists&catid=32': 4,  # 发改委  发改要闻
            'http://www.dazhou.gov.cn/articlist_20150716231227389_1.html': 15,  # 人民政府  今日达州
            'http://www.dazhou.gov.cn/articlist_20150716235707701_1.html': 7,  # 人民政府  达州新成就
            'http://www.dazhou.gov.cn/systemgovop/openlist_0_20150716232811147_0_0_0_0_1.html': 23,  # 人民政府  通知公告
            'http://www.dazhou.gov.cn/systemgovop/openlist_0_20150716233314319_0_0_0_0_1.html': 9,  # 人民政府  政策文件及解读
            'http://www.dazhou.gov.cn/articlist_20150716231259034_1.html': 10,  # 人民政府  部门动态
            'http://www.dazhou.gov.cn/articlist_20150716231305838_1.html': 10,  # 人民政府   区县动态
            'http://zjj.dazhou.gov.cn/Article/ShowClass.asp?ClassID=33': 13,  # 住建局   建设要闻
            'http://zjj.dazhou.gov.cn/Article/ShowClass.asp?ClassID=9': 22,  # 住建局   公示公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'dzggzy' in url:
                xpath= "//table/tbody/tr[@class='trfont']/td[2]/a"
            elif 'systemgovop' in url:
                xpath= "//div[2]/table/tbody/tr/td[1]/a"
            elif 'fgw' in url:
                xpath= "//div[@class='all_zhengwen']/ul/li"
            elif 'zjj' in url:
                xpath= '//*[@id="table21"]/tbody/tr/td/span/table/tbody/tr/td[2]/a'
            else:
                xpath ="//div[@class='ArticListLinkDiv']"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'systemgovop' in url and i==1:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]').replace("t']/td", f"t'][{i}]/td").replace("v']", f"v'][{i}]")

                        if 'dzggzy' in url or 'systemgovop' in url or 'zjj' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            if 'dzggzy' in url:
                                publictime = html_1.xpath(f"{xpath1.replace('[2]/a','[3]')}/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')
                            elif 'systemgovop' in url:
                                publictime = html_1.xpath(f"{xpath1.replace('[1]/a','[3]')}/text()")[0].strip().replace('年', '-').replace('月', '-').replace('日', '').replace('.', '-')
                            else:
                                publi = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('/', '-').replace('\n', '').replace('\t', '').replace('\r', '')
                                publictime=re.findall('更新时间：(.*) ',publi)[0]
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            try:
                                publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')
                            except:
                                publictime = html_1.xpath(f"{xpath1}/font/text()")[0].strip().replace('(', '').replace(')', '').replace('/', '-').replace('.', '-')

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
                                    if 'dzggzy' in url:
                                        driver.find_element_by_xpath('//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('达州\t', e)
        driver.close()
        return dazhou(name)

# todo  雅安  公共资源中心| 发改委 |人民政府 |住建局
def yaan(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {

            'http://www.yaggzy.org.cn/tzgg': 3,  # 公共资源中心  通知公告
            'http://www.yaggzy.org.cn/zxdt?area=001': 3,  # 公共资源中心  工作动态
            'http://www.yaan.gov.cn/xinwen/list/3D398D21-A382-4687-BD79-DA201B366232.html': 100,  # 人民政府  最新要闻
            'http://fgw.yaan.gov.cn/xinwen/list/1bb8e66d-4aa8-4b80-ab79-8bb0b3a25e56.html': 19,  # 发改委  新闻资讯
            'http://fgw.yaan.gov.cn/xinwen/list/b9d1ecfe-4b4e-4c27-a7c8-2dedd82d2d5b.html': 19,  # 发改委  通知公告
            'http://fgw.yaan.gov.cn/xinwen/list/94b4e404-a6aa-4a46-ab61-dd1287ce579c.html': 2,  # 发改委  招标投标
            'http://zfhcxjsj.yaan.gov.cn/xinwen/list/ea77b7fd-56cc-4887-b721-a11e0a4864eb.html': 20,  # 住建局  工作动态
            'http://zfhcxjsj.yaan.gov.cn/xinwen/list/22adb82a-de0d-4e42-9610-ece93531ce7f.html': 1,  # 住建局  政策法规
            'http://zfhcxjsj.yaan.gov.cn/xinwen/list/d4a3713c-8577-4e69-ab17-eca30abc5d9b.html': 15,  # 住建局  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'yaggzy' in url:
                xpath= "//table[@id='p2']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath)) + 2
            elif 'fgw' in url:
                xpath= "//div[@class='id-list id-list-li03']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'zfhcxjsj' in url:
                xpath= "//div[@class='id-list02']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            else:
                xpath ="//div[@class='list01']/ul/li"
                length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]')

                        if 'yaggzy' in url and i==1:
                            pass
                        else:
                            if 'yaggzy' in url:
                                href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                                title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                                publictime = html_1.xpath(f"{xpath1.replace('[2]/a','[3]')}/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

                            else:
                                href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                                publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                        if 'dzggzy' in url:
                                            driver.find_element_by_xpath('//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                        else:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('雅安\t', e)
        driver.close()
        return yaan(name)

# todo  巴中  公共资源中心| 发改委 |人民政府 |住建局
def bazhong(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://zwhjy.cnbz.gov.cn/xwdt/zxdt/index.html': 44,  # 公共资源中心  工作动态
            'http://zwhjy.cnbz.gov.cn/xwdt/tzgg/index.html': 4,  # 公共资源中心  通知公告
            'http://zwhjy.cnbz.gov.cn/xxgk/zcjd/index.html': 1,  # 公共资源中心  政策解读
            'http://www.cnbz.gov.cn/xxgk/bzyw/index.html': 234,  # 人民政府  巴中要闻
            'http://www.cnbz.gov.cn/xxgk/gzdt/index.html': 234,  # 人民政府  工作动态
            'http://www.cnbz.gov.cn/xxgk/gsgg/index.html': 236,  # 人民政府  公示公告
            'http://www.cnbz.gov.cn/xxgk/zcwj1/szfwj/index.html': 1,  # 人民政府  市政府文件
            'http://www.cnbz.gov.cn/xxgk/zcwj1/szfbwj/index.html': 3,  # 人民政府  市政府办文件
            'http://fzggw.cnbz.gov.cn/xwdt/gzdt/index.html': 13,  # 发改委  工作动态
            'http://fzggw.cnbz.gov.cn/xwdt/tzgg/index.html': 4,  # 发改委  通知公告
            'http://fzggw.cnbz.gov.cn/xxgk/zcfg/index.html': 3,  # 发改委  政策文件
            'http://zfcxjsj.cnbz.gov.cn/xwdt/bjdt/index.html': 6,  # 住建局  本局动态
            'http://zfcxjsj.cnbz.gov.cn/xwdt/tzgg/index.html': 12,  # 住建局  通知公告
            'http://zfcxjsj.cnbz.gov.cn/xxgk/zcfg/zcjd/index.html': 1,  # 住建局  政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)

            xpath ="//div[@class='listnews']/ul/li"
            length = len(html_2.xpath(xpath))

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                    if 'dzggzy' in url:
                                        driver.find_element_by_xpath('//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('巴中\t', e)
        driver.close()
        return bazhong(name)

# todo  广安  公共资源中心| 发改委 |人民政府 |住建局
def guangan(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzy.guang-an.gov.cn/gasggzyjyw/tzgg/list.shtml': 9,  # 公共资源中心  交易时讯
            'http://ggzy.guang-an.gov.cn/gasggzyjyw/c103136/list.shtml': 1,  # 公共资源中心  政策法规>工程建设
            'http://ggzy.guang-an.gov.cn/gasggzyjyw/c103144/list.shtml': 6,  # 公共资源中心 工作动态>本市级
            'http://ggzy.guang-an.gov.cn/gasggzyjyw/c103145/list.shtml': 4,  # 公共资源中心 工作动态>广安区
            'http://ggzy.guang-an.gov.cn/gasggzyjyw/c103146/list.shtml': 7,  # 公共资源中心 工作动态>前锋区
            'http://ggzy.guang-an.gov.cn/gasggzyjyw/c103148/list.shtml': 3,  # 公共资源中心 工作动态>岳池县
            'http://www.guang-an.gov.cn/gasrmzfw/gayw/list.shtml': 123,  # 人民政府 广安要闻
            'http://www.guang-an.gov.cn/gasrmzfw/qsxdt/list.shtml': 77,  # 人民政府 区市县动态
            'http://www.guang-an.gov.cn/gasrmzfw/bmdt/list.shtml': 24,  # 人民政府 部门动态
            'http://www.guang-an.gov.cn/gasrmzfw/yqdt/list.shtml': 20,  # 人民政府 园区动态
            'http://www.guang-an.gov.cn/gasrmzfw/tzgg/list.shtml': 15,  # 人民政府 公示公告
            'http://www.guang-an.gov.cn/gasrmzfw/rdgz/rdgz_list.shtml': 126,  # 人民政府 热点关注
            'http://www.guang-an.gov.cn/gasrmzfw/wjjd/listsadssadsad.shtml': 11,  # 人民政府 文件解读
            'http://fgw.guang-an.gov.cn/gasfzggwth/gzdt/list.shtml': 14,  # 发改委 发展改革动态
            'http://fgw.guang-an.gov.cn/gasfzggwth/qsxdt/list.shtml': 5,  # 发改委 区市县动态
            'http://fgw.guang-an.gov.cn/gasfzggwth/tzgg/list.shtml': 5,  # 发改委 通知公告
            'http://fgw.guang-an.gov.cn/gasfzggwth/zcwj/list.shtml': 6,  # 发改委 政策文件
            'http://zfjsj.guang-an.gov.cn/gazj/zwdt/list.shtml': 7,  # 住建局 政务动态
            'http://zfjsj.guang-an.gov.cn/gazj/gsgg/list.shtml': 11,  # 住建局 公示公告
            'http://zfjsj.guang-an.gov.cn/gazj/qxdt/list.shtml': 1,  # 住建局 公示公告
            'http://zfjsj.guang-an.gov.cn/gazj/zcwj/list.shtml': 2,  # 住建局 政策文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url or 'zfjsj' in url:
                xpath ="//div[@class='list_right']/ul/li"
            else:
                xpath ="//div[@class='content']/ul/li"
            length = len(html_2.xpath(xpath))+1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'www' in url:
                            publictime = html_1.xpath(f"{xpath1}/span[@class='fr']/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                    if 'dzggzy' in url:
                                        driver.find_element_by_xpath('//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('广安\t', e)
        driver.close()
        return guangan(name)


# todo  资阳  公共资源中心| 发改委 |人民政府 |住建局
def ziyang(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjyzx.ziyang.gov.cn/tzgg?city=': 5,  # 公共资源中心  通知公告
            'http://ggzyjyzx.ziyang.gov.cn/zxdt?city=': 3,  # 公共资源中心  工作动态
            'http://www.ziyang.gov.cn/_ziyang/column.aspx?id=80': 189,  # 人民政府  资阳要闻
            'http://www.ziyang.gov.cn/_ziyang/column.aspx?id=137': 52,  # 人民政府  区县动态
            'http://www.ziyang.gov.cn/_ziyang/column.aspx?id=71': 17,  # 人民政府  热点追踪
            'http://www.ziyang.gov.cn/_ziyang/column.aspx?id=142': 56,  # 人民政府  部门动态
            'http://www.ziyang.gov.cn/_ziyang/column.aspx?id=92': 26,  # 人民政府  公示公告
            'http://sfgw.ziyang.gov.cn/catalog_list.aspx?id=1': 26,  # 发改委  	公告
            'http://sfgw.ziyang.gov.cn/catalog_list.aspx?id=6': 13,  # 发改委  	工作动态
            'http://sjsj.ziyang.gov.cn/article/article.php?id=15': 3,  # 住建局 通知公告
            'http://sjsj.ziyang.gov.cn/article/article.php?id=14': 6,  # 住建局 新闻中心
            'http://sjsj.ziyang.gov.cn/article/article.php?id=11': 1,  # 住建局 新闻中心
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjyzx' in url:
                xpath ="//div[@class='contentSe']/table/tbody/tr/td[2]/a"
            elif 'sjsj' in url:
                xpath ="//div[@class='newslist']/ul/li"
            elif 'sfgw' in url:
                xpath ="//tbody/tr/td[@class='xia2'][2]/a"
            else:
                xpath ="//div[@class='column_list_box_full']/ul/li"
            length = len(html_2.xpath(xpath))+1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if i%6==0 or ('ggzyjyzx' in url and i==1):
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                        if 'ggzyjyzx' in url or 'sfgw' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            publictime = html_1.xpath(f"{xpath1.replace('[2]/a', '[3]')}//text()")[0].replace('\n', '').replace(
                                    '\t', '').replace('\r', '').strip().replace('[', '').replace(']', '').replace('/',  '-').replace( '.', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime.replace(' ',''), "%Y-%m-%d")))
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
                                    if 'dzggzy' in url:
                                        driver.find_element_by_xpath('//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('资阳\t', e)
        driver.close()
        return ziyang(name)


# todo  甘孜藏族自治州  公共资源中心
def ganzi(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        url='http://www.scgzzg.com/pub/showMcontent'
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'Cookie': '_gscu_1973744593=915846036b58en72; UM_distinctid=17291d5bfad3b1-0c3b2b46c4aa73-f7d1d38-13c680-17291d5bfae7ac; JSESSIONID=E565C7C0563068F5EB322519CDE0E096; _gscbrs_1973744593=1; CNZZDATA1273436361=1017049967-1591584604-null%7C1594369884; _gscs_1973744593=94369882s7b8t711|pv:5',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '63',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'www.scgzzg.com',
            'Origin': 'http://www.scgzzg.com',
            'Referer': 'http://www.scgzzg.com/pub/categorys_gzdt.html',
            'X-Requested-With': 'XMLHttpRequest'
        }

        xpaths = {
            "GZDTZHXX": 4,  # 综合信息
            "GZDTZXDT": 2,  # 中心动态
            "GZDTGGTZ": 3,  # 公告通知
        }
        for xpath1, pages in zip(xpaths.keys(), xpaths.values()):
            data = {
                'mcode': f'{xpath1}_DEFAULT',
                'clicktype': '1',
                'pageNum': '1',
                'keyname': '',
                'areacode': '',
            }
            for page in range(1,pages+1):
                con=requests.post(url,headers=headers,data=data).content.decode('utf-8')
                conts=json.loads(con)['data']['content']
                for cont in conts:
                    id=cont['id']
                    title=cont['mctype']
                    publictime=cont['mckeys']
                    href=f'http://www.scgzzg.com/pub/indexContent_{id}.html'

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
                                chuli1(publictime, href, url, title, city)


    except Exception as e:
        print('甘孜藏族自治州\t', e)
        return ganzi(name)

# todo  甘孜藏族自治州  发改委 |人民政府 |住建局
def ganzi1(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjyzx.ziyang.gov.cn/tzgg?city=': 50,  # 人民政府  甘孜要闻
            'http://www.gzz.gov.cn/gzzrmzf/c100044/list.shtml': 50,  # 人民政府  部门动态
            'http://www.gzz.gov.cn/gzzrmzf/c100045/list.shtml': 50,  # 人民政府  市县动态
            'http://www.gzz.gov.cn/gzzrmzf/c100046/list.shtml': 8,  # 人民政府  通知公告
            'http://www.gzz.gov.cn/gzzrmzf/c100031/list.shtml': 7,  # 人民政府  政策解读
            'http://fgw.gzz.gov.cn/gzzfgw/c100334/common_list.shtml': 17,  # 发改委  工作动态
            'http://fgw.gzz.gov.cn/gzzfgw/c100352/common_list.shtml': 3,  # 发改委  部门文件
            'http://jsj.gzz.gov.cn/gzzjsj/c100334/common_list.shtml': 2,  # 住建局  新闻动态
            'http://jsj.gzz.gov.cn/gzzjsj/c100353/common_list.shtml': 2,  # 住建局  公示公告
            'http://jsj.gzz.gov.cn/gzzjsj/c100355/common_list.shtml': 1,  # 住建局  文件通知
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//div[@class='list_container']/ul/li"
            else:
                xpath ="//div[@class='comm_list']/ul/li"
            length = len(html_2.xpath(xpath))+1

            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                        if 'ggzyjyzx' in url or 'sfgw' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            publictime = html_1.xpath(f"{xpath1.replace('[2]/a', '[3]')}/text()")[0].replace('\n', '').replace(
                                    '\t', '').replace('\r', '').strip().replace('[', '').replace(']', '').replace('/',  '-').replace( '.', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('.', '-')

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
                                    if 'dzggzy' in url:
                                        driver.find_element_by_xpath('//*[@id="Paging"]/div/div/table/tbody/tr/td[15]').click()
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('甘孜藏族自治州\t', e)
        driver.close()
        return ganzi1(name)



# todo  成都  公共资源中心 | 发改委  |人民政府(有问题)
def chengdu(name):
    global driver
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
            'https://www.cdggzy.com/site/Plus/NoticeList.aspx?cid=0002000100400010001': 6,  # 公共资源中心 通知公告
            'https://www.cdggzy.com/site/OpenGovernment/List.aspx?cid=0001000100020001': 13,  # 公共资源中心 工作动态
            'http://www.chengdu.gov.cn/chengdu/home/xw.shtml': 13, # 人民政府 新闻(有问题)
            'http://www.chengdu.gov.cn/es-search/search/45de5c5a85d04f9e831ea731c8193c37?_channelName=%E6%8E%A8%E8%8D%90&_isAgg=0&_pageSize=20&_template=chengdu_list': 40,
            'http://cddrc.chengdu.gov.cn/cdfgw/fzggdt/fzggdt_list.shtml':73,
            'http://cddrc.chengdu.gov.cn/cdfgw/c120592/jksj_list_1.shtml?classId=070305030103':3,
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'cddrc' in url:
                xpath="//ul/li/a/span[@class='text']"
            elif 'www.cdgg' in url:
                xpath="//tr[2]/td/table[@id='Result']/tbody/tr/td/a"
            elif 'www.chengd' in url:
                xpath="//ul[@class='list']/li"
            else:
                xpath = "//ul[@id='moreinfomenulist']/li/p/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i%6==0:
                        pass
                    else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('li/p/a', f'li[{i}]/p').replace('li/a', f'[{i}]/a').replace('tr/td', f'tr[{i}]/td').replace("ix']", f"ix'][{i}]")
                        if 'fgw' in url:
                            href = html_1.xpath(f'//*[@id="more_right"]/div/div[2]/div/ul/li[{i}]/a/@href')[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace('·', '')
                            publictime = html_1.xpath(f"{xpath1.replace('text','date')}/text()")[0].strip().replace('/', '-')

                        elif 'www.cdgg' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/p/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1.replace('/a','')}[@class='date']/text()")[0].strip().replace('/', '-')
                        else:

                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

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
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('成都\t', e)
        driver.close()
        return chengdu(name)
# todo  成都  公共资源中心 | 发改委  |人民政府
def chengdu1(name):
    global driver
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
            'http://www.chengdu.gov.cn/es-search/search/17b0921ed7834c66aa970471b5f6315f?_channelName=%E6%96%B0%E9%97%BB&_isAgg=0&_pageSize=20&_template=chengdu_list': 13,
            # 人民政府 新闻
            'http://www.chengdu.gov.cn/es-search/search/45de5c5a85d04f9e831ea731c8193c37?_channelName=%E6%8E%A8%E8%8D%90&_isAgg=0&_pageSize=20&_template=chengdu_list': 40, # 人民政府 推荐
            'http://cddrc.chengdu.gov.cn/cdfgw/c120592/jksj_list_1.shtml?classId=070305030103&pageNum=2': 40, # 人民政府 推荐
            'http://cddrc.chengdu.gov.cn/cdfgw/c112449/list_1.shtml': 40, # 人民政府 推荐

        }
        for url1, pages in zip(urls.keys(), urls.values()):
            from urllib import parse

            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',

            }

            # driver.get(url)
            # con = driver.page_source
            # html_2 = etree.HTML(con)
            # if 'fgw' in url:
            #     xpath="//li[@class='pb-30 b-b-1 list-img clear mb20']/div/h1"
            # elif 'www.cdgg' in url:
            #     xpath="//tr[2]/td/table[@id='Result']/tbody/tr/td/a"
            # elif 'www.chengd' in url:
            #     xpath="//ul[@class='list']/li"
            # else:
            #     xpath = "//ul[@id='moreinfomenulist']/li/p/a"
            # length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):

                if 'cddrc' in url1:
                    url = f'http://api.chengdu.gov.cn/govInfoPub/infoList.action?classId{re.findall("classId(.*)", url1)[0]}&pageSize=20&result=json&x-msc-token=xEFvsIO1mO3DXOtZsqLLSGIAcwn4Ug9t'
                    data = {
                        'classId': f'{re.findall("classId=(.*)&pageNum", url1)[0]}',
                        'pageNum': f'{page}',
                        'pageSize': '20',
                        'result': 'json',
                        'x - msc - token': 'xEFvsIO1mO3DXOtZsqLLSGIAcwn4Ug9t'
                    }
                else:
                    url = url1
                    data = {
                        '_channelName': f'{parse.unquote(re.findall("channelName=(.*?)&_isAg", url1)[0])}',
                        '_isAgg': '0',
                        '_pageSize': '20',
                        '_template': 'chengdu_list'
                    }
                conn = requests.get(url, headers=headers, data=data).content.decode('utf-8')
                cons=json.loads(conn)['datalist']
                for con in cons:
                    id=con['id']
                    title=con['name']
                    publictime=con['time']
                    href=f'http://cddrc.chengdu.gov.cn/cdfgw/c120593/jksj_nry.shtml?id={id}&tn=2'
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli1(publictime, href, url, title, city)
                        else:
                            po += 1
                            break

    except Exception as e:
        print('成都\t', e)
        driver.close()
        return chengdu1(name)# todo  成都  公共资源中心 | 发改委  |人民政府
def chengdu2(name):
    global driver
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
            'http://cddrc.chengdu.gov.cn/es-search/search/25a2a967cc7c4547931386405212fc74?_template=zhaofa/fgw_list&_isAgg=1&_pageSize=20&page=1': 40, # 发改委 推荐

        }
        for url1, pages in zip(urls.keys(), urls.values()):
            from urllib import parse

            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',

            }
            po = 0
            for page in range(1, pages+1):
                data = {
                    '_template': 'zhaofa / fgw_list',
                    '_isAgg': '1',
                    '_pageSize': '20',
                    'page': f'{page}'
                }

                conn = requests.get(url1, headers=headers, params=data).content.decode('utf-8')
                cons=json.loads(conn)['datalist']
                for con in cons:
                    id=con['id']
                    title=con['name']
                    publictime=con['time']
                    href=f'http://cddrc.chengdu.gov.cn/cdfgw/c120593/jksj_nry.shtml?id={id}&tn=2'
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli1(publictime, href, href, title, city)
                        else:
                            po += 1
                            break

    except Exception as e:
        print('成都\t', e)
        driver.close()
        return chengdu2(name)



def start():
    # sichuan('四川')
    # panzhihua('攀枝花')
    # panzhihua1('攀枝花')
    # luzhou('泸州')
    # deyang('德阳')
    # mianyang('绵阳')
    # guangyuan('广元')
    # suining('遂宁')
    # neijiang('内江')
    # neijiang1('内江')
    # leshan('乐山')
    # meishan('眉山')

    yibin('宜宾')
    yibin1('宜宾')
    dazhou('达州')
    yaan('雅安')
    bazhong('巴中')
    guangan('广安')
    ziyang('资阳')
    ganzi('甘孜藏族自治州')
    ganzi1('甘孜藏族自治州')

start()

# meishan('眉山')
# chengdu1('成都')
