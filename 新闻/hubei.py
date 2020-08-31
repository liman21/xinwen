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
pro = '湖北'


def chuli(publictime, href, driver, url, title, city, xpath1):
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
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/' + href
        uid = uuid.uuid4()
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
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


# todo  湖北  公共资源中心  |住建局
def hubei(name):
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
            'http://jycg.hubei.gov.cn/fbjd/gzdt/': 36,  # 公共资源中心 工作动态
            'http://jycg.hubei.gov.cn/fbjd/tzgg/': 7,  # 公共资源中心 通知公告
            'http://zjt.hubei.gov.cn/fbjd/dtyw/zjyw/': 50,  # 住建局 住建要闻
            'http://zjt.hubei.gov.cn/fbjd/dtyw/gzdt/': 31,  # 住建局 工作动态
            'http://zjt.hubei.gov.cn/fbjd/dtyw/tzgg/': 73,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jycg' in url:
                xpath = "//div[@class='main list mb20']/ul/li/a"
            else:
                xpath = "//div[@class='list']/ul/li/h4/a"
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
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'jycg' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/h4/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "/p/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1.replace('h4/a','p/span')}/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('湖北\t', e)
        driver.close()
        return hubei(name)
# todo   湖北(ij)   发改委 |人民政府
def hubei1(name):
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
            'https://www.hubei.gov.cn/xxgk/zcjd/': 9,  # 人民政府  部门动态
            'https://www.hubei.gov.cn/zwgk/hbyw/hbywqb/': 50,  # 人民政府  湖北要闻
            'https://www.hubei.gov.cn/xxgk/gsgg/': 2,  # 人民政府  公示公告
            'https://www.hubei.gov.cn/hbfb/bmdt/': 50,  # 人民政府  部门动态
            'http://fgw.hubei.gov.cn/fbjd/dtyw/fgyw/': 24,  # 发改委  发改要闻
            'http://fgw.hubei.gov.cn/fbjd/tzgg/tz/': 9,  # 发改委  通知公告>通知
            'http://fgw.hubei.gov.cn/fbjd/tzgg/gg/': 2,  # 发改委  通知公告>公告
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'www' in url:
                xpath = "//div[@class='container']/div/div/ul/li/a"
            else:
                xpath="//div[@class='lsj-list']/ul/li"
            xpathj = f"{xpath.replace('/a','')}[1]"
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
                        xpath1 = xpath.replace('div/div/ul/li/a', f'div[{j}]/div/ul/li[{i}]').replace('ul/li', f'ul[{j}]/li[{i}]')
                        if 'www' in url:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('.','-').replace('\t','').replace('\r','')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                            title = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/a/i/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('»'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('湖北\t',e)
        driver.close()
        return hubei1(name)

# todo  武汉  公共资源中心  |住建局
def wuhan(name):
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
            'https://www.whzbtb.com/V2PRTS/wz/201311080946010001/tzgg/201804281421120154.html': 2,  # 公共资源中心 通知公告
            'http://www.wuhan.gov.cn/sy/whyw/': 200,  # 公共资源中心 武汉要闻
            'http://www.wuhan.gov.cn/zwgk/tzgg/': 42,  # 人民政府 通知公告
            'http://www.wuhan.gov.cn/zwgk/xxgk/zcjd/': 39,  # 人民政府 政策解读
            'http://fgw.wuhan.gov.cn/xwzx/fgyw/': 34,  # 发改委 发改要闻首页 > 新闻中心 > 发改要闻
            'http://fgw.wuhan.gov.cn/xwzx/gzdt/': 12,  # 发改委 工作动态
            'http://fgw.wuhan.gov.cn/xwzx/tpxw/': 4,  # 发改委 图片新闻
            'http://fgw.wuhan.gov.cn/zwgk/wjzl/zcwj/zcjd/': 2,  # 发改委 政策解读
            'http://fgj.wuhan.gov.cn/zwgk_44/zwdt/gzdt/': 28,  # 住建局 工作动态
            'http://fgj.wuhan.gov.cn/zwgk_44/zwdt/tzgg/': 13,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'whzbtb' in url:
                xpath = "//div[@class='information_release_list_t clear']/ul/li"
            elif 'fgw' in url:
                xpath = "//div[@class='newsList']/ul/li"
            elif 'fgj' in url:
                xpath = "//div[@class='list']/ul/li/h4/a"
            else:
                xpath = "//div[@class='articleList']/ul/li"
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
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'fgj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('h4/a','p/span')+ "/text()")[0].strip().replace('/', '-').replace('\n', '')[:10]
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]
                        try:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        except:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[1].strip().replace('\n', '').replace('[','').replace(
                                ']', '').replace('日', '').replace('/', '-')[:10]
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
        print('武汉\t', e)
        driver.close()
        return wuhan(name)

# todo  黄石  公共资源中心  |住建局
def huangshi(name):
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
            'https://www.hsztbzx.com/front/content/9002001000': 5,  # 公共资源中心 通知公告
            'https://www.hsztbzx.com/front/content/9002002000': 3,  # 公共资源中心 工作动态
            'http://www.huangshi.gov.cn/xwdt/hsyw/': 67,  # 人民政府   黄石要闻
            'http://www.huangshi.gov.cn/xwdt/bmdt/': 60,  # 人民政府   部门动态
            'http://www.huangshi.gov.cn/xwdt/rdgz/': 60,  # 人民政府   热点关注
            'http://www.huangshi.gov.cn/xwdt/xsqdt/': 43,  # 人民政府   县市区动态
            'http://www.huangshi.gov.cn/xxxgk/zwdt/': 15,  # 人民政府   政务动态
            'http://www.huangshi.gov.cn/xxxgk/fdzdgknr/tzgg/index.shtml': 8,  # 人民政府   通知公告
            'http://fgw.huangshi.gov.cn/xwzx/fgyw/': 2,  # 发改委  发改要闻
            'http://fgw.huangshi.gov.cn/xwzx/tzgg/': 7,  # 发改委  通知公告
            'http://fgw.huangshi.gov.cn/xwzx/gzdt/': 8,  # 发改委  工作动态
            'http://zjj.huangshi.gov.cn/index2019/zjdt/zjxw/': 11,  # 住建局  住建新闻
            'http://zjj.huangshi.gov.cn/index2019/xxgk_7967/tzgg_7975/': 7,  # 住建局  通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hsztbzx' in url:
                xpath = "//div[@class='right-content']/ul/li/a"
            elif 'fgw' in url or 'zjj' in url:
                xpath = "//div[@id='op1']/ul/li"
            elif 'fdzdgknr' in url:
                xpath = "//div[@class='news_list1']/ul/li"
            else:
                xpath = "//div[@class='newList']/ul/li"
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
                    if 'www.huangshi' in url:
                        xpath1 = xpath.replace('ul/li', f'ul[{i}]/li')
                    else:
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hsztbzx' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span[1]/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "/span[2]/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        try:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/font/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                        link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/' + href

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            uid = uuid.uuid4()
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('黄石\t', e)
        driver.close()
        return huangshi(name)

# todo  十堰  公共资源中心  |住建局
def shiyan(name):
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
            'http://ggzyjy.shiyan.gov.cn/gzyw/tzgg/': 5,  # 公共资源中心 通知公告
            'http://ggzyjy.shiyan.gov.cn/gzyw/gzdt/': 25,  # 公共资源中心 中心动态
            'http://www.shiyan.gov.cn/ywdt/syyw/': 100,  # 人民政府 十堰要闻
            'http://www.shiyan.gov.cn/ywdt/bmdt/': 100,  # 人民政府 部门动态
            'http://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_tzgg/': 12,  # 人民政府 通知公告
            'http://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_zcjd/': 10,  # 人民政府 政策解读
            'http://fgw.shiyan.gov.cn/xwzx/gzdt/': 25,  # 发改委 工作动态
            'http://fgw.shiyan.gov.cn/xwzx/xsdt/': 7,  # 发改委 县市动态
            'http://fgw.shiyan.gov.cn/xwzx/tzgg/': 2,  # 发改委 通知公告
            'http://fgw.shiyan.gov.cn/zcjd/': 2,  # 发改委 政策解读
            'http://zjw.shiyan.gov.cn/xwzx/cjdt/': 10,  # 住建局 城建动态
            'http://zjw.shiyan.gov.cn/xwzx/tzgg/': 7,  # 住建局 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy' in url:
                xpath = "//div[@class='list_cloumn']/ul/li/h2/a"
                length = len(html_2.xpath(xpath)) + 1
            elif 'xxgk' in url:
                xpath = "//div[@class='border p-3 xxgk-content overflow-auto']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'zjw' in url:
                xpath = "//div[@class='col9']/ul/li"
                length = len(html_2.xpath(xpath))
            elif 'fgw' in url:
                xpath = "//div[@class='col-left pd_l10 mb20']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath = "//div[@class='card bg-light my-3']/a/div/h5"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('fgw' in url or 'zjw' in url ) and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    if 'ggzyjy' in url:
                        xpath1 = xpath.replace(']/ul/', f'][{i}]/ul/')
                    else:
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'ggzyjy' in url:
                        href = html_1.xpath(f"/html/body/div[6]/div[2]/div[1]/div[{i}]/@onclick")[0].strip().replace("window.location.href=",'').replace("'",'')
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('h2/a','span')+ "/text()")[0].strip().replace('日期：', '').replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '')
                    elif 'www.shiyan' in url and 'xxgk' not in url:
                        href = html_1.xpath(f"{xpath1.replace('/div/h5','')}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('h5','small')+ "/text()")[0].strip().replace('日期：', '').replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('日期：', '').replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('十堰\t', e)
        driver.close()
        return shiyan(name)


# todo  宜昌  公共资源中心  |住建局
def yichang(name):
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
            'http://ggzyjyzx.yichang.gov.cn/xwzh/001003/about.html': 19,  # 公共资源中心 工作动态
            'http://ggzyjyzx.yichang.gov.cn/zcfg/004002/about.html': 1,  # 公共资源中心 工程建设
            'http://www.yichang.gov.cn/list-164-1.html': 376,  # 人民政府 政务动态
            'http://www.yichang.gov.cn/list-184-1.html': 68,  # 人民政府 公示公告
            'http://www.yichang.gov.cn/list-166-1.html': 50,  # 人民政府 重要新闻
            'http://www.yichang.gov.cn/list-43026-1.html': 6,  # 人民政府 本地决策解读
            'http://fgw.yichang.gov.cn/list-39406-1.html': 6,  # 发改委 发展改革动态
            'http://fgw.yichang.gov.cn/list-39427-1.html': 15,  # 发改委 通知公告
            'http://zj.yichang.gov.cn/list-41740-1.html': 15,  # 住建局 工作要闻
            'http://zj.yichang.gov.cn/list-52145-1.html': 13,  # 住建局 通知公告
            'http://zj.yichang.gov.cn/list-55807-1.html': 11,  # 住建局 基层动态

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjyzx' in url:
                xpath = "//div[@class='ewb-col-bd']/ul/li/div/a"
                length = len(html_2.xpath(xpath)) + 1
            elif 'fgw' in url:
                xpath = "//div[@id='lb_news']/ul/li/span[1]/a"
                length = len(html_2.xpath(xpath)) + 1
            elif 'zj' in url:
                xpath = "//div[@class='default_pgContainer']/ul/li/a"
                length = len(html_2.xpath(xpath)) *2

            else:
                xpath = "//div[@id='test103_14']/ul/li/h1/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            if 'zj' in url:
                step = 2
            else:
                step = 1
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length,step):
                  if ('fgw' in url or 'zjw' in url ) and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'ggzyjyzx' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')[:10]
                    elif 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[1]/a','[2]')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')[:10]
                    elif 'www' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('h1/a','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')[:10]
                    else:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        if 'zj' in url:
                            publictime = html_1.xpath(f"{xpath.replace('ul/li', f'ul/li[{i+1}]').replace('/a','')}/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]
                        else:
                            publictime = html_1.xpath(f"{xpath1.replace('/a','[2]')}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('宜昌\t', e)
        driver.close()
        return yichang(name)

# todo   襄阳(ij)   发改委 |人民政府
def xiangyang(name):
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
            'http://jyzx.xiangyang.gov.cn/xwzx/': 15,  # 公共资源中心  新闻资讯
            'http://jyzx.xiangyang.gov.cn/xwzx/gzdt/': 8,  # 公共资源中心  工作动态
            'http://jyzx.xiangyang.gov.cn/xwzx/tzgg/': 4 , # 公共资源中心  通知公告
            'http://www.xiangyang.gov.cn/zxzx/zxgg/': 7,  # 人民政府  最新公告
            'http://www.xiangyang.gov.cn/zxzx/bmdt/': 33,  # 人民政府  部门动态
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'jyzx' in url:
                xpath = "//article[@class='list-page']/ul/li"
            else:
                xpath="//div[@class='article_left_content1 useDiv']/ul/li"
            xpathj = f"{xpath.replace('/a','')}[1]"
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
                        xpath1 = xpath.replace('div/div/ul/li/a', f'div[{j}]/div/ul/li[{i}]').replace('ul/li', f'ul[{j}]/li[{i}]')
                        if 'jyzx' in url:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}/time/text()")[0].strip().replace('\n','').replace('.','-').replace('\t','').replace('\r','')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('襄阳\t',e)
        driver.close()
        return xiangyang(name)
# todo  襄阳  公共资源中心  |住建局
def xiangyang1(name):
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
            'http://fgw.xiangyang.gov.cn/gzdt/fgyw/': 50,  # 发改委 发改动态
            'http://fgw.xiangyang.gov.cn/gzdt/xsqdt/': 18,  # 发改委 县市区动态
            'http://fgw.xiangyang.gov.cn/gzdt/ttxw/': 3,  # 发改委 头条新闻
            'http://fgw.xiangyang.gov.cn/zwgk/xxgkml/gsgg/': 3,  # 发改委 通知公告
            'http://szjj.xiangyang.gov.cn/zxzx/jsdt/': 30,  # 住建局 工作动态

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//div[@class='tow_list']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath = "//div[@class='card bg-light my-3']/a/div/h5"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('fgw' in url ) and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'ggzyjy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('h2/a"','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('襄阳\t', e)
        driver.close()
        return xiangyang1(name)

# todo  鄂州  公共资源中心
def ezhou(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        # chromeOptions = webdriver.ChromeOptions()
        # chromeOptions.add_experimental_option('w3c', False)
        # chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        # driver = webdriver.Chrome(options=chromeOptions,
        #                           executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        # driver.maximize_window()
        #
        # urls = {
        #
        #
        # }

        for page in range(1, 4):
            url = f'http://www.ezggzy.cn/tongzhigonggao/queryTongZhiGongGaoPagination.do?biaoti=&caidanbh=1&page={page}&rows=8'  # 公共资源中心 通知公告
            data={
                'biaoti':'' ,
                'caidanbh': '1',
                'page': '2',
                'rows': '8'
            }
            con=requests.get(url).content.decode('utf-8')
            conts=json.loads(con)['rows']
            for cont in conts:
                guid=cont['tongZhiGuid']
                link=f'http://www.ezggzy.cn/tongzhigonggao/tzgg_view.html?guid={guid}'
                title=cont['title']
                publictime=cont['faBuStartDate']
                select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在
                #
                if select == None:
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        uid = uuid.uuid4()
                        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                           biaoti=title, tianjiatime=insertDBtime, zt='0')
                        print(f'--{city}-【{title}】写入成功')



            # lengt = len(html_1.xpath(xpath))
            # xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
            # if 'ggzyjy' in url:
            #     href = html_1.xpath(f"{xpath1}/@href")[0].strip()
            #     title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
            #         '\r', '')
            #     publictime = html_1.xpath(xpath1.replace('h2/a"','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
            # else:
            #     href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
            #     title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
            #     publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]
            #
            # select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在
            #
            # if select == None:
            #     publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
            #     # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
            #     if publictime_times >= jiezhi_time:
            #         if 'jxcq' in url:
            #             insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #             link = 'http://www.jxcq.org' + href
            #             uid = uuid.uuid4()
            #             Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime,
            #                                url=link,
            #                                biaoti=title, tianjiatime=insertDBtime, zt='0')
            #             print(f'--{city}-【{title}】写入成功')
            #         else:
            #             chuli(publictime, href, driver, url, title, city, xpath1)
            #     else:
            #         po += 1
            #         break
            # if i == lengt:
            #     if lengt < length - 1:
            #         break
            #     else:
            #         if page != pages:
            #             try:
            #                 driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
            #             except:
            #                 try:
            #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
            #                 except:
            #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
            #     break
    except Exception as e:
        print('鄂州\t', e)
        driver.close()
        return ezhou(name)
# todo   鄂州(ij)   发改委 |人民政府 |住建局
def ezhou1(name):
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
            'http://www.ezhou.gov.cn/sy/ezyw/': 50,  # 人民政府  鄂州要闻
            'http://www.ezhou.gov.cn/sy/qjdt/': 50,  # 人民政府  地方动态
            'http://www.ezhou.gov.cn/sy/bmdt/': 50,  # 人民政府  部门动态
            'http://fgw.ezhou.gov.cn/xwzx_1411/gzdt_1412/': 9,  # 发改委  工作动态
            'http://fgw.ezhou.gov.cn/xwzx_1411/tzgg_1413/': 3,  # 发改委  通知公告
            'http://cjw.ezhou.gov.cn/zxzx/gzdt/': 8,  # 住建局  工作动态
            'http://cjw.ezhou.gov.cn/zxzx/gsgg/': 13,  # 住建局  公示公告
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='ztzl-two-right']/div/ul/li"
            xpathj = f"{xpath.replace('/a','')}[1]"
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
                        xpath1 = xpath.replace('div/ul/li', f'div[{j}]/ul/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('鄂州\t',e)
        driver.close()
        return ezhou1(name)

# todo  荆门  公共资源中心  |住建局
def jingmen(name):
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
            'http://zyjy.jingmen.gov.cn/gzdt/002001/level.html': 3,  # 公共资源中心 本地动态
            'http://zyjy.jingmen.gov.cn/tzgg/level.html': 2,  # 公共资源中心 通知公告
            'http://zyjy.jingmen.gov.cn/zcfg/005002/level.html': 1,  # 公共资源中心 政策法规
            'http://www.jingmen.gov.cn/col/col438/index.html?uid=8548&pageNum=1': 20,  # 人民政府 荆门要闻  230
            'http://www.jingmen.gov.cn/col/col4816/index.html?uid=8548&pageNum=1': 13,  # 人民政府 公示公告
            'http://www.jingmen.gov.cn/col/col439/index.html?uid=8548&pageNum=1': 20,  # 人民政府 县市动态  90
            'http://www.jingmen.gov.cn/col/col440/index.html?uid=8548&pageNum=1': 30,  # 人民政府 部门动态
            'http://fgw.jingmen.gov.cn/col/col3163/index.html': 6,  # 发改委 发展动态
            'http://fgw.jingmen.gov.cn/col/col3164/index.html': 3,  # 发改委 通知公告
            'http://zfhcxjsj.jingmen.gov.cn/col/col4032/index.html': 7,  # 住建局 工作动态
            'http://zfhcxjsj.jingmen.gov.cn/col/col4552/index.html': 8,  # 住建局 通知公告
            'http://zfhcxjsj.jingmen.gov.cn/col/col4237/index.html': 12,  # 住建局 系统动态

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zyjy' in url:
                xpath = "//div[@class='em-infos']/ul/li/a"
            elif 'fgw' in url:
                xpath = "//div[@id='26146']/div/li"
            elif 'zfhcxjsj' in url:
                xpath = "//div[@id='28976']/div/li"
            else:
                xpath = "//div[@class='lucidity_pgContainer']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if 'www.jingmen' in url :
                    if page==1:
                        pass
                    else:
                        driver.get(url.replace('pageNum=1',f'pageNum={page}'))
                        time.sleep(2)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('fgw' in url ) and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'zyjy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span[1]//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "/span[2]/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                    if 'www.jingmen' in url:
                        pass
                    else:
                     if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                try:
                                    driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('荆门\t', e)
        driver.close()
        return jingmen(name)

# todo  孝感  公共资源中心  |住建局
def xiaogan(name):
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
            'http://xn.xgsggzy.com/xnweb/zhyw/071001/': 2,  # 公共资源中心 工作动态
            'http://xn.xgsggzy.com/xnweb/zhyw/071002/': 1,  # 公共资源中心 重要通知
            'http://www.xiaogan.gov.cn/xgyw/index.jhtml': 117,  # 人民政府 孝感要闻
            'http://www.xiaogan.gov.cn/bmdh/index.jhtml': 209,  # 人民政府 部门导航
            'http://xgfgw.xiaogan.gov.cn/gzdt01/index.jhtml': 7,  # 发改委 工作动态
            'http://xgfgw.xiaogan.gov.cn/gsgg01/index.jhtml': 3,  # 发改委 公示公告
            'http://xgfgw.xiaogan.gov.cn/ghjh/index.jhtml': 1,  # 发改委 规划计划
            'http://xgscxjswyh.xiaogan.gov.cn/xjxw/index.jhtml': 25,  # 住建局 孝建新闻
            'http://xgscxjswyh.xiaogan.gov.cn/xsdt/index.jhtml': 10,  # 住建局 县市动态
            'http://xgscxjswyh.xiaogan.gov.cn/tzgg/index.jhtml': 17,  # 住建局 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='list-content']/ul/li"
            elif 'xgscxjswyh' in url:
                xpath = "//div[@id='bodyTab21']/ul/li/div/a"
            elif 'xgfgw' in url:
                xpath = "//div[@class='list-news ']/ul/li"
            else:
                xpath = "//div[@class='categorypagingcontent']/div[1]/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if ('fgw' in url ) and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'xgscxjswyh' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a','[2]')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                                    driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('孝感\t', e)
        driver.close()
        return xiaogan(name)

# todo  荆州  公共资源中心 |发改委  | 住建局
def jingzhou(name):
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
            'http://www.jzggzy.com/xwzh/001001/moreinfo.html': 1,  # 公共资源中心 新闻快讯
            'http://www.jzggzy.com/xwzh/001002/moreinfo.html': 2,  # 公共资源中心 工作动态
            'http://www.jzggzy.com/xwzh/001003/moreinfo.html': 2,  # 公共资源中心 通知公告
            'http://fgw.jingzhou.gov.cn/xxdt/dtyw/': 25,  # 发改委 动态要闻
            'http://fgw.jingzhou.gov.cn/fbjd_14/tzgg/': 4,  # 发改委 通知公告
            'http://zjj.jingzhou.gov.cn/xwzx/dtyw/': 30,  # 住建局  动态要闻
            'http://zjj.jingzhou.gov.cn/xwzx/xtdt/': 31,  # 住建局  系统动态
            'http://zjj.jingzhou.gov.cn/xxgk/xxgkml/tzgg/': 31,  # 住建局  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fbjd_14' in url or 'xxgkml' in url:
                xpath = "//div[@class='article-box jiedu-list']/ul/li"
            elif 'fgw' in url or 'zjj' in url:
                xpath = "//div[@class='con_r_mav con_li']/ul/li"
            else:
                xpath = "//div[@class='ewb-right-info']/div[2]/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if ('fgw' in url ) and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'xgscxjswyh' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a','[2]')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                                if 'moreinfo' in url:
                                    try:
                                        driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.find_element_by_xpath( f"//li[@class='ewb-page-li ewb-page-hover'][2]/a").click()
                                else:
                                    try:
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()

                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('荆州\t', e)
        driver.close()
        return jingzhou(name)
# todo   荆州(ij)   人民政府
def jingzhou1(name):
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
            'http://www.jingzhou.gov.cn/zfwxw/jzyq/': 25,  # 人民政府  荆州要情
            'http://www.jingzhou.gov.cn/zfwxw/bmdt/': 25,  # 人民政府  部门动态
            'http://www.jingzhou.gov.cn/zfwxw/xsqdt/': 25,  # 人民政府  县市区动态
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='fr public-r']/ul/li"
            xpathj = f"{xpath.replace('/a','')}[1]"
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

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/b/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('荆州\t',e)
        driver.close()
        return jingzhou1(name)

# todo  黄冈  公共资源中心
def huanggang(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        #
        urls = {
             f'http://www.hgggzy.com/ceinwz/wxfirst.ashx?newsid=21&FromUrl=xwdt_gg':3,  # 公共资源中心 通知公告
             f'http://www.hgggzy.com/ceinwz/wxfirst.ashx?num=5&newsid=139&FromUrl=gzdt':3,  # 公共资源中心 工作动态

        }

        for url,pages in zip(urls.keys(),urls.values()):
          for page in range(1,pages+1):

            data={
                'k': 'getnewsList',
                'pageIndex': f'{page-1}',
                'pageCount': '10',
                'KW':'',
            }
            con=requests.post(url,data=data).content.decode('gbk')
            conts=json.loads(con)['newslist']
            for cont in conts:
                link='http://www.hgggzy.com/ceinwz/hgweb/'+cont['url']
                title=cont['title']
                publictime=cont['pubdate'][:10]
                select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在
                #
                if select == None:
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        uid = uuid.uuid4()
                        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                           biaoti=title, tianjiatime=insertDBtime, zt='0')
                        print(f'--{city}-【{title}】写入成功')



            # lengt = len(html_1.xpath(xpath))
            # xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
            # if 'ggzyjy' in url:
            #     href = html_1.xpath(f"{xpath1}/@href")[0].strip()
            #     title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
            #         '\r', '')
            #     publictime = html_1.xpath(xpath1.replace('h2/a"','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
            # else:
            #     href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
            #     title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
            #     publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]
            #
            # select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在
            #
            # if select == None:
            #     publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
            #     # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
            #     if publictime_times >= jiezhi_time:
            #         if 'jxcq' in url:
            #             insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            #             link = 'http://www.jxcq.org' + href
            #             uid = uuid.uuid4()
            #             Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime,
            #                                url=link,
            #                                biaoti=title, tianjiatime=insertDBtime, zt='0')
            #             print(f'--{city}-【{title}】写入成功')
            #         else:
            #             chuli(publictime, href, driver, url, title, city, xpath1)
            #     else:
            #         po += 1
            #         break
            # if i == lengt:
            #     if lengt < length - 1:
            #         break
            #     else:
            #         if page != pages:
            #             try:
            #                 driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
            #             except:
            #                 try:
            #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
            #                 except:
            #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
            #     break
    except Exception as e:
        print('黄冈\t', e)
        driver.close()
        return huanggang(name)
# todo  黄冈  公共资源中心 |发改委  | 住建局
def huanggang1(name):
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
            'http://www.hg.gov.cn/col/col13617/index.html?number=A00002A00004': 5,  # 人民政府 政策解读
            'http://www.hg.gov.cn/col/col36/index.html': 5,  # 人民政府 公示公告
            'http://www.hg.gov.cn/col/col30/index.html': 127,  # 人民政府 黄冈要闻
            'http://www.hg.gov.cn/col/col32/index.html': 201,  # 人民政府 部门动态
            'http://www.hg.gov.cn/col/col33/index.html': 326,  # 人民政府 县市新闻
            'http://fgw.hg.gov.cn/col/col14966/index.html': 13,  # 发改委 发改要闻
            'http://fgw.hg.gov.cn/col/col14967/index.html': 13,  # 发改委 县市动态
            'http://fgw.hg.gov.cn/col/col14968/index.html': 2,  # 发改委 通知公告
            'http://fgw.hg.gov.cn/col/col14976/index.html': 1,  # 发改委 政策解读
            'http://zjw.hg.gov.cn/col/col9926/index.html': 17,  # 住建局 住建要闻
            'http://zjw.hg.gov.cn/col/col9927/index.html': 7,  # 住建局 县市区动态
            'http://zjw.hg.gov.cn/col/col9928/index.html': 12,  # 住建局 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = '//*[@id="18070"]/div/table/tbody/tr/td/table/tbody/tr/td[1]/a'
            elif 'fgw' in url:
                xpath = "//div[@id='15619']/div/li"
            elif 'zjw' in url:
                xpath = "//div[@class='list']/ul/li"
            else:
                xpath = "//div[@id='8181']/div/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('www' in url ) and i==1:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('dy/tr/td/table', f'dy/tr[{i}]/td/table')
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[1]/a','[2]')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('黄冈\t', e)
        driver.close()
        return huanggang(name)

# todo  咸宁  公共资源中心 |发改委  | 住建局
def xianning(name):
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
            'http://xnztb.xianning.gov.cn/xnweb/tzgg/': 1,  # 公共资源中心 通知公告
            'http://fgw.xianning.gov.cn/zwdt/gzdt/': 8,  # 发改委 工作动态
            'http://fgw.xianning.gov.cn/zwdt/tzgg/': 3,  # 发改委 通知公告
            'http://fgw.xianning.gov.cn/xxgk/zcjd/': 1,  # 发改委 政策解读
            'http://zjj.xianning.gov.cn/xwdt/jsdt/': 13,  # 住建局 建设动态
            'http://zjj.xianning.gov.cn/xwdt/xssm/': 7,  # 住建局 县市扫描
            'http://zjj.xianning.gov.cn/xxgk/wjtz/': 5,  # 住建局 文件通知
            'http://zjj.xianning.gov.cn/xxgk/zcwj/': 1,  # 住建局 政策文件
            'http://zjj.xianning.gov.cn/xxgk/zcjd/': 1,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'xnztb' in url:
                xpath = "//div[@class='s-tt-bd']/div[1]/table/tbody/tr/td[2]/a"
            elif 'zjj' in url:
                xpath = "//div[@class='list_list m15 bg01']/ul/li"
            else:
                xpath = "//div[@class='concon p10 m15 bshadow2']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if ('fgw' in url ) and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'xnztb' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a','[3]/font')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('咸宁\t', e)
        driver.close()
        return xianning(name)
# todo   咸宁(ij)   人民政府
def xianning1(name):
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
            'http://www.xianning.gov.cn/xwzx/xnyw/': 28,  # 人民政府  咸宁市
            'http://www.xianning.gov.cn/xwzx/xnsz/': 25,  # 人民政府  部门动态
            'http://www.xianning.gov.cn/xwzx/xssm/': 28,  # 人民政府  县市扫描
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='xwlb-content']/div/ul/li"
            xpathj = f"{xpath}[1]"
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
                        xpath1 = xpath.replace('div/ul/li', f'div[{j}]/ul/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/span/em//text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/i/em//text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('咸宁\t',e)
        driver.close()
        return xianning1(name)

# todo   随州(ij)   人民政府
def suizhou(name):
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
            'http://www.suizhou.gov.cn/xwdt/szyw/': 20,  # 人民政府  随州要闻
            'http://www.suizhou.gov.cn/xwdt/bmdt/': 20,  # 人民政府  部门动态
            'http://www.suizhou.gov.cn/xwdt/xqdt/': 20,  # 人民政府  县市区（管委会）动态
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='news-list']/ul/li"
            xpathj = f"{xpath}[1]"
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

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/div//text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('随州\t',e)
        driver.close()
        return suizhou(name)
# todo  随州  公共资源中心 |发改委、住建局（无）
def suizhou1(name):
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
            'http://www.hbbidcloud.cn/suizhou/tzgg/about.html': 1,  # 公共资源中心 通知公告


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hbbidcloud' in url:
                xpath = "//div[@class='ewb-info-bd']/ul/li/div/a"
            else:
                xpath = "//div[@class='news-list xxgk-list']/ul/li/div/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if ('fgw' in url ) and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hbbidcloud' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('随州\t', e)
        driver.close()
        return suizhou1(name)

# todo   恩施(ij)   公共资源中心 |发改委  |住建局
def enshi(name):
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
            'http://ggzy.enshi.gov.cn/tzgg/': 3,  # 公共资源中心  通知公告
            'http://ggzy.enshi.gov.cn/zhxx/': 6,  # 公共资源中心  综合信息
            'http://ggzy.enshi.gov.cn/zcfg/': 1,  # 公共资源中心  政策法规
            'http://fgw.enshi.gov.cn/zfgw/zxdt/fgyw/': 9,  # 发改委  发改要闻
            'http://fgw.enshi.gov.cn/zfgw/xxgk/tzgg/': 3,  # 发改委  通知公告
            'http://fgw.enshi.gov.cn/zfgw/zcfg/': 1,  # 发改委  政策法规
            'http://zjw.enshi.gov.cn/zzjw/jszx/': 5,  # 住建局  建设资讯
            'http://zjw.enshi.gov.cn/zzjw/gsgg/': 13,  # 住建局  公示公告
            'http://zjw.enshi.gov.cn/zzjw/bmwj/': 2,  # 住建局  部门文件
            'http://zjw.enshi.gov.cn/zzjw/xslb/': 2,  # 住建局  县市联播
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@id='list_article']/ul/li"
            xpathj = f"{xpath}[1]"
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

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')[:10]
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('恩施\t',e)
        driver.close()
        return enshi(name)
# todo  恩施  人民政府
def enshi1(name):
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
            'http://www.enshi.gov.cn/xw/esxw/': 50,  # 人民政府 恩施新闻
            'http://www.enshi.gov.cn/zc/zcjd/': 5,  # 人民政府 政策解读


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'enshi' in url:
                xpath = "//div[@id='lists']/ul/li"
            else:
                xpath = "//div[@class='news-list xxgk-list']/ul/li/div/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('enshi' in url ) and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'suizhou' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('恩施\t', e)
        driver.close()
        return enshi1(name)

# todo  仙桃  公共资源中心|人民政府
def xiantao(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                       Object.defineProperty(navigator, 'webdriver', {
                           get: () => undefined
                       });
                      """
        })
        driver.maximize_window()
        urls = {
            'http://www.xtggzy.com/NewsTrends/Index?ind_code=11&rid=bc132e2d-2ce7-4604-a2f7-838ecbb7532a': 1,  # 公共资源中心 工作动态
            'http://www.xtggzy.com/NewsTrends/Index?ind_code=21&rid=1af9e142-7743-499e-b2ee-388ad91b10e4': 2,  # 公共资源中心 通知公告
            'http://www.xiantao.gov.cn/zwgk/xtyw/index.shtml': 1,  # 人民政府 仙桃要闻
            'http://www.xiantao.gov.cn/zwgk/bmdt/index.shtml': 1,  # 人民政府 部门动态
            'http://www.xiantao.gov.cn/zwgk/zbdt/index.shtml': 1,  # 人民政府 镇办动态
            'http://www.xiantao.gov.cn/zwgk/tpxw/index.shtml': 1,  # 人民政府 图片新闻
            'http://fgw.xiantao.gov.cn/xw/fgyw/index.shtml': 9,  # 发改委 发改要闻
            'http://fgw.xiantao.gov.cn/xw/tpxw/index.shtml': 3,  # 发改委 图片新闻
            'http://fgw.xiantao.gov.cn/xw/tzgg/index.shtml': 5,  # 发改委 通知公告
            'http://zjw.xiantao.gov.cn/gzdt/index.shtml': 4,  # 住建局 工作动态
            'http://zjw.xiantao.gov.cn/zcjd/index.shtml': 1,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'xtggzy' in url:
                xpath = "//div[@class='container-body']/ul/li"
            elif 'fgw' in url:
                xpath = "//div[@class='right fr']/ul/li"
            else:
                xpath = "//div[@class='gl_list1']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if page==1:
                    pass
                else:
                    driver.get(url.replace('index.shtml',f'index_{page-1}.shtml'))
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('enshi' in url ) and i%6==0:
                        pass
                  else:
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'suizhou' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a','span')+ "/text()")[0].strip().replace('日', '').replace('月', '-').replace('年', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

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
                    #                 driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                    #             except:
                    #                 try:
                    #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                    #                 except:
                    #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                    #     break
    except Exception as e:
        print('仙桃\t', e)
        driver.close()
        return xiantao(name)
# import requests.packages.urllib3.util.ssl_
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'
def xiantao1():
    url='http://www.xiantao.gov.cn/zwgk/xtyw/index_1.shtml'
    headers={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'FSSBBIl1UgzbN7N80S=aRlSy37JJeuEAhfP.lALY9E6KwfBhBWbpozp4YMEnQ9eOT8Xl1TN.pIybUeKLRxF; _trs_uv=kcu8awxt_3221_kf0x; _trs_ua_s_1=kdik4trz_3221_8ggg; Hm_lvt_ff67159502e9baa4a1f21cabdf1b5d22=1595232602,1596703661; Hm_lpvt_ff67159502e9baa4a1f21cabdf1b5d22=1596704218;',
        'Host': 'www.xiantao.gov.cn',
        'Referer': 'http://www.xiantao.gov.cn/zwgk/xtyw/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
    }
    con=requests.get(url,headers=headers).content.decode('utf-8')
    print('fdesf')
# xiantao1()

# todo  天门  公共资源中心 | 发改委
def tianmen(name):
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
            'http://ztb.tianmen.gov.cn/News/xwdt/tzgg': 8,  # 公共资源中心 最新通知
            'http://www.tianmen.gov.cn/zwgk/bmhxzxxgkml/bm/sfzhggwyh/gzdt/': 3,  # 发改委 工作动态
            'http://www.tianmen.gov.cn/zwgk/bmhxzxxgkml/bm/sfzhggwyh/bmwj/': 1,  # 发改委 部门文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ztb' in url:
                xpath = "//div[@class='newslist']/ul/li/a"
            elif 'fgw' in url:
                xpath = "//div[@class='right fr']/ul/li"
            else:
                xpath = "//div[@class='gl_list1']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if ('enshi' in url ) and i%6==0:
                        pass
                  else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'ztb' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span[1]/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+ "/span[2]/text()")[0].strip().replace('/', '-').replace('年', '-').replace('\n', '').replace('发布时间：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('天门\t', e)
        driver.close()
        return tianmen(name)
# todo   天门(ij)   人民政府  |住建局
def tianmen1(name):
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
            'http://www.tianmen.gov.cn/xwzx/tmxw/': 50,  # 人民政府  天门新闻
            'http://www.tianmen.gov.cn/xwzx/tzgg/': 33,  # 人民政府  通知公告
            'http://www.tianmen.gov.cn/xwzx/jcdt/': 151,  # 人民政府  基层动态
            'http://www.hbjsgov.com/xxgk_list/12.html': 2,  # 住建局  基层动态
            'http://www.hbjsgov.com/xxgk_list/30.html': 1,  # 住建局  住建部动态
            'http://www.hbjsgov.com/xxgk_list/31.html': 1,  # 住建局  部门动态
            'http://www.hbjsgov.com/xxgk_list/32.html': 1,  # 住建局  市县动态
            'http://www.hbjsgov.com/xxgk_list/15.html': 1,  # 住建局  市县动态

            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'hbjsgov' in url:
                xpath="//div[@class='l1']/ul/li"
            else:
                xpath = "//div[@class='gl_list1']/ul/li"
            xpathj = f"{xpath}[1]"
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
                    if 'hbjsgov' in url:
                        xpathi = f"{xpath.replace(']/ul/li', f'][{j}]/ul/li')}"
                    else:
                        xpathi = f"{xpath.replace('ul/li', f'ul[{j}]/li')}"
                    ii = len(html_1.xpath(xpathi)) + 1
                    for i in range(1, ii):
                        lengt = len(html_2.xpath(xpath))
                        if 'hbjsgov' in url:
                            xpath1 = xpath.replace(']/ul/li', f'][{j}]/ul/li[{i}]')
                        else:
                            xpath1 = xpath.replace('ul/li', f'ul[{j}]/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        if 'hbjsgov' in url:
                            publictime = html_1.xpath(f"{xpath1}/div/text()")[0].strip().replace('\n', '').replace('.','-').replace(']','').replace('[','').replace('\t', '').replace('\r', '')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('天门\t',e)
        driver.close()
        return tianmen1(name)

# todo  潜江  公共资源中心 |住建局
def qianjiang(name):
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
            'http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=1&pageNumber=1&orderBy=id&orderType=desc': 4,  # 公共资源中心 政务信息
            'http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=22&pageNumber=1&orderBy=id&orderType=desc': 2,  # 公共资源中心 公告通知
            'http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=3&pageNumber=1&orderBy=id&orderType=desc': 1,  # 公共资源中心 政策法规
            'http://qjjcj.gov.cn/cxgzdt/index.html': 3,  # 住建局 工作动态
            'http://qjjcj.gov.cn/cxzcjd/index.html': 1,  # 住建局 政策及政策解读
            'http://qjjcj.gov.cn/cxbmwj/index.html': 2,  # 住建局 本部门文件


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'qjggzy' in url:
                xpath = "//div[@id='noHasChildContent']/div/div/a"
            else:
                xpath = "//div[@class='infoList-listSub infoList-listThreeLevel']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if page==1:
                    pass
                else:
                    driver.get(url.replace('pageNumber=1',f'pageNumber={page}').replace('index.html',f'index_{page}.html'))

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if ('enshi' in url ) and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[').replace('div/div', f'div[{i}]/div')
                    if 'qjggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a','[2]')+ "/text()")[0].strip().replace('/', '-').replace('年', '-').replace('\n', '').replace('发布时间：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

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
                    #                 xy = "//td[contains(string(),'下页')]"
                    #                 driver.find_element_by_xpath(xy).click()
                    #             except:
                    #                 try:
                    #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页> '))
                    #                 except:
                    #                     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                    #     break
    except Exception as e:
        print('潜江\t', e)
        driver.close()
        return qianjiang(name)
# todo   潜江(ij)   发改委 |人民政府
def qianjiang1(name):
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
            'http://www.hbqj.gov.cn/xwzx/jrqj/qjyw/': 34,  # 人民政府  潜江要闻
            'http://www.hbqj.gov.cn/xxgk/xxgkml/szfxxgkml/zcjzcjd/': 34,  # 人民政府  政策解读
            'http://fgw.hbqj.gov.cn/gzdt/': 4,  # 发改委  工作动态
            'http://fgw.hbqj.gov.cn/gsgg/': 2,  # 发改委  公示公告
            'http://fgw.hbqj.gov.cn/bbmwj/': 3,  # 发改委  本部门文件
            'http://fgw.hbqj.gov.cn/zcjzcjd/': 1,  # 发改委 政策及政策解读

            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'xwzx' in url:
                xpath="//div[@class='fr xcNero ldSec']/div[2]/div/ul/li"
            elif 'fgw' in url:
                xpath="//div[@class='side-right fr']/div[2]/div/ul/li"
            else:
                xpath = "//div[@class='mar-T20']/ul/li"
            xpathj = f"{xpath}[1]"
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
                        xpath1 = xpath.replace('div/ul/li', f'div[{j}]/ul/li[{i}]').replace(']/ul/li', f']/ul[{j}]/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ', '').replace('\n','').replace('\t', '').replace('\r', '')
                        if 'zcjzcjd' in url:
                            publictime = html_1.xpath(f"{xpath1}/span[2]/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('.','-').replace('\t', '').replace('\r', '')
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
                                                              driver.find_element_by_link_text('>'))
                                        # driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('潜江\t',e)
        driver.close()
        return qianjiang(name)

# todo  神农架  公共资源中心 |发改委 |人民政府 |住建局（无）
def shennongjia(name):
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
            'http://ggzy.zhsnj.cn/xxgk.jsp?urltype=egovinfo.EgovTreeURl&wbtreeid=1004&type=egovinfodeptsubcattree&sccode=gzdt&subtype=1&dpcode=ggzy&gilevel=1': 1,  # 公共资源中心 工作动态
            'http://ggzy.zhsnj.cn/xxgk.jsp?urltype=egovinfo.EgovTreeURl&wbtreeid=1004&type=egovinfodeptsubcattree&sccode=tzgg&subtype=1&dpcode=ggzy&gilevel=1': 1,  # 公共资源中心 通知公告
            'http://ggzy.zhsnj.cn/xxgk.jsp?urltype=egovinfo.EgovTreeURl&wbtreeid=1004&type=egovinfodeptsubcattree&sccode=WJ_&subtype=1&dpcode=ggzy&gilevel=1': 1,  # 公共资源中心 政策法规
            'http://www.snj.gov.cn/xwzx/zwyw/': 72,  # 人民政府 政务要闻
            'http://www.snj.gov.cn/xwzx/bmdt/': 72,  # 人民政府 部门动态
            'http://www.snj.gov.cn/xwzx/gsgg/': 50,  # 人民政府  公示公告
            'http://fgw.zhsnj.cn/fgdt.htm': 4,  # 发改委  发改动态
            'http://fgw.zhsnj.cn/xxgk.jsp?urltype=egovinfo.EgovTreeURl&wbtreeid=1004&type=egovinfodeptsubcattree&sccode=tzgg&subtype=1&dpcode=8a8a8a811bb18738011bb1951dc40001&gilevel=1': 1,  # 发改委  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='col-news-con']/ul/li"
            elif 'www' in url:
                xpath = "//div[@class='ld_right_sider fr mar-T30']/div/div/a/h2"
            else:
                xpath = "//div[@class='col-news-con']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if ('enshi' in url ) and i%6==0:
                  #       pass
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[').replace('div/div', f'div[{i}]/div')
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1.replace('/h2','')}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/h2',"/p[@class='mar-T10']")+ "/text()")[0].strip().replace('/', '-').replace('年', '-').replace('日', '').replace('月', '-').replace('\n', '').replace('日期：', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('【', '').replace('】','').replace('日', '').replace('/', '-')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                        break
    except Exception as e:
        print('神农架\t', e)
        driver.close()
        return shennongjia(name)

def shennongjia1():
    city='神农架'
    url1='http://fgw.zhsnj.cn/fgdt.htm' # 发改委  发改动态
    for page in range(10,0,-1):
        if page==10:
           url=url1
        else:
           url=url1.replace('.htm',f'/{page}.htm')
        headers={'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
                }
        cont=requests.get(url,headers=headers).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
        cons=re.findall('<A class="news-title" href="(.*?)">(.*?)</A> <SPAN class="news-date">(.*?)</SPAN>',cont)
        for con in cons:
            href=con[0]
            link='http://fgw.zhsnj.cn/'+href
            title=con[1]
            publictime=con[2]
            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
            if select == None:
                publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                if publictime_times >= jiezhi_time:
                    uid = uuid.uuid4()
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                       biaoti=title, tianjiatime=insertDBtime, zt='0')

                    print(f'--{city}-【{title}】写入成功')


hubei('湖北')
hubei1('湖北')
wuhan('武汉')
huangshi('黄石')
shiyan('十堰')
yichang('宜昌')
xiangyang('襄阳')
xiangyang1('襄阳')
ezhou('鄂州')
ezhou1('鄂州')
jingmen('荆门')
xiaogan('孝感')
jingzhou('荆州')
jingzhou1('荆州')
huanggang('黄冈')
huanggang1('黄冈')
xianning('咸宁')
xianning1('咸宁')
suizhou('随州')
suizhou1('随州')
enshi('恩施')
enshi1('恩施')
xiantao('仙桃')
tianmen('天门')
tianmen1('天门')
qianjiang('潜江')
qianjiang1('潜江')
shennongjia1()
shennongjia('神农架')