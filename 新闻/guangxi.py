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
pro = '广西'


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


# todo  广西  公共资源中心
def guangxi(name):
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
            'http://gxggzy.gxzf.gov.cn/gxzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001': 1,  # 公共资源中心 中心动态  5
            'http://gxggzy.gxzf.gov.cn/gxzbw/ztbdt/009003/MoreInfo.aspx?CategoryNum=009003': 1,  # 公共资源中心 综合新闻   2
            'http://gxggzy.gxzf.gov.cn/gxzbw/tzgg/MoreInfo.aspx?CategoryNum=008': 1,  # 公共资源中心 通知公告   3

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'gxggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            else:
                xpath = "//li[@class='clearfix']/div/h3"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'gxggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
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
                                    driver.find_element_by_xpath(f"//div[@id='MoreInfoList1_Pager']/table/tbody/tr/td[2]/a[{page-1}]").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('广西\t', e)
        driver.close()
        return guangxi(name)

# todo   广西(ij)   发改委 |人民政府 |住建局
def guangxi1(name):
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
            'http://www.gxzf.gov.cn/gxyw/': 34,  # 人民政府  广西要闻
            'http://www.gxzf.gov.cn/zwhd/': 34,  # 人民政府  政务活动
            'http://www.gxzf.gov.cn/zcjd/': 4,  # 人民政府  政策解读
            'http://www.gxzf.gov.cn/gggs/': 4,  # 人民政府  公告公示
            'http://www.gxzf.gov.cn/xwfb/': 7,  # 人民政府  新闻发布
            'http://fgw.gxzf.gov.cn/xwzx/fgyw/': 19,  # 发改委  发改要闻
            'http://fgw.gxzf.gov.cn/zwgk/wjzx/tzgg/': 8,  # 发改委 通知公告
            'http://fgw.gxzf.gov.cn/xwzx/xwfb/': 3,  # 发改委 新闻发布
            'http://fgw.gxzf.gov.cn/xwzx/mtgz/': 1,  # 发改委 媒体关注
            'http://fgw.gxzf.gov.cn/zwgk/wjzx/zcjd/': 2,  # 发改委 政策解读
            'http://zjt.gxzf.gov.cn/wjtz/': 10,  # 住建局 文件通知
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('.','-').replace('\t','').replace('\r','').replace('（','').replace('）','')
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
        print('广西\t',e)
        driver.close()
        return guangxi1(name)


# todo  南宁  公共资源中心
def nanning(name):
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
            'https://www.nnggzy.org.cn/nnzbwmanger/ShowInfo/more.aspx?categoryNum=009001': 1,  # 公共资源中心 工作动态   5
            'https://www.nnggzy.org.cn/gxnnzbw/ShowInfo/more.aspx?categoryNum=008': 1,  # 公共资源中心 通知公告
            'http://fgw.nanning.gov.cn/zwxxdt/tzgg/': 7,  # 发改委 通知公告
            'http://fgw.nanning.gov.cn/zwxxdt/zwxx/': 22,  # 发改委 政务信息
            'http://zjj.nanning.gov.cn/dtzx/gzdt/': 30,  # 住建局 工作动态
            'http://zjj.nanning.gov.cn/dtzx/tzgg/zhgl/': 32,  # 住建局 综合管理
            'http://zjj.nanning.gov.cn/xxgk/zcfgyzcjd/zcjd1/': 2,  # 住建局 政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'nnggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            elif 'zjj' in url:
                xpath = "//div[@class='nav1Cont']/ul/li"
            else:
                xpath = "//div[@class='box1']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'nnggzy' in url or 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        if 'fgw' in url:
                            publictime = html_1.xpath(xpath1.replace('/a', "/font") + "/text()")[0].strip().replace('/', '-').replace('[', '-').replace(']', '-')
                        else:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
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
                                if '008' in url:
                                    driver.find_element_by_xpath("//td[contains(string(),'下页')]").click()
                                else:
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
        print('南宁\t', e)
        driver.close()
        return nanning(name)
# todo   南宁(ij)   发改委 |人民政府 |住建局
def nanning1(name):
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
            'http://www.nanning.gov.cn/ywzx/bmdt/': 13,  # 人民政府  部门动态
            'http://www.nanning.gov.cn/ywzx/nnyw/': 14,  # 人民政府  南宁要闻
            'http://www.nanning.gov.cn/ywzx/xqdt/': 14,  # 人民政府  县区动态
            'http://www.nanning.gov.cn/ywzx/ldhd/': 15,  # 人民政府  领导活动
            'http://www.nanning.gov.cn/ywzx/zzqyw/': 15,  # 人民政府  自治区要闻
            'http://www.nanning.gov.cn/ywzx/gggs/': 14,  # 人民政府  公告公示
            'http://www.nanning.gov.cn/ywzx/tpxw/': 12,  # 人民政府  图片新闻
            'http://www.nanning.gov.cn/ywzx/zfhy/': 5,  # 人民政府  政府会议
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='nav1Cont']/ul/li"
            xpathj = "//div[@class='nav1Cont']/ul/li[1]"
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
                        publictime = html_1.xpath(f"{xpath1}/span[2]/text()")[0].strip().replace('\n','').replace('.','-').replace('\t','').replace('\r','')
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
        print('南宁\t',e)
        driver.close()
        return nanning1(name)

# todo  柳州  公共资源中心
def liuzhou(name):
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
            'http://ggzy.liuzhou.gov.cn/gxlzzbw/ztbdt/009003/MoreInfo.aspx?CategoryNum=9003': 5,  # 公共资源中心 通知公告
            'http://ggzy.liuzhou.gov.cn/gxlzzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=9001': 5,  # 公共资源中心 新闻动态
            'http://www.liuzhou.gov.cn/xwzx/zwyw/': 40,  # 人民政府 柳州要闻
            'http://www.liuzhou.gov.cn/xwzx/bmdt/': 273,  # 人民政府 部门动态
            'http://www.liuzhou.gov.cn/xwzx/qxdt/': 80,  # 人民政府 区县动态
            'http://www.liuzhou.gov.cn/xwzx/notice/': 60,  # 人民政府 通知公告
            'http://fgw.liuzhou.gov.cn/zhdt/': 15,  # 发改委 综合动态
            'http://fgw.liuzhou.gov.cn/tzgg/': 4,  # 发改委 通知公告
            'http://fgw.liuzhou.gov.cn/xxgk/zcwj/zcjd/': 2,  # 发改委 政策解读
            'http://zjj.liuzhou.gov.cn/gzdt/': 1,  # 住建局 工作动态
            'http://zjj.liuzhou.gov.cn/bszn_42347/': 1,  # 住建局 最新文件通知
            'http://zjj.liuzhou.gov.cn/bszn_42026/bszn_42026/': 1,  # 住建局 政策规范
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td/div/a"
            elif 'fgw' in url:
                xpath = "//div[@class='wzlb']/ul/li"
            elif 'zjj' in url:
                xpath = "//div[@class='newslist']/ul/li"
            else:
                xpath = "//li[@class='clearfix']/div/h3"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'ggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
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
                                # try:
                                #     driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                # except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('柳州\t', e)
        driver.close()
        return liuzhou(name)


# todo  桂林  公共资源中心
def guilin(name):
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
            # 'http://glggzy.org.cn/gxglzbw/ztbdt/009001/': 1,  # 公共资源中心 工作动态
            # 'http://glggzy.org.cn/gxglzbw/tzgg/': 1,  # 公共资源中心 通知公告
            # 'http://www.guilin.gov.cn/ywdt/zwdt/': 1,  # 人民政府 政务动态
            # 'http://www.guilin.gov.cn/ywdt/bmdt/': 1,  # 人民政府 部门动态
            # 'http://www.guilin.gov.cn/ywdt/xqdt/': 1,  # 人民政府 县区动态
            # 'http://www.guilin.gov.cn/ywdt/xwgz/': 1,  # 人民政府 新闻关注
            # 'http://www.guilin.gov.cn/ywdt/gggs/': 1,  # 人民政府 公告公示
            'http://fgw.guilin.gov.cn/tztg/': 1,  # 发改委 通知公告
            'http://fgw.guilin.gov.cn/glfzggdt/wnyw/': 1,  # 发改委 发展改革工作
            'http://fgw.guilin.gov.cn/glfzggdt/glyw/': 1,  # 发改委 桂林市要闻
            'http://fgw.guilin.gov.cn/zcfg/': 1,  # 发改委 政策法规
            'http://zj.guilin.gov.cn/dtzx/gzdt/': 1,  # 住建局 工作动态
            'http://zj.guilin.gov.cn/dtzx/tzgg/': 1,  # 住建局 通知公告
            'http://zj.guilin.gov.cn/zcfg/flfggz/': 1,  # 住建局 法律法规规章
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'glggzy' in url:
                xpath = "//div[@id='right']/ul/li/div/a"
            elif 'fgw' in url:
                xpath = "//div[@id='main']/div[2]/div/div/div[2]/ul/li"
            elif 'zj' in url:
                xpath = "//div[@class='lf']/div/ul/li"
            else:
                xpath = "//div[@id='morelist']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'glggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ','').replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')
                    elif 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[1].strip().replace('\n', '').replace('▪   ','').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "/a/span/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace('▪   ','').replace(
                            '\r', '')
                        if 'zj' in url:
                            publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('[', '').replace(']','').replace(
                            '日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']','').replace(
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
                                    driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))

    except Exception as e:
        print('桂林\t', e)
        driver.close()
        return guilin(name)


# todo  梧州  公共资源中心
def wuzhou(name):
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
            'http://www.wzggzy.cn/gxwzzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001': 2,  # 公共资源中心 工作动态
            'http://www.wzggzy.cn/gxwzzbw/tzgg/MoreInfo.aspx?CategoryNum=008': 2,  # 公共资源中心 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'wzggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            else:
                xpath = "//div[@id='morelist']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'wzggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ','').replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')
                    elif 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[1].strip().replace('\n', '').replace('▪   ','').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "span/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace('▪   ','').replace(
                            '\r', '')
                        if 'zj' in url:
                            publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('[', '').replace(']','').replace(
                            '日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']','').replace(
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
                                    driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))

    except Exception as e:
        print('梧州\t', e)
        driver.close()
        return wuzhou(name)
# todo   梧州(ij)   发改委 |人民政府 |住建局
def wuzhou1(name):
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
            'http://www.wuzhou.gov.cn/zwgk/xxgkml/jcxxgk/zwdt/tzgg/': 3,  # 人民政府  通知公告
            'http://www.wuzhou.gov.cn/zwgk/xxgkml/jcxxgk/zwdt/jrwz/': 19,  # 人民政府  今日梧州
            'http://www.wuzhou.gov.cn/zwgk/xxgkml/jcxxgk/zwdt/bmdt/': 34,  # 人民政府  部门动态
            'http://www.wuzhou.gov.cn/zwgk/xxgkml/jcxxgk/zwdt/xqdt/': 34,  # 人民政府  县区动态
            'http://fgw.wuzhou.gov.cn/zwdt/': 10,  # 发改委  政务动态
            'http://fgw.wuzhou.gov.cn/gggs/': 3,  # 发改委  公告公示
            'http://fgw.wuzhou.gov.cn/xxgk/zcwj/': 19,  # 发改委  政策文件
            'http://zjj.wuzhou.gov.cn/xxgk/zwdt/tzgg/': 10,  # 住建局  通知公告
            'http://zjj.wuzhou.gov.cn/xxgk/zwdt/gzdt/': 4,  # 住建局  工作动态
            'http://zjj.wuzhou.gov.cn/xxgk/jcxx/wjzl/flfg/': 1,  # 住建局   法律法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
        print('梧州\t',e)
        driver.close()
        return wuzhou(name)

# todo  北海  公共资源中心
def beihai(name):
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
            'http://www.bhsggzy.cn/gxbhzbw/tzgg/MoreInfo.aspx?CategoryNum=008': 2,  # 公共资源中心 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'bhsggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            else:
                xpath = "//div[@id='morelist']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'bhsggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ','').replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')
                    elif 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[1].strip().replace('\n', '').replace('▪   ','').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "span/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace('▪   ','').replace(
                            '\r', '')
                        if 'zj' in url:
                            publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('[', '').replace(']','').replace(
                            '日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']','').replace(
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
                                    driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))

    except Exception as e:
        print('北海\t', e)
        driver.close()
        return beihai(name)
# todo   北海(ij)   发改委 |人民政府 |住建局
def beihai1(name):
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
            'http://www.beihai.gov.cn/xwdt/bhyw/': 50,  # 人民政府  北海要闻
            'http://www.beihai.gov.cn/xwdt/spxw/': 50,  # 人民政府  视频新闻
            'http://www.beihai.gov.cn/xwdt/bmdt/': 50,  # 人民政府  部门动态
            'http://www.beihai.gov.cn/zwgg/': 50,  # 人民政府  政务公告
            'http://www.beihai.gov.cn/zwgk/jcxxgk/zcjd_88294/bjzcjd/': 3,  # 人民政府  政策解读
            'http://www.beihai.gov.cn/zwgk/jcxxgk/bmgg/': 50,  # 人民政府  部门公告
            'http://xxgk.beihai.gov.cn/bhsfzhggwyh/gzdt_84198/': 50,  # 发改委  工作信息
            'http://xxgk.beihai.gov.cn/bhsfzhggwyh/tzgg_84199/': 50,  # 发改委  通知公告
            'http://xxgk.beihai.gov.cn/bhsfzhggwyh/zcfgzl_84200/zcfg_88779/': 2,  # 发改委  政策解读
            'http://xxgk.beihai.gov.cn/bhszfhcxjsj/gzdt_84530/': 50,  # 住建局  工作信息
            'http://xxgk.beihai.gov.cn/bhszfhcxjsj/tzgg_84531/': 50,  # 住建局  通知公告
            'http://xxgk.beihai.gov.cn/bhszfhcxjsj/zcfgzl_84532/zcfg_88769/': 4,  # 住建局  政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='ov']/div/ul/li"
            xpathj = "//div[@class='ov']/div/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('北海\t',e)
        driver.close()
        return beihai1(name)

# todo  防城港  公共资源中心
def fangchenggang(name):
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
            'http://www.fcgggzy.cn/gxfcgzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001': 2,  # 公共资源中心 通知公告
            'http://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/': 25,  # 人民政府 防城港要闻
            'http://www.fcgs.gov.cn/zxzx/zzqyw/': 2,  # 人民政府 自治区要闻
            'http://www.fcgs.gov.cn/zxzx/rdzx/': 25,  # 人民政府 热点资讯
            'http://www.fcgs.gov.cn/zxzx/xqdt/': 25,  # 人民政府 县区动态
            'http://www.fcgs.gov.cn/zxzx/bmdt/': 25,  # 人民政府 部门聚焦

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fcgggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@class='rightDiv']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 if 'www.fcgs' in url and i%6==0:
                        pass
                 else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'www.fcgs' in url:
                        href = html_1.xpath(f"{xpath1}/span/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span/a/text()")[0].strip().replace('\n', '').replace('\t','▪   ', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace('日', '').replace('/', '-')
                    else:

                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ','').replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/', '-').replace('[', '').replace(']','')


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
                                    driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))

    except Exception as e:
        print('防城港\t', e)
        driver.close()
        return fangchenggang(name)
# todo   防城港(ij)   发改委 |人民政府 |住建局
def fangchenggang1(name):
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
            'http://fgw.fcgs.gov.cn/zwdt/': 3,  # 发改委  政务动态
            'http://fgw.fcgs.gov.cn/xxgk/zcwj/': 1,  # 发改委  政策文件
            'http://zjj.fcgs.gov.cn/zwdt/': 5,  # 住建局  政务动态
            'http://zjj.fcgs.gov.cn/xxgk/zcwj/': 1,  # 住建局  政策文件
            'http://zjj.fcgs.gov.cn/xxcxygs/xxgs/': 4,  # 住建局  信息公示

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('防城港\t',e)
        driver.close()
        return fangchenggang1(name)

# todo  钦州  公共资源中心
def qinzhou(name):
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
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001': 5,  # 公共资源中心 工作动态
            'http://ggzyjy.qinzhou.gov.cn/gxqzzbw/tzgg/MoreInfo.aspx?CategoryNum=008': 2,  # 公共资源中心 通知公告
            'http://www.qinzhou.gov.cn/zwgk_213/jcxx/tzgg/': 5,  # 人民政府 通知公告
            'http://www.qinzhou.gov.cn/xwdt_239/qxdt/': 83,  # 人民政府 区县动态
            'http://www.qinzhou.gov.cn/xwdt_239/bmdt/': 81,  # 人民政府 部门动态
            'http://www.qinzhou.gov.cn/xwdt_239/zwyw/': 119,  # 人民政府 政务要闻
            'http://www.qinzhou.gov.cn/zcwj_246/zcjd/': 6,  # 人民政府 政策解读
            'http://zwgk.qinzhou.gov.cn/auto2521/gzdt_2874/': 6,  # 发改委 工作动态
            'http://zjj.qinzhou.gov.cn/zwgk_12788/bwdt/': 10,  # 住建局 本局动态
            'http://zjj.qinzhou.gov.cn/zwgk_12788/gsgg_12861/': 25,  # 住建局 公示公告
            'http://zjj.qinzhou.gov.cn/zwgk_12788/zcfg_12815/': 2,  # 住建局 政策法规及解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath))+1
            elif 'zwgk' in url:
                xpath = "//table[@id='bbsTab']/tbody/tr/td/a"
                length = len(html_2.xpath(xpath))+1
            elif 'zjj' in url:
                xpath = "//div[@class='lbyBox']/ul/li"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@class='sublist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 if 'www' in url or 'zjj' in url and i%6==0:
                        pass
                 else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'ggzyjy' in url or 'zwgk' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ', '').replace('\n',
                                                                                                        '').replace(
                            '\t', '').replace(
                            '\r', '')
                        if 'ggzyjy' in url:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/',
                                                                                                                 '-').replace(
                            '[', '').replace(']', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('/a', "[5]") + "/text()")[0].strip().replace(
                                '/',
                                '-').replace(
                                '[', '').replace(']', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                             '▪   ',
                                                                                                             '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
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
                                    driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))

    except Exception as e:
        print('钦州\t', e)
        driver.close()
        return qinzhou(name)
# todo  钦州  人民政府 | 发改委| 住建局
def qinzhou1(name):
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
            'http://www.qinzhou.gov.cn/zwgk_213/jcxx/tzgg/index.html': 5,  # 人民政府 通知公告
            'http://www.qinzhou.gov.cn/xwdt_239/qxdt/index.html': 83,  # 人民政府 区县动态
            'http://www.qinzhou.gov.cn/xwdt_239/bmdt/index.html': 81,  # 人民政府 部门动态
            'http://www.qinzhou.gov.cn/xwdt_239/zwyw/index.html': 119,  # 人民政府 政务要闻
            'http://www.qinzhou.gov.cn/zcwj_246/zcjd/index.html': 6,  # 人民政府 政策解读
            'http://zwgk.qinzhou.gov.cn/auto2521/gzdt_2874/index.html': 41,  # 发改委 工作动态
            'http://zwgk.qinzhou.gov.cn/auto2521/bmwj_2875/': 35,  # 发改委 部门文件
            'http://zjj.qinzhou.gov.cn/zwgk_12788/bwdt/index.html': 10,  # 住建局 本局动态
            'http://zjj.qinzhou.gov.cn/zwgk_12788/gsgg_12861/index.html': 25,  # 住建局 公示公告
            'http://zjj.qinzhou.gov.cn/zwgk_12788/zcfg_12815/index.html': 2,  # 住建局 政策法规及解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            # driver.get(url)
            # con = driver.page_source
            # html_2 = etree.HTML(con)
            if 'ggzyjy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                # length = len(html_2.xpath(xpath))+1
            elif 'zwgk' in url:
                xpath = "//table[@id='bbsTab']/tbody/tr/td/a"
                # length = len(html_2.xpath(xpath))+1
            elif 'zjj' in url:
                xpath = "//div[@class='lbyBox']/ul/li"
                # length = len(html_2.xpath(xpath))+1
            else:
                xpath = ""
                # length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                if page==1:
                    driver.get(url)
                else:
                    driver.get(url.replace('index.html',f'index_{page}.html'))
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                length = len(html_1.xpath(xpath)) + 1
                if po > 0:
                    break
                for i in range(1, length):
                 if 'www' in url or 'zjj' in url and i%6==0:
                        pass
                 else:
                    # lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'ggzyjy' in url or 'zwgk' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ', '').replace('\n',
                                                                                                        '').replace(
                            '\t', '').replace(
                            '\r', '')
                        if 'ggzyjy' in url:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]") + "/text()")[0].strip().replace('/',
                                                                                                                 '-').replace(
                            '[', '').replace(']', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('/a', "[5]") + "/text()")[0].strip().replace(
                                '/',
                                '-').replace(
                                '[', '').replace(']', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                             '▪   ',
                                                                                                             '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
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
                    # if i == lengt:
                    #     if lengt < length - 1:
                    #         break
                    #     else:
                    #         if page != pages:
                    #             try:
                    #                 driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                    #                 break
                    #             except:
                    #                 try:
                    #                     driver.execute_script("arguments[0].click();",
                    #                                           driver.find_element_by_link_text('下页>'))
                    #                 except:
                    #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))

    except Exception as e:
        print('钦州\t', e)
        driver.close()
        return qinzhou1(name)


# todo  贵港  公共资源中心
def guigang(name):
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
            'http://ggggjy.gxgg.gov.cn:9005/zxdt/about.html': 13,  # 公共资源中心 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggggjy' in url:
                xpath = "//div[@class='ewb-con-bd']/ul/li/div/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@class='sublist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'www' in url and i%6==0:
                 #        pass
                 # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'ggggjy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('▪   ', '').replace('\n', '').replace(
                            '\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('/','-').replace(
                            '[', '').replace(']', '')

                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace(
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
                                    driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('[下一页]'))
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('»'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
    except Exception as e:
        print('贵港\t', e)
        driver.close()
        return guigang(name)
# todo   贵港(ij)   发改委（无） |人民政府 |住建局（无）
def guigang1(name):
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
            'http://www.gxgg.gov.cn/zwdt/': 25,  # 人民政府  政务动态
            'http://www.gxgg.gov.cn/bmdt/': 34,  # 人民政府  部门动态
            'http://www.gxgg.gov.cn/tzgg/': 3,  # 人民政府  通知公告
            'http://www.gxgg.gov.cn/xxgk/zcjd/': 8,  # 人民政府  政策解读
            'http://www.gxgg.gov.cn/gdtt/': 34,  # 人民政府  更多头条
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
        print('贵港\t',e)
        driver.close()
        return guigang1(name)

# todo  玉林  公共资源中心 |人民政府 |发改委 |住建局
def yulin(name):
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
            'http://ggzy.yulin.gov.cn/tzgg/moreinfoonly.html': 2,  # 公共资源中心 通知公告
            'http://www.yulin.gov.cn/jryl/zwxx/': 34,  # 人民政府 政务信息
            'http://www.yulin.gov.cn/zfgzdt/bmdt/': 34,  # 人民政府 部门动态
            'http://www.yulin.gov.cn/zfgzdt/xsqdt/': 34,  # 人民政府 县（市、区）动态
            'http://www.yulin.gov.cn/zfgzdt/tzgg/': 5,  # 人民政府 通知公告
            'http://www.yulin.gov.cn/zwgk/jcxx/zcjd/': 3,  # 人民政府 政策解读
            'http://fgw.yulin.gov.cn/zwdt/zwyw/': 5,  # 发改委 政务动态
            'http://fgw.yulin.gov.cn/zwdt/tzgg/': 3,  # 发改委 通知公告
            'http://zjj.yulin.gov.cn/tzgg/': 1,  # 住建局 通知公告
            'http://zjj.yulin.gov.cn/zwyw/': 3,  # 住建局 政务要闻
            'http://zjj.yulin.gov.cn/zcjd/': 4,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='col-md-19']/ul/li/div/a"
                length = len(html_2.xpath(xpath))+1
            elif 'zjj' in url:
                xpath = "//div[@id='morelist']/ul/li/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@id='morelist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'www' in url and i%6==0:
                 #        pass
                 # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'ggzy' in url or 'zjj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'zjj' in url:
                            publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('/','-').replace(
                            '（', '').replace('）', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('/a', "") + "/text()")[0].strip().replace(
                                '/', '-').replace('[', '').replace(']', '')

                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace(
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
                                    driver.find_element_by_xpath("//ul[@class='m-pagination-page']/li[2]/a").click()
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('»'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
    except Exception as e:
        print('玉林\t', e)
        driver.close()
        return yulin(name)


# todo  百色  公共资源中心 |人民政府 |发改委 |住建局
def baise(name):
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
            'http://www.bsggzy.org.cn/gxbszbw/ztbdt/009001/': 1,  # 公共资源中心 工作动态
            'http://www.bsggzy.org.cn/gxbszbw/tzgg/': 1,  # 公共资源中心 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'bsggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@id='morelist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'www' in url and i%6==0:
                 #        pass
                 # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'bsggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('2]/a', "3]") + "/text()")[0].strip().replace(
                                '/', '-').replace('[', '').replace(']', '')

                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace(
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
                                    driver.find_element_by_xpath("//ul[@class='m-pagination-page']/li[2]/a").click()
                                    break
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('»'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
    except Exception as e:
        print('百色\t', e)
        driver.close()
        return baise(name)
# todo   百色(ij)   发改委 |人民政府 |住建局
def baise1(name):
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
            'http://www.baise.gov.cn/xwdt/zwyw/': 34,  # 人民政府  政务要闻
            'http://www.baise.gov.cn/tzgg/': 6,  # 人民政府  通知公告
            'http://www.baise.gov.cn/xwdt/bmdt/': 30,  # 人民政府  部门动态
            'http://www.baise.gov.cn/xwdt/xqdt/': 22,  # 人民政府  县区动态
            'http://fgw.baise.gov.cn/xwzx/wndt/': 8,  # 发改委  委内动态
            'http://fgw.baise.gov.cn/xwzx/bsyw/': 2,  # 发改委  百色要闻
            'http://zjj.baise.gov.cn/zwgk/gzdt/': 4,  # 住建局  工作动态
            'http://zjj.baise.gov.cn/zwgk/tzwj/': 7,  # 住建局  通知文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('百色\t',e)
        driver.close()
        return baise1(name)

# todo   贺州(ij)   公共资源中心 | 发改委 |人民政府 |住建局
def hezhou(name):
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
            'http://ggzyjy.gxhz.gov.cn/gzdt/': 4,  # 公共资源中心  工作动态
            'http://www.gxhz.gov.cn/sy/ywzx/hzyw/': 34,  # 人民政府  贺州要闻
            'http://www.gxhz.gov.cn/sy/ywzx/bmdt/': 33,  # 人民政府 部门动态
            'http://www.gxhz.gov.cn/sy/ywzx/qxdt/': 33,  # 人民政府 区县动态
            'http://www.gxhz.gov.cn/sy/ywzx/ggl/': 2,  # 人民政府 公告栏
            'http://fgw.gxhz.gov.cn/zwgk/fgyw/': 34,  # 发改委 发改要闻
            'http://zjj.gxhz.gov.cn/xwdt/': 6,  # 住建局 新闻动态
            'http://zjj.gxhz.gov.cn/zwgk/zcxx/zcfg/': 1,  # 住建局 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('贺州\t',e)
        driver.close()
        return hezhou(name)


# todo  河池  公共资源中心 |人民政府 |发改委 |住建局
def hechi(name):
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
            'http://www.hcjyxxw.com/gxhczbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001': 4,  # 公共资源中心 工作动态
            'http://www.hcjyxxw.com/gxhczbw/tzgg/MoreInfo.aspx?CategoryNum=008': 3,  # 公共资源中心 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'bsggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@id='morelist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'www' in url and i%6==0:
                 #        pass
                 # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'bsggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('2]/a', "3]") + "/text()")[0].strip().replace(
                                '/', '-').replace('[', '').replace(']', '')

                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace(
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
                                # try:
                                #     driver.find_element_by_xpath("//ul[@class='m-pagination-page']/li[2]/a").click()
                                #     break
                                # except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('»'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
    except Exception as e:
        print('河池\t', e)
        driver.close()
        return hechi(name)
# todo   河池(ij)   发改委 |人民政府 |住建局
def hechi1(name):
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
            'http://www.hechi.gov.cn/zwdt/': 10,  # 人民政府  政务动态
            'http://www.hechi.gov.cn/bmdt_67736/': 5,  # 人民政府  部门动态
            'http://www.hechi.gov.cn/xqdt/': 2,  # 人民政府  县区动态
            'http://www.hechi.gov.cn/zh_67737/': 4,  # 人民政府  综合发布
            'http://www.hechi.gov.cn/tzgg/': 5,  # 人民政府  通知公告
            'http://www.hechi.gov.cn/xxgk/zfhy/': 3,  # 人民政府  政府会议
            'http://www.hechi.gov.cn/xxgk/zfwj/bmwj/': 9,  # 人民政府  部门文件
            'http://www.hechi.gov.cn/gdtt/': 9,  # 人民政府 更多头条
            'http://fgw.hechi.gov.cn/zwdt/': 5,  # 发改委 政务动态
            'http://fgw.hechi.gov.cn/wjgg/xmbjpzjg/': 9,  # 发改委 项目报建批准结果
            'http://fgw.hechi.gov.cn/wjgg/wjgs/': 9,  # 发改委 文件公示
            'http://fgw.hechi.gov.cn/xxgk/zcwj/': 1,  # 发改委 政策文件
            'http://zjj.hechi.gov.cn/zwdt/': 9,  # 住建局 政务动态
            'http://zjj.hechi.gov.cn/gggs/': 9,  # 住建局 公告公示
            'http://zjj.hechi.gov.cn/bmwj/': 8,  # 住建局 部门文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('河池\t',e)
        driver.close()
        return hechi1(name)

# todo  来宾  公共资源中心 |人民政府 |发改委 |住建局
def laibin(name):
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
            'http://ggzyjy.laibin.gov.cn/gxlbzbw/ztbdt/009001/MoreInfo.aspx?CategoryNum=009001': 3,  # 公共资源中心 中心动态
            'http://ggzyjy.laibin.gov.cn/gxlbzbw/tzgg/MoreInfo.aspx?CategoryNum=008': 3,  # 公共资源中心 通知公告
            'http://ggzyjy.laibin.gov.cn/gxlbzbw/zcfg/003006/003006001/MoreInfo.aspx?CategoryNum=003006001': 1,  # 公共资源中心 政策法规

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'bsggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@id='morelist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'www' in url and i%6==0:
                 #        pass
                 # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'bsggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('2]/a', "3]") + "/text()")[0].strip().replace(
                                '/', '-').replace('[', '').replace(']', '')

                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace(
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
                                # try:
                                #     driver.find_element_by_xpath("//ul[@class='m-pagination-page']/li[2]/a").click()
                                #     break
                                # except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('»'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
    except Exception as e:
        print('来宾\t', e)
        driver.close()
        return laibin(name)
# todo   来宾(ij)   发改委 |人民政府 |住建局
def laibin1(name):
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
            'http://www.laibin.gov.cn/xwzx/zwdt/': 24,  # 人民政府  政务动态
            'http://www.laibin.gov.cn/xwzx/qxbd/': 23,  # 人民政府  区县报道
            'http://www.laibin.gov.cn/xwzx/bmdt/': 34,  # 人民政府  部门动态
            'http://www.laibin.gov.cn/xwzx/tzgg/': 22,  # 人民政府  通知公告
            'http://www.laibin.gov.cn/xxgk/zcjd/': 4,  # 人民政府  政策解读
            'http://www.laibin.gov.cn/xxgk/bmwj/': 34,  # 人民政府  部门文件
            'http://www.laibin.gov.cn/xxgk/zfwj/': 13,  # 人民政府  政府文件
            'http://fgw.laibin.gov.cn/zwdt/': 7,  # 发改委  政务动态
            'http://fgw.laibin.gov.cn/tzgg/': 3,  # 发改委  通知公告
            'http://zjj.laibin.gov.cn/zwfw/wjtz/': 4,  # 住建局  文件通知
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('来宾\t',e)
        driver.close()
        return laibin1(name)

# todo  崇左  公共资源中心 |人民政府 |发改委 |住建局
def chongzuo(name):
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
            'http://www.czjyzx.gov.cn/gxczzbw/tzgg/MoreInfo.aspx?CategoryNum=008': 1,  # 公共资源中心 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'bsggzy' in url:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@id='morelist']/ul/li"
                length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'www' in url and i%6==0:
                 #        pass
                 # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/', f'tr[{i}]/td/')
                    if 'bsggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('2]/a', "3]") + "/text()")[0].strip().replace(
                                '/', '-').replace('[', '').replace(']', '')

                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('[', '').replace(']','').replace(
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
                                # try:
                                #     driver.find_element_by_xpath("//ul[@class='m-pagination-page']/li[2]/a").click()
                                #     break
                                # except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('»'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
    except Exception as e:
        print('崇左\t', e)
        driver.close()
        return chongzuo(name)
# todo   崇左(ij)   发改委 |人民政府 |住建局
def chongzuo1(name):
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
            'http://www.chongzuo.gov.cn/zwdt/': 34,  # 人民政府  政务动态
            'http://www.chongzuo.gov.cn/bmdt/': 23,  # 人民政府  部门动态
            'http://www.chongzuo.gov.cn/tzgg/': 13,  # 人民政府  通知公告
            'http://www.chongzuo.gov.cn/xxgk/jcxxgk/zcjd/': 1,  # 人民政府  政策解读
            'http://www.chongzuo.gov.cn/gdtt/': 23,  # 人民政府  更多头条
            'http://fgw.chongzuo.gov.cn/gzdt/': 23,  # 发改委  工作动态
            'http://fgw.chongzuo.gov.cn/tzgg/': 4,  # 发改委  通知公告
            'http://fgw.chongzuo.gov.cn/xxgk/zcjd/': 1,  # 发改委  政策解读
            'http://zjj.chongzuo.gov.cn/zwgk/gzdt/': 10,  # 住建局  工作动态
            'http://zjj.chongzuo.gov.cn/zwgk/tzgg/': 5,  # 住建局  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='morelist']/ul/li"
            xpathj = "//div[@id='morelist']/ul/li[1]"
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
                        xpath1 = xpath.replace('/div/ul/li', f'/div[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('(','').replace(')','').replace('\t','').replace('\r','')
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
        print('崇左\t',e)
        driver.close()
        return chongzuo1(name)


#
# guangxi('广西')
# guangxi1('广西')
# nanning('南宁')
# nanning1('南宁')
# liuzhou('柳州')
guilin('桂林')
wuzhou('梧州')
wuzhou1('梧州')
beihai('北海')
beihai1('北海')
fangchenggang('防城港')
fangchenggang1('防城港')
qinzhou('钦州')
qinzhou1('钦州')
guigang('贵港')
guigang1('贵港')
baise('百色')
baise1('百色')
hezhou('贺州')
hechi('河池')
hechi1('河池')
laibin('来宾')
laibin1('来宾')
chongzuo('崇左')
chongzuo1('崇左')