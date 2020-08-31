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
pro = '海南'


def chuli(publictime, href, driver, url, title, city, xpath1):
    try:
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
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
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
        else:
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/' + href
        uid = uuid.uuid4()
        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                           biaoti=title, tianjiatime=insertDBtime, zt='0')

        print(f'--{city}-【{title}】写入成功')

    except Exception as e:
        print('处理\t', e)
def chuli1(publictime, href, url, title, city):
    try:
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if re.findall('http', href):
            link = href
        elif './' in href:
            link = url + href.replace('./', '')
        elif href[0] == '/':
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
        else:
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/' + href
        uid = uuid.uuid4()
        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                           biaoti=title, tianjiatime=insertDBtime, zt='0')
        print(f'--{city}-【{title}】写入成功')

    except Exception as e:
        print('处理\t', e)


# todo  海南  公共资源中心
def hainan(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,
                                  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://zw.hainan.gov.cn/ggzy/ggzy/tzgg/index.jhtml': 3,  # 公共资源中心 通知公告
            'http://zw.hainan.gov.cn/ggzy/ggzy/xwdt/index.jhtml': 1,  # 公共资源中心 新闻动态
            'https://www.hainan.gov.cn/hainan/0101/list3_1.shtml': 16,  # 人民政府 公示公告
            'https://www.hainan.gov.cn/common/search/2f11247a5c2c49eeb3cdbb00a8178bc7?_isAgg=false&_pageSize=12&_template=hainan&_channelName=&page=1': 314,  # 人民政府 政务动态
            'https://www.hainan.gov.cn/common/search/55acf8539596d25624059980986aaa78?_isAgg=false&_pageSize=12&_template=hainan&_channelName=&page=1': 326,  # 人民政府 今日海南
            'https://www.hainan.gov.cn/common/search/82cdb5b25e514a1bba6429aef621ce6c?_isAgg=false&_pageSize=12&_template=hainan&sort=publishedTime&_channelName=&page=1': 189,  # 人民政府 省府要闻
            'https://www.hainan.gov.cn/hainan/zxjd/list3.shtml': 2,  # 人民政府 政策解读>最新解读
            'http://plan.hainan.gov.cn/sfgw/zwdt/list3.shtml': 5,  # 发改委  要闻动态 > 政务动态
            'http://plan.hainan.gov.cn/sfgw/gzdt/list3.shtml': 20,  # 发改委  工作动态
            'http://plan.hainan.gov.cn/sfgw/zxdt/list3.shtml': 50,  # 发改委  最新动态
            'http://zjt.hainan.gov.cn/szjt/zwdt/tablist.shtml': 36,  # 住建局  政务动态
            'http://zjt.hainan.gov.cn/szjt/sxxx/iframelist_sx.shtml': 15,  # 住建局  市县信息


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zw' in url:
                xpath = "//table[@class='newtable']/tbody/tr/td[2]/a"
            elif 'plan' in url:
                xpath = "//div[@class='Fivelist']/ul/li"
            elif 'zjt' in url:
                xpath = "//div[@class='con-right']/div/div/a"
            else:
                xpath = "//div[@class='cen-div-1 mar-t']/div/div/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'plan' in url and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/div/div/div/a', f'/div/div[{i}]/div/a').replace('tr/td[', f'tr[{i}]/td[')
                    if 'zw' in url or 'www' in url or 'zjt' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        if 'zw' in url:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('div/a', "table/tbody/tr/td") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：                    ', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace(
                            '日', '').replace('/', '-')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

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
                                chuli(publictime, href, driver, url, title, city, xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('海南\t', e)
        driver.close()
        return hainan(name)

# todo  海口  公共资源中心
def haikou(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,
                                  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzy.haikou.gov.cn/ywdt/zwdt/02/2_201603-002_1.html': 3,  # 公共资源中心 政务动态
            'http://ggzy.haikou.gov.cn/xxgk/gsgg/02/3_201603-005_1.html': 2,  # 公共资源中心 公示公告
            'http://ggzy.haikou.gov.cn/xxgk/zcwj/02/3_201603-010_1.html': 1,  # 公共资源中心 政策文件
            'http://ggzy.haikou.gov.cn/jdhy/zxjd/02/4_201603-045_1.html': 1,  # 公共资源中心 最新解读
            'http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcfg/szfxzgfxwj/': 3,  # 人民政府 市政府行政规范性文件
            'http://www.haikou.gov.cn/xxgk/szfbjxxgk/zcfg/bmxzgfxwj/': 1,  # 人民政府 部门行政规范性文件
            'http://www.haikou.gov.cn/zfdt/xbzwdt/gqrd/': 36,  # 人民政府 市 政务动态 >> 各区动态
            'http://www.haikou.gov.cn/zfdt/xbzwdt/bmdt/': 22,  # 人民政府 市 政务动态 >> 部门动态
            'http://www.haikou.gov.cn/xxgk/szfbjxxgk/ggtz/': 19,  # 人民政府  公示公告
            'http://www.haikou.gov.cn/tzhk/zcjy/': 1,  # 人民政府  政策机遇
            'http://drc.haikou.gov.cn/ywdt/gzdt/': 11,  # 发改委  工作动态
            'http://drc.haikou.gov.cn/xxxgk/gsgg/': 2,  # 发改委  公示公告
            'http://hkjsj.haikou.gov.cn/xxgk1/gsgg/': 5,  # 住建局  公示公告
            'http://hkjsj.haikou.gov.cn/xxgk1/zcwj/bmwj/': 1,  # 住建局 部门文件
            'http://hkjsj.haikou.gov.cn/jdhy/zxjd/': 1,  # 住建局 最新解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@id='list_div']/div/div/a"

            elif 'drc' in url:
                xpath = "//div[@class='con-right']/div/div/a"

            elif 'hkjsj' in url:
                xpath = "//div[@class='con-right fr']/div/div/a"

            else:
                xpath = "//div[@class='list-c']/ul/li/p[1]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'plan' in url and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/div/div/div/a', f'/div/div[{i}]/div/a').replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]')
                    if 'ggzy' in url or  'www' in url or  'drc' in url  or  'hkjsj' in url :
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'www' in url:
                            publictime = html_1.xpath(xpath1.replace('[1]/a', "[2]/span") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：', '')
                        elif 'hkjsj' in url:
                            publictime = html_1.xpath(xpath1.replace('div/a', "table/tbody/tr/td[1]") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('div/a', "div/span") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace(
                            '日', '').replace('/', '-')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime.replace(' ', '').replace('[', '').replace(']',''), "%Y-%m-%d")))
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
                                chuli(publictime, href, driver, url, title, city, xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('海口\t', e)
        driver.close()
        return haikou(name)

# todo  三亚  公共资源中心 | 人民政府 |发改委 |住建局
def sanya(name):
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
            'http://zw.hainan.gov.cn/ggzy/syggzy/xwdt1/index.jhtml': 4,  # 公共资源中心 新闻动态
            'http://zw.hainan.gov.cn/ggzy/syggzy/GGtzgg/index.jhtml': 2,  # 公共资源中心 通知公告
            'http://www.sanya.gov.cn/sanyasite/syyw/simple_list.shtml': 134,  # 人民政府 今日三亚
            'http://www.sanya.gov.cn/sanyasite/zwdt/simple_list.shtml': 134,  # 人民政府 政务动态
            'http://www.sanya.gov.cn/sanyasite/gggs/simple_list.shtml': 29,  # 人民政府 公告公示
            'http://www.sanya.gov.cn/sanyasite/zxjd/simple_list.shtml': 7,  # 人民政府 最新解读
            'http://fg.sanya.gov.cn/fgwsite/gzdt/list2.shtml': 33,  # 发改委 工作动态
            'http://fg.sanya.gov.cn/fgwsite/tzgg/list2.shtml': 6,  # 发改委 通知公告
            'http://fg.sanya.gov.cn/fgwsite/zcjd/list2.shtml': 2,  # 发改委 政策解读
            'http://www.sanya.gov.cn/zjjsite/gzdt/list2.shtml': 10,  # 住建局 工作动态
            'http://www.sanya.gov.cn/zjjsite/tzgg/list2.shtml': 13,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zw' in url:
                xpath = "//table[@class='newtable']/tbody/tr[1]/td[2]/a"
            elif 'fg' in url:
                xpath = "//div[@class='list_1 box3']/ul/li"
            else:
                xpath = "//div[@class='list_1']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'plan' in url and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/div/div/div/a', f'/div/div[{i}]/div/a').replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]')
                    if 'zw' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

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
                                chuli(publictime, href, driver, url, title, city, xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('海口\t', e)
        driver.close()
        return haikou(name)

# todo  三沙  公共资源中心 | 人民政府 |发改委（无） |住建局（无）
def sansha(name):
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
            'http://zw.hainan.gov.cn/ggzy/ssggzy/GGtzgg/index.jhtml': 1,  # 公共资源中心 通知公告
            'http://zw.hainan.gov.cn/ggzy/ssggzy/xwdt1/index.jhtml': 1,  # 公共资源中心 新闻动态
            'http://www.sansha.gov.cn/sansha/sysdt/nlist2_new.shtml': 42,  # 人民政府 三沙动态
            'http://www.sansha.gov.cn/sansha/zwfwxxgs/nlist2.shtml': 2,  # 人民政府 三沙信息公示
            'http://www.hainan.gov.cn/hainan/zxjd/list3.shtml': 2,  # 人民政府 最新解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zw' in url:
                xpath = "//table[@class='newtable']/tbody/tr[1]/td[2]/a"
            else:
                xpath = "//div[@class='list_1']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'plan' in url and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/div/div/div/a', f'/div/div[{i}]/div/a').replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]')
                    if 'zw' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime.replace('[', '').replace(']',''), "%Y-%m-%d")))
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
                                chuli(publictime, href, driver, url, title, city, xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('三沙\t', e)
        driver.close()
        return sansha(name)

# todo  儋州  公共资源中心(响应慢) | 人民政府 |发改委（无） |住建局（无）
def danzhou(name):
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
            'http://zw.hainan.gov.cn/ggzy/dzggzy/xwdt1/index.jhtml': 2,  # 公共资源中心 新闻动态
            'http://zw.hainan.gov.cn/ggzy/dzggzy/GGtzgg/index.jhtml': 1,  # 公共资源中心 通知公告
            'https://www.danzhou.gov.cn/danzhou/ywdt/jrdz/': 15,  # 人民政府 今日儋州
            'https://www.danzhou.gov.cn/danzhou/ywdt/ldhd/': 15,  # 人民政府 领导活动
            'https://www.danzhou.gov.cn/danzhou/jdhy/zcjd/zxjd/': 1,  # 人民政府 最新解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zw' in url:
                xpath = "//table[@class='newtable']/tbody/tr[1]/td[2]/a"
            elif 'ywdt' in url:
                xpath = "//dl[@class='listtxt listtxt0 fr']/dd/ul/li"
            else:
                xpath = "//dl[@class='listtxt fr']/dd/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'plan' in url and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/div/div/div/a', f'/div/div[{i}]/div/a').replace('tr/td[', f'tr[{i}]/td[').replace('ul/li', f'ul/li[{i}]')
                    if 'zw' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('\n', '').replace('/', '-').replace('发布时间：', '').replace('[', '').replace(']','')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime.replace('[', '').replace(']',''), "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:

                                chuli(publictime, href, driver, url, title, city, xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('儋州\t', e)
        driver.close()
        return danzhou(name)


hainan('海南')
haikou('海口')
sanya('三亚')
sansha('三沙')
danzhou('儋州')
