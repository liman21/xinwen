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
pro = '新疆'

def chuli(publictime,href,driver,url,title,city,xpath1):
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

# todo  新疆  公共资源中心 | 发改委 |人民政府 |住建局
def xinjiang(name):
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
            'http://zwfw.xinjiang.gov.cn/xinjiangggzy/zwgk/002004/tradingCommon.html': 2,  # 公共资源中心  通知公告
            'http://zwfw.xinjiang.gov.cn/xinjiangggzy/fwzn/004001/tradingCommon.html': 2,  # 公共资源中心  政策法规
            'http://www.xinjiang.gov.cn/xinjiang/xjyw/common_list.shtml': 2,  # 人民政府  政务动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zwfw' in url:
                xpath="//div[@class='ewb-con-bd']/table/tbody/tr/td/a"
                length = len(html_2.xpath(xpath)) + 2
                ii=2
            else:
                xpath = "//li/div/div[@class='contitle']/a"
                length = len(html_2.xpath(xpath)) + 1
                ii = 1
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace("//li/div/div[@class='contitle']/a",f"//li[{i}]/div[@class='coninfo']/div/a").replace('tr/td/a', f'tr[{i}]/td')
                        if 'www' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1.replace('/a','/span')+"/text()")[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('新疆\t', e)
        driver.close()
        return xinjiang(name)

# todo  乌鲁木齐  公共资源中心|人民政府  | （无）发改委 、住建局
def wulumuqui(name):
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
            'http://zwfw.xinjiang.gov.cn/xinjiangggzy/zwgk/002004/tradingCommon.html': 2,  # 公共资源中心  通知公告
            'http://www.urumqi.gov.cn/info/iList.jsp?cat_id=10005': 86,  # 人民政府  乌鲁木齐要闻
            'http://www.urumqi.gov.cn/info/iList.jsp?cat_id=12034': 59,  # 人民政府  自治区要闻
            'http://www.urumqi.gov.cn/info/iList.jsp?cat_id=12115': 61,  # 人民政府  通知公告
            'http://www.urumqi.gov.cn/info/iList.jsp?cat_id=10006': 2,  # 人民政府  政策解读
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zwfw' in url:
                xpath="//div[@class='ewb-colu-bd']/div/ul/li/div"
                length = len(html_2.xpath(xpath)) + 2
                ii=2
            else:
                xpath = "//ul[@class='commonList_dot am-padding-top-sm am-padding-bottom-0 commonList_dot_Listnews']/li"
                length = len(html_2.xpath(xpath)) + 1
                ii = 1
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace(']/li', f']/li[{i}]')
                        if 'zwfw' in url:
                            href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/div/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1+"/span/text()")[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('乌鲁木齐\t', e)
        driver.close()
        return wulumuqui(name)

# todo  克拉玛依   人民政府  | （无）公共资源中心、发改委 、住建局
def kelamayi(name):
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
            'https://www.klmy.gov.cn/002/002002/secondpage.html': 23,  # 人民政府  自治区要闻
            'https://www.klmy.gov.cn/002/002003/secondpage.html': 30,  # 人民政府  市政要闻
            'https://www.klmy.gov.cn/002/002004/secondpage.html': 11,  # 人民政府  重要公告
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@id='list']/ul/li"
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace(']/li', f']/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/div/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/div/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1+"/span/text()")[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')


                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                break
    except Exception as e:
        print('克拉玛依\t', e)
        driver.close()
        return kelamayi(name)

# todo  吐鲁番   人民政府  | （无）公共资源中心、发改委 、住建局
def tulufan(name):
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
            'http://www.tlf.gov.cn/ztlm/tlfxw.htm': 35,  # 人民政府  吐鲁番新闻
            'http://www.tlf.gov.cn/ztlm/gsggtz.htm': 19,  # 人民政府  公示公告通知
            'http://www.tlf.gov.cn/ztlm/xsdt.htm': 16,  # 人民政府  >县区动态
            'http://www.tlf.gov.cn/ztlm/bmdt.htm': 12,  # 人民政府  >部门动态
            'http://www.tlf.gov.cn/ztlm/jnwxw.htm': 21,  # 人民政府  疆内外新闻




            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)

            xpath="//table[@class='winstyle11251']/tbody/tr"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i%5==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath+f'[{i}]'

                        href = html_1.xpath(f"{xpath1}/td[2]/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/td[2]/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/td[3]/span/text()")[0].strip().replace('/', '-')

                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('吐鲁番\t', e)
        driver.close()
        return tulufan(name)

# todo  哈密   人民政府  | （无）公共资源中心、发改委 、住建局
def hami(name):
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
            'http://www.hami.gov.cn/zxzx/zwgz.htm': 54,  # 人民政府  要闻动态
            'http://www.hami.gov.cn/zxzx/gggs.htm': 14,  # 人民政府  通知公告

            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)

            xpath = "//div[@class='about_right_font']/ul/li"
            length = len(html_2.xpath(xpath))+1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%5==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('/', '-').replace('[', '').replace(']', '')

                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('哈密\t', e)
        driver.close()
        return hami(name)

# todo  阿勒泰   人民政府  | （无）公共资源中心、发改委 、住建局
def aletai(name):
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
            'http://www.alt.gov.cn/zwxx/001003/listPage.html': 436,  # 人民政府  自治区要闻
            'http://www.alt.gov.cn/zwxx/001001/listPage.html': 47,  # 人民政府  政务动态
            'http://www.alt.gov.cn/zwxx/001004/listPage.html': 20,  # 人民政府  乡镇场动态
            'http://www.alt.gov.cn/zwxx/001005/listPage.html': 32,  # 人民政府  部门动态
            'http://www.alt.gov.cn/zwxx/001006/listPage.html': 5,  # 人民政府  公示公告

            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)

            xpath = "//div[@class='ewb-pl20']/ul/li"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%5==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')

                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('阿勒泰\t', e)
        driver.close()
        return aletai(name)



xinjiang('新疆')
wulumuqui('乌鲁木齐')
kelamayi('克拉玛依')
tulufan('吐鲁番')
hami('哈密')
aletai('阿勒泰')