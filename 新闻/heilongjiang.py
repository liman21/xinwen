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
pro = '黑龙江'


def chuli(publictime, href, driver, url, title, city, xpath1):
    try:
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if re.findall('http', href):
            link = href
        elif re.findall('szf/jgsz', href):
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href.replace('../','')
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


# todo  黑龙江  公共资源中心
def heilongjiang(name):
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
            'http://www.hljggzyjyw.gov.cn/web/news?cid=1&pageNo=1': 29,  # 公共资源中心 综合新闻
            'http://www.hljggzyjyw.gov.cn/web/news?cid=6&pageNo=1': 23,  # 公共资源中心 通知公告
            'http://www.hljggzyjyw.gov.cn/web/zffg?cid=2': 1,  # 公共资源中心 政策法规
            'http://www.hljggzyjyw.gov.cn/web/zffg?cid=31': 1,  # 公共资源中心 地方法规
            'http://www.hlj.gov.cn/30/35/index1.html': 359,  # 人民政府 龙江要闻
            'http://www.hlj.gov.cn/30/43/index1.html': 845,  # 人民政府  龙江要闻 >> 市县
            'http://www.hljdpc.gov.cn/col/col348/index.html?uid=478&pageNum=1': 23,  # 发改委  龙江要闻 >> 市县 845
            'http://www.hljdpc.gov.cn/col/col293/index.html?uid=4577&pageNum=1': 27,  # 发改委  通知公告 >> 通知
            'http://www.hljdpc.gov.cn/col/col294/index.html?uid=4577&pageNum=1': 6,  # 发改委  通知公告 >> 公告
            'http://www.hljdpc.gov.cn/col/col350/index.html?uid=478&pageNum=1': 8,  # 发改委   委内工作
            'http://www.hljdpc.gov.cn/col/col406/index.html?uid=478&pageNum=1': 12,  # 发改委  市县发改
            'http://www.hljdpc.gov.cn/col/col157/index.html?uid=5700&pageNum=1': 55,  # 发改委  政策解读
            'http://zfcxjst.hlj.gov.cn/plus/list.aspx?tid=444&TotalResult=6051&PageNo=1': 55,  # 住建局  文件通知
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hljggzyjyw' in url:
                xpath = "//div[@class='right_box']/ul/li"
            elif 'hljdpc' in url:
                xpath = "//table[@class='lm_tabe']/tbody/tr/td[1]/a"
            elif 'zfcxjst' in url:
                xpath = "//div[@class='info']/ul/li"
            else:
                xpath = "//div[@class='fr']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if page==1:
                    pass
                else:
                    if 'hljdpc' in url:
                        driver.get(url.replace('pageNum=1',f'pageNum={page}'))
                    elif 'www.hlj.gov.cn' in url:
                        driver.get(url.replace('index1.html',f'index{page}.html'))
                    else:
                        driver.get(url.replace('PageNo=1',f'PageNo={page}'))
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'plan' in url and i%6==0:
                        pass
                  else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hljdpc' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[1]/a', "[2]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        if 'hljggzyjyw' in url:
                            publictime = html_1.xpath(f"{xpath1}/span[@class='date']/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')
                        elif 'www.hlj.gov.cn' in url:
                            publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('日', '').replace('/', '-')[:10]
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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

    except Exception as e:
        print('黑龙江\t', e)
        driver.close()
        return heilongjiang(name)

# todo  哈尔滨  公共资源中心 /人民政府 | 发改委 |住建局（无）
def haerbin(name):
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
            'http://www.hrbggzy.org.cn/xxgk/005004/secondpage.html': 2,  # 公共资源中心 通知公告
            'http://www.hrbggzy.org.cn/xxgk/005003/secondpage.html': 1,  # 公共资源中心 工作动态
            'http://www.harbin.gov.cn/col/col98/index.html': 84,  # 人民政府 今日要闻
            'http://www.harbin.gov.cn/col/col100/index.html': 47,  # 人民政府 区县工作
            'http://www.harbin.gov.cn/col/col101/index.html': 18,  # 人民政府 部门动态
            'http://fgw.harbin.gov.cn/gzdt/': 21,  # 发改委 部门动态
            'http://fgw.harbin.gov.cn/zcfg/sfgwwj/': 2,  # 发改委 政策解读
            'http://fgw.harbin.gov.cn/tzhgg/': 3,  # 发改委 通知公告
            'http://fgw.harbin.gov.cn/bbfz/': 7,  # 发改委 新闻资讯


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hrbggzy' in url:
                xpath = "//div[@class='ewb-con']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
            elif 'fgw' in url:
                xpath = "//div[@class='ldlist_con zw_lb']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            # elif 'xxgk' in url:
            #     xpath = "//table[@class='tb_list']/tbody/tr/td[1]/a"
            #     length = len(html_2.xpath(xpath)) + 2
            else:
                xpath = "//div[@class='default_pgContainer']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'xxgk' in url and i==1:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hrbggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a', "/span") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        if 'hljggzyjyw' in url:
                            publictime = html_1.xpath(f"{xpath1}/span[@class='date']/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')
                        elif 'zfcxjst' in url:
                            publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('日', '').replace('/', '-')[:10]
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

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
                                if 'fgw' in url:
                                    break
                                else:
                                    try:
                                        driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()

                                        except:

                                            try:
                                                driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                            except:
                                                    xy = "//td[contains(string(),'下页')]"
                                                    driver.find_element_by_xpath(xy).click()

                        break
    except Exception as e:
        print('哈尔滨\t', e)
        driver.close()
        return haerbin(name)

# todo  齐齐哈尔  公共资源中心 | 人民政府(响应慢) | 发改委 、住建局（无）
def qiqihaer(name):
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
            'http://ggzy.qqhr.gov.cn/ggfwpt/010004/about.html': 8,  # 公共资源中心 通知公告
            'http://ggzy.qqhr.gov.cn/ggfwpt/010001/about.html': 1,  # 公共资源中心 最新动态
            'http://ggzy.qqhr.gov.cn/zwgk/001003/about.html': 6,  # 公共资源中心 中心动态
            'http://ggzy.qqhr.gov.cn/zcjd/about.html': 1,  # 公共资源中心 政策解读
            'http://www.qqhr.gov.cn/News_showFontNewsList.action?messagekey=146': 105,  # 人民政府 	政务要闻
            'http://www.qqhr.gov.cn/News_showFontNewsList.action?messagekey=4': 152,  # 人民政府 	部门动态
            'http://www.qqhr.gov.cn/News_showFontNewsList.action?messagekey=5': 475,  # 人民政府 		县区工作
            'http://www.qqhr.gov.cn/News_showFontNewsList.action?messagekey=8': 71,  # 人民政府 		通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='ewb-info-bd']/ul/li/div/a"
            else:
                xpath = "/html/body/div[2]/div/table/tbody/tr/td[2]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'www' in url and i<3:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'ggzy' in url or 'www' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        if 'ggzy' in url:
                            publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[4]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

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
                                    driver.find_element_by_xpath(f"//tr/td[7]/a[@class='page'][3]").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('齐齐哈尔\t', e)
        driver.close()
        return qiqihaer(name)

# todo   鸡西(ij)   公共资源中心（无）| 发改委 |人民政府 |住建局
def jixi(name):
    global driver
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
            'http://www.jixi.gov.cn/zwgk/zwdt/': 226,  # 人民政府  政务动态
            'http://www.jixi.gov.cn/syzwyw_2778/': 106,  # 人民政府  今日鸡西
            'http://www.jixi.gov.cn/syszf_2777/': 24,  # 人民政府  市政府
            'http://www.jixi.gov.cn/sybm/': 238,  # 人民政府  部门
            'http://www.jixi.gov.cn/xsq_2780/': 29,  # 人民政府  县（市）区
            'http://www.jixi.gov.cn/flfg/': 24,  # 人民政府  政策法规
            'http://www.jixi.gov.cn/homeyw/': 55,  # 人民政府  要闻
            'http://www.jixi.gov.cn/szf/jgsz/fgw_936/gzdt_3060/': 4,  # 发改委  工作动态
            'http://www.jixi.gov.cn/szf/jgsz/fgw_936/zwxxgk_3061/zcjd_6802/': 2,  # 发改委  政策解读
            'http://www.jixi.gov.cn/szf/jgsz/cxjsj_1076/bmgzzt_1078/': 5,  # 住建局  工作动态
            'http://www.jixi.gov.cn/szf/jgsz/cxjsj_1076/zwxxgk_3141/zcjd_6816/': 5,  # 住建局  政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'zcjd' in url:
                xpath = "//div[@id='listbox1']/ul/li"
            else:
                xpath = "//div[@id='listbox2']/ul/li"

            xpathj = "//div[@id='listbox2']/ul/li[1]"
            jj = len(html_2.xpath(xpathj)) + 1
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1,  pages+1):
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
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
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
        print('鸡西\t',e)
        driver.close()
        return jixi(name)

# todo  鹤岗  公共资源中心 | 发改委 |人民政府 | 住建局（无）
def hegang(name):
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
            'http://www.hgggzyjyw.org.cn/jyfw/about.html': 6,  # 公共资源中心 综合新闻
            'http://www.hgggzyjyw.org.cn/tzgg/about.html': 3,  # 公共资源中心 通知公告
            'http://www.hgggzyjyw.org.cn/zcfg/about.html': 1,  # 公共资源中心 政策法规
            'http://www.hegang.gov.cn/zwfb/z_hgyw/': 234,  # 人民政府 鹤岗新闻
            'http://www.hegang.gov.cn/zwxxgk/gkzn/zfwj/szfwj/': 2,  # 人民政府 市政府文件
            'http://www.hegang.gov.cn/zwfb/zwfb_zcjd/': 4,  # 人民政府 政策解读
            'http://www.hegang.gov.cn/zwfb/z_qxdt/': 10,  # 人民政府 县区动态
            'http://www.hegang.gov.cn/zwfb/z_bmdt/': 17,  # 人民政府 部门动态
            'http://www.hegang.gov.cn/szf/tzgg/': 23,  # 人民政府 通知公告
            'http://www.hegang.gov.cn/zwxxgk/gkzn/szdwl/sfgw/zdgz/': 1,  # 发改委 重点工作

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hgggzyjyw' in url:
                xpath = "//div[@class='ewb-info-bd']/ul/li"
            elif 'sfgw' in url:
                xpath = "//div[@class='sq_nr1']/ul/li"
            else:
                xpath = "//ul/li/span[@class='pull-left']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hegang' in url and 'sfgw' not in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a', "").replace('left', "right") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        if 'hljggzyjyw' in url:
                            publictime = html_1.xpath(f"{xpath1}/span[@class='date']/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')
                        elif 'zfcxjst' in url:
                            publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('日', '').replace('/', '-')[:10]
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('鹤岗\t', e)
        driver.close()
        return hegang(name)

# todo  双鸭山  公共资源中心（无） | 发改委 |人民政府 | 住建局（无）
def shuangyashan(name):
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
            'http://www.shuangyashan.gov.cn/NewCMS/index/html/newslist/newslist_one.jsp?lmid=31': 243,  # 人民政府 时政信息
            'http://www.shuangyashan.gov.cn/NewCMS/index/html/newslist/newslist_one_gg.jsp': 243,  # 人民政府 通知公告
            'http://www.shuangyashan.gov.cn/NewCMS/index/html/newslist/newslist_one.jsp?lmid=254': 118,  # 人民政府 部门动态
            'http://www.shuangyashan.gov.cn/NewCMS/index/html/newslist/newslist_one_q.jsp': 135,  # 人民政府 区域动态
            'http://www.shuangyashan.gov.cn/NewCMS/index/html/newslist/newslist_one_x.jsp': 131,  # 人民政府 县域动态
            'http://www.shuangyashan.gov.cn/NewCMS/index/html/newslist/newslist_one_dw.jsp?lmid=254&dwid=43': 2,  # 发改委 政务信息
                    }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='contain']/form/ul/li"
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
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                        '\r', '')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace(
                    '日', '').replace('/', '-')
                    try:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    except:
                        publictime = html_1.xpath(f"{xpath1}/span[2]/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('双鸭山\t', e)
        driver.close()
        return shuangyashan(name)

# todo  大庆  公共资源中心 | 发改委（无） |人民政府 | 住建局（无）
def daqing(name):
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
            'http://ggzyjyzx.daqing.gov.cn/gnxw/index.htm': 5,  # 公共资源中心 工作动态
            'http://ggzyjyzx.daqing.gov.cn/notice/index.htm': 3,  # 公共资源中心 通知公告
            'http://ggzyjyzx.daqing.gov.cn/zcfgJsgc/index.htm': 1,  # 公共资源中心 政策法规
            'http://www.daqing.gov.cn/zfgz/zfgg/': 10,  # 人民政府 政府公告
            'http://www.daqing.gov.cn/zwdt/qszwxx/': 37,  # 人民政府 全市政务信息
            'http://www.daqing.gov.cn/zfgw/zcjd/': 2,  # 人民政府 政策解读
            'http://www.daqing.gov.cn/zfbm/jsxxgs/': 2,  # 住建局 建设信息公示
                    }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjyzx' in url:
                xpath = "//div[@class='list-con1']/ul/li"
            else:
                xpath = "//div[@class='middle_list_Content']/ul/li"
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
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hegang' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('left', "right") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('/', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('后一页>>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                        break
    except Exception as e:
        print('大庆\t', e)
        driver.close()
        return daqing(name)

# todo  伊春  公共资源中心 | 发改委（无法访问） |人民政府 | 住建局（无）
def yichun(name):
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
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2099&parentChannelId=-1': 3,  # 公共资源中心 综合新闻
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2103&parentChannelId=-1': 1,  # 公共资源中心 通知公告
            'http://ggzy.yc.gov.cn/docweb/docList.action?channelId=2100&parentChannelId=-1': 1,  # 公共资源中心 政策法规
            'http://www.yc.gov.cn/docweb/docList.action?channelId=3980&parentChannelId=3979': 113,  # 人民政府 伊春要闻
            'http://www.yc.gov.cn/docweb/docList.action?channelId=3981&parentChannelId=3979': 26,  # 人民政府 通知公告
            'http://www.yc.gov.cn/docweb/docList.action?channelId=3982&parentChannelId=3979': 175,  # 人民政府 县区动态
            'http://www.yc.gov.cn/docweb/docList.action?channelId=3983&parentChannelId=3979': 65,  # 人民政府 部门动态
            'http://www.yc.gov.cn/docweb/docList.action?channelId=4024&parentChannelId=3987': 65,  # 人民政府 市级政策解读

                    }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='trends']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'www.yc' in url:
                xpath = "//table[@class='list']/tbody/tr/td[1]/a"
                length = len(html_2.xpath(xpath)) + 2
            else:
                xpath = "//div[@class='middle_list_Content']/ul/li"
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
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'www.yc' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[1]/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('.', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('后一页>>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                        break
    except Exception as e:
        print('伊春\t', e)
        driver.close()
        return yichun(name)


# todo  佳木斯  公共资源中心（无） | 发改委 |人民政府 | 住建局（无）
def jiamusi(name):
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
            'http://www.jms.gov.cn/html/index/page/000100050001_1.html': 142,  # 人民政府 本地要闻
            'http://www.jms.gov.cn/html/index/page/000100050002_1.html': 52,  # 人民政府 重要政务
            'http://www.jms.gov.cn/html/index/page/000100050003_1.html': 441,  # 人民政府 区县动态
            'http://www.jms.gov.cn/html/index/page/000100050004_1.html': 154,  # 人民政府 部门动态
            'http://www.jms.gov.cn/html/index/page/000100050009_1.html': 101,  # 人民政府 公告公示
            'http://www.jms.gov.cn/html/zwgk/page/10062_1.html': 3,  # 人民政府 政策解读
            'http://www.hljdpc.gov.cn/col/col348/index.html': 92,  # 发改委 要闻资讯
            'http://www.hljdpc.gov.cn/col/col293/index.html': 27,  # 发改委 通知
            'http://www.hljdpc.gov.cn/col/col294/index.html': 6,  # 发改委 公告
            'http://www.hljdpc.gov.cn/col/col350/index.html': 8,  # 发改委 委内工作
            'http://www.hljdpc.gov.cn/col/col406/index.html': 12,  # 发改委 市县发改
            'http://www.hljdpc.gov.cn/col/col157/index.html': 56,  # 发改委 政策解读

                    }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jms' in url:
                xpath = "//div[@class='jms_listC']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'hljdpc' in url:
                xpath = "//table[@class='lm_tabe']/tbody/tr/td[1]/a"
                length = len(html_2.xpath(xpath)) + 1
            else:
                xpath = "//table[@id='mylist']/tbody/tr/td[1]/a"
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
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if '10062_1' in url or 'hljdpc' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        if '10062_1' in url:
                            publictime = html_1.xpath(xpath1.replace('[1]/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('[1]/a', "[@class='bt_time']") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('.', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                        break
    except Exception as e:
        print('佳木斯\t', e)
        driver.close()
        return jiamusi(name)

# todo  七台河  公共资源中心（无） | 发改委 |人民政府 | 住建局（无）
def qitaihe(name):
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
            'http://www.qth.gov.cn/xxgk_12340/szyw/': 25,  # 人民政府 本地要闻
            'http://www.qth.gov.cn/xxgk_12340/tzgg/': 18,  # 人民政府 通知公告
            'http://www.qth.gov.cn/xxgk_12340/qxdt/': 25,  # 人民政府 区县动态
            'http://www.qth.gov.cn/xxgk_12340/bmdt/': 25,  # 人民政府 部门动态
            'http://www.qth.gov.cn/xxsbxt/sxdw/fgwxx/': 1,  # 发改委
            'http://www.qth.gov.cn/xxsbxt/sxdw/fcj/': 3,  # 住建局
                    }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'qth' in url:
                xpath = "//table[2]/tbody/tr[3]/td/table/tbody/tr/td/a"
                length = len(html_2.xpath(xpath)) + 2
            elif 'hljdpc' in url:
                xpath = "//table[@class='lm_tabe']/tbody/tr/td[1]/a"
                length = len(html_2.xpath(xpath)) + 1
            else:
                xpath = "//table[@id='mylist']/tbody/tr/td[1]/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'qth' in url and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'qth' in url or 'hljdpc' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        if 'qth' in url:
                            publictime = html_1.xpath(xpath1.replace('/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('[1]/a', "[@class='bt_time']") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('.', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                        break
    except Exception as e:
        print('七台河\t', e)
        driver.close()
        return qitaihe(name)

# todo  牡丹江  公共资源中心（无） | 发改委 |人民政府 | 住建局
def mudanjiang(name):
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
            'http://wcmplu.mdj.gov.cn:8081/govsearch/bumen.jsp?name=%E5%B8%82%E5%85%AC%E5%85%B1%E8%B5%84%E6%BA%90%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&channelid=6864&themecat=291&catname=%E9%83%A8%E9%97%A8%E6%96%87%E4%BB%B6': 1,  # 市公共资源交易中心 部门文件
            'http://wcmplu.mdj.gov.cn:8081/govsearch/bumen.jsp?name=%E5%B8%82%E5%85%AC%E5%85%B1%E8%B5%84%E6%BA%90%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&channelid=6864&themecat=294&catname=%E9%87%8D%E7%82%B9%E5%B7%A5%E4%BD%9C': 1,  # 市公共资源交易中心 重点工作
            'http://wcmplu.mdj.gov.cn:8081/govsearch/bumen.jsp?name=%E5%B8%82%E5%85%AC%E5%85%B1%E8%B5%84%E6%BA%90%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&channelid=6864&themecat=263&catname=%E6%B3%95%E5%BE%8B%E6%B3%95%E8%A7%84': 1,  # 市公共资源交易中心 法律法规
            'http://wcmplu.mdj.gov.cn:8081/govsearch/bumen.jsp?name=%E5%B8%82%E5%85%AC%E5%85%B1%E8%B5%84%E6%BA%90%E4%BA%A4%E6%98%93%E4%B8%AD%E5%BF%83&channelid=6864&themecat=308&catname=%E5%85%B6%E4%BB%96%E4%BF%A1%E6%81%AF': 1,  # 市公共资源交易中心 其他信息
            'http://www.mdj.gov.cn/shizheng/djyw/': 200,  # 人民政府 雪城要闻
            'http://www.mdj.gov.cn/shizheng/ttxw/': 23,  # 人民政府 头条新闻
            'http://www.mdj.gov.cn/shizheng/bmdt/': 44,  # 人民政府 部门动态
            'http://www.mdj.gov.cn/shizheng/xsqdt/': 52,  # 人民政府 县市动态
            'http://wcmplu.mdj.gov.cn:8081/govsearch/bumen.jsp?name=%E5%B8%82%E5%8F%91%E6%94%B9%E5%A7%94&channelid=6872&themecat=294&catname=%E9%87%8D%E7%82%B9%E5%B7%A5%E4%BD%9C': 1,  # 发改委  重点工作
            'http://wcmplu.mdj.gov.cn:8081/govsearch/bumen.jsp?name=%E5%B8%82%E5%9F%8E%E4%B9%A1%E5%BB%BA%E8%AE%BE%E5%B1%80&channelid=6887&themecat=294&catname=%E9%87%8D%E7%82%B9%E5%B7%A5%E4%BD%9C': 1,  # 住建局  重点工作
                    }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='common_list m_h400']/ul/li"
                length = len(html_2.xpath(xpath)) + 2
            else:
                xpath = "//div[@class='row']/li[@class='mc']/div/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'qth' in url and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[').replace(']/li', f'][{i}]/li')
                    if 'wcmplu' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("'mc']/div/a", "'fbrq']") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('.', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                        break
    except Exception as e:
        print('牡丹江\t', e)
        driver.close()
        return mudanjiang(name)

# todo  黑河  公共资源中心（无） | 发改委 |人民政府 | 住建局
def heihe(name):
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
            'http://www.heihe.gov.cn/index/zwyw.htm': 136,  # 人民政府 政务要闻
            'http://www.heihe.gov.cn/egovtree/1397/EGOVCOLUMNCONTENT/xxgk/xxgk-three-list.htm': 7,  # 人民政府 政府文件
            'http://www.heihe.gov.cn/zwfb/zcjd.htm': 5,  # 人民政府 政策解读
            'http://www.heihe.gov.cn/zwfb/bmdt.htm': 141,  # 人民政府 部门动态
            'http://www.heihe.gov.cn/zwfb/xsdt/x_s_zy.htm': 141,  # 人民政府 县市动态
            'http://zwgk.heihe.gov.cn/xzbmym.jsp?urltype=tree.TreeTempUrl&wbtreeid=1393': 1,  # 发改委
            'http://zwgk.heihe.gov.cn/xzbmym.jsp?urltype=tree.TreeTempUrl&wbtreeid=1368': 20,  # 住建局
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='news-list-con']/ul/li"
                length = len(html_2.xpath(xpath)) + 2
            else:
                xpath = "//table[@class='winstyle151845']/tbody/tr/td[2]/span/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'zwgk' in url and i==1:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[').replace(']/li', f'][{i}]/li')
                    if 'zwgk' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("[2]/span/a", "[3]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('.', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页'))
                        break
    except Exception as e:
        print('黑河\t', e)
        driver.close()
        return heihe(name)

# todo  绥化  公共资源中心（无） | 发改委 |人民政府、住建局（无）
def suihua(name):
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
            'http://www.suihua.gov.cn/pages/website/list.html?permission_id=43': 52,  # 人民政府 本地要闻
            'http://www.suihua.gov.cn/pages/website/list.html?permission_id=46': 6,  # 人民政府 公告信息
            'http://www.suihua.gov.cn/pages/website/list.html?permission_id=48': 3,  # 人民政府 政策解读
            'http://www.suihua.gov.cn/pages/website/tablelist.html?permission_id=45': 38,  # 人民政府 县市动态
            'http://www.suihua.gov.cn/pages/website/listBMDT.html?permission_id=44': 108,  # 人民政府 部门动态

            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'list' in url:
                xpath = "//div[@class='yc_info_con4']/ul/li"
                length = len(html_2.xpath(xpath)) + 2
            else:
                xpath = "//table[@id='biuuu_city_list']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'zwgk' in url and i==1:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[').replace(']/li', f'][{i}]/li')
                    if 'tablelist' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("[2]/a", "[4]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('(', '').replace(')','').replace('日', '').replace('.', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页'))
                        break
    except Exception as e:
        print('绥化\t', e)
        driver.close()
        return suihua(name)




# heilongjiang('黑龙江')
# haerbin('哈尔滨')
qiqihaer('齐齐哈尔')
jixi('鸡西')
hegang('鹤岗')
shuangyashan('双鸭山')
daqing('大庆')
yichun('伊春')
jiamusi('佳木斯')
qitaihe('七台河')
mudanjiang('牡丹江')
heihe('黑河')
suihua('绥化')
