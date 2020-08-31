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
pro = '广东'


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


# todo  广东  公共资源中心 | 发改委 |人民政府 |住建局
def guangdong(name):
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
            'http://ggzy.gd.gov.cn/gdggzy_important_center_work/index.html': 10,  # 公共资源中心 通知公告 / 中心公告
            'http://ggzy.gd.gov.cn/gdggzy_government_column/zcjd/index.html': 2,  # 公共资源中心 政策解读
            'http://ggzy.gd.gov.cn/gdggzy_important_center_notice/index.html': 2,  # 公共资源中心 通知公告
            'http://www.gd.gov.cn/gdywdt/gdyw/index.html': 88,  # 人民政府 广东要闻
            'http://www.gd.gov.cn/gdywdt/bmdt/index.html': 45,  # 人民政府 部门动态
            'http://www.gd.gov.cn/gdywdt/dsdt/index.html': 42,  # 人民政府 地市动态
            'http://drc.gd.gov.cn/gzyw5618/index.html': 7,  # 发改委 工作动态
            'http://drc.gd.gov.cn/sxdt5619/index.html': 11,  # 发改委 市县动态
            'http://drc.gd.gov.cn/ywgs/index.html': 2,  # 发改委 公告公示 > 业务公示
            'http://drc.gd.gov.cn/ywtz/index.html': 11,  # 发改委 业务通知
            'http://drc.gd.gov.cn/zcjd5635/index.html': 2,  # 发改委 政策解读
            'http://zfcj.gz.gov.cn/zjdt/zjxw/index.html': 20,  # 住建局 住建新闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='viewList']/ul/li/span/a"
            elif 'drc' in url:
                xpath = "//div[@class='gl-cont2 f-r']/ul/li"
            elif 'zfcj' in url:
                xpath = "//div[@class='pageList infoList maxList']/ul/li"
            elif 'gdggzy_government_column' in url or 'gdggzy_important_center_notice' in url:
                xpath = "//div[@class='xxgk_right_con']/ul/li"
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
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a', "[@class='time']") + "/text()")[
                            0].strip().replace('/', '-')
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
        print('广东\t', e)
        driver.close()
        return guangdong(name)


# todo  广州  公共资源中心 | 发改委 |人民政府 |住建局
def guangzhou(name):
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
            'http://ggzy.gz.gov.cn/zxgg/index.jhtml': 10,  # 公共资源中心 通知公告 / 中心公告
            'http://ggzy.gz.gov.cn/gywmxxgkmlzxdt/index.jhtml': 20,  # 公共资源中心 中心动态
            'http://www.gz.gov.cn/xw/gzyw/index.html': 100,  # 人民政府 广州要闻
            'http://www.gz.gov.cn/xw/zwlb/': 64,  # 人民政府 政务联播
            'http://www.gz.gov.cn/xw/jrgz/': 100,  # 人民政府 今日关注
            'http://www.gz.gov.cn/xw/tzgg/': 20,  # 人民政府 通知公告
            'http://fgw.gz.gov.cn/gkmlpt/index': 1,  # 发改委 通知公告
            'http://fgw.gz.gov.cn/tzgg/index.html': 1,  # 发改委 通知公告
            'http://zfcj.gz.gov.cn/zjdt/zjxw/index.html': 20,  # 住建局 住建新闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw.gz.gov.cn/tzgg' in url:
                xpath = "//div[@class='list_li']/ul/li"
            elif 'gkmlpt' in url:
                xpath = "//table[@class='table-content']/tbody/tr/td/a"
            elif 'zfcj' in url:
                xpath = "//div[@class='pageList infoList maxList']/ul/li"
            else:
                xpath = "//table[@class='table public-table procureBulletin-table']/tbody/tr[1]/td[2]/a"
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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/a', f'tr[{i}]/td')
                    if 'ggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]/span") + "/text()")[0].strip().replace(
                            '/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        if 'gkmlpt' in url:
                            publictime = html_1.xpath(xpath1.replace('/a', '[2]') + f"/text()")[0].strip().replace('[',
                                                                                                                   '').replace(
                                ']', '').replace('日', '').replace('/', '-')
                        else:
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('广州\t', e)
        driver.close()
        return guangzhou(name)


# todo  韶关  公共资源中心 | 发改委 |人民政府 |住建局
def shaoguan(name):
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
            'http://jyzx.sg.gov.cn/announcementAction!frontAnnouncementList.do': 15,  # 公共资源中心 通知公告
            'https://www.sg.gov.cn/xw/xwzx/index.html': 20,  # 人民政府 新闻资讯
            'https://www.sg.gov.cn/xw/tzgg/': 15,  # 人民政府 通知公告
            'http://fgj.sg.gov.cn/xwzx/dtxx/index.html': 48,  # 发改委 动态信息
            'http://fgj.sg.gov.cn/xwzx/tzgg/': 7,  # 发改委 通知公告
            'http://fgj.sg.gov.cn/fgzq/zcfg/index.html': 2,  # 发改委 政策法规
            'http://fgj.sg.gov.cn/fgzq/fzgggz/': 9,  # 发改委 发展改革工作
            'http://fgj.sg.gov.cn/zwgk/zcjd/index.html': 4,  # 发改委 政策解读
            'http://zgj.sg.gov.cn/xwzx/gzdt/index.html': 10,  # 住建局 工作动态
            'http://zgj.sg.gov.cn/xwzx/gsgg/': 14,  # 住建局 公示公告
            'http://zgj.sg.gov.cn/xwzx/zcjd//': 2,  # 住建局 公示公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jyzx' in url:
                xpath = '//*[@id="dataList"]/tbody/tr/td[1]'
            elif 'fgj' in url:
                xpath = "//div[@class='fy-right']/ul/li"
            elif 'zgj' in url:
                xpath = "//div[@class='gl-cont-r f-r']/ul/li"
            else:
                xpath = "//div[@class='gl-right']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'jyzx' in url:
                  #       xpathh = xpath.replace('tr/td[', f'tr[{i}]/td[')
                  #
                  # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'ggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]/span") + "/text()")[0].strip().replace(
                            '/', '-')
                    elif 'zgj' in url:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                        '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1 + "/span/text()")[0].strip().replace('/', '-')
                    elif 'www' in url or 'jyzx' in url:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        if 'jyzx' in url:
                            fenlei= html_1.xpath(xpath1.replace('td[1]', 'td[2]') + f"/text()")[0].strip().replace(
                                '[', '').replace(']', '').replace('日', '').replace('/', '-')
                            if fenlei=='建设工程交易':
                                publictime = html_1.xpath(xpath1.replace('td[1]', 'td[3]') + f"/text()")[0].strip().replace(
                                '[', '').replace(']', '').replace('日', '').replace('/', '-')
                            else:
                                publictime=''
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(
                                ']', '').replace('日', '').replace('/', '-')

                    else:
                        href = html_1.xpath(f"{xpath1}/a[2]/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a[2]//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                            '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
                            '日', '').replace('/', '-')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在

                    if select == None:
                        if publictime == '': pass
                        else:
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
        print('韶关\t', e)
        driver.close()
        return shaoguan(name)


# todo  深圳  公共资源中心 | 发改委 |人民政府 |住建局
def shenzhen(name):
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
            'http://ggzy.sz.gov.cn/cn/zcfg/zcfg/szszcfg/index.html': 1,  # 公共资源中心 深圳市政策法规
            'http://ggzy.sz.gov.cn/cn/xyzx/tzgg/index.html': 6,  # 公共资源中心 通知公告
            'http://ggzy.sz.gov.cn/cn/xyzx/gzdt/': 6,  # 公共资源中心 工作动态
            'http://www.sz.gov.cn/cn/xxgk/zfxxgj/zwdt/index.html': 20,  # 人民政府 工作动态
            'http://www.sz.gov.cn/cn/xxgk/zfxxgj/tzgg/index.html': 20,  # 人民政府 通知公告
            'http://fgw.sz.gov.cn/zwgk/qt/tzgg/index.html': 8,  # 发改委 通知公告
            'http://fgw.sz.gov.cn/zwgk/qt/gzdt/index.html': 5,  # 发改委 工作动态
            'http://zjj.sz.gov.cn/xxgk/tzgg/index.html': 12,  # 住建局 通知公告
            'http://zjj.sz.gov.cn/xxgk/gzdt/': 5,  # 住建局 工作动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='tag-list4']/ul/li"
            elif 'fgw' in url:
                xpath = "//div[@class='con']/ul/li/a/span[@class='p_bt']"
            elif 'zjj' in url:
                xpath = "//div[@class='listcontent_right']/ul/li"
            else:
                xpath = "//div[@class='zx_ml_list']/ul/li/span/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i == 1:
                        pass
                    else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/a', f'tr[{i}]/td')
                        if 'www' in url or 'fgw' in url:
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                          '').replace(
                                '\r', '')
                            if 'fgw' in url:
                                href = html_1.xpath(xpath1.replace("/span[@class='p_bt']", "") +"/@href")[0].strip()
                                publictime = html_1.xpath(xpath1.replace('p_bt', "p_sj") + "/text()")[
                                    0].strip().replace('/', '-').replace('日', '').replace('年', '-').replace('月', '-')
                            else:
                                href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                                publictime = html_1.xpath(xpath1.replace('/a', "[3]") + "/text()")[0].strip().replace(
                                    '/', '-').replace('日', '').replace('年', '-').replace('月', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                             '').replace(
                                '\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                                   '').replace(
                                '日', '').replace('年', '-').replace('月', '-').replace('/', '-')
                            if publictime[2:3]=='-':
                                publictime='20'+publictime
                            else:publictime=publictime

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
                                        driver.find_element_by_xpath(
                                            f"//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('深圳\t', e)
        driver.close()
        return shenzhen(name)


# todo  珠海  公共资源中心 | 发改委 |人民政府 |住建局
def zhuhai(name):
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
            'http://ggzy.zhuhai.gov.cn/notices/zxgg/index.jhtml': 3,  # 公共资源中心 中心通知公告
            'http://ggzy.zhuhai.gov.cn/notices/jgbmtzgg/index.jhtml': 1,  # 公共资源中心 监管部门通知公告
            'http://ggzy.zhuhai.gov.cn/policy/jsgclaw/index.jhtml': 1,  # 公共资源中心 建设工程
            'http://www.zhuhai.gov.cn/xw/xwzx/zhyw/index.html': 20,  # 人民政府 珠海要闻
            'http://www.zhuhai.gov.cn/xw/xwzx/bmkx/': 20,  # 人民政府 部门快讯
            'http://www.zhuhai.gov.cn/xw/xwzx/gqdt/': 20,  # 人民政府 各区动态
            'http://www.zhuhai.gov.cn/xw/gsgg/index.html': 20,  # 人民政府 公示公告
            'http://www.zhuhai.gov.cn/zw/fggw/zcjd/bmjd/index.html': 13,  # 人民政府 部门解读
            'http://fgj.zhuhai.gov.cn/zwgk/gzdt/index.html': 8,  # 发改委 工作动态
            'http://fgj.zhuhai.gov.cn/zwgk/tzgg/': 7,  # 发改委 通知公告
            'http://fgj.zhuhai.gov.cn/zwgk/zcjd/index.html': 7,  # 发改委 政策解读
            'http://zjj.zhuhai.gov.cn/zwgk/gzdt/index.html': 11,  # 住建局 工作动态
            'http://zjj.zhuhai.gov.cn/zwgk/tzgg/': 9,  # 住建局 通知公告
            'http://zjj.zhuhai.gov.cn/zwgk/zcfg/zffg/': 1,  # 住建局 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='rl-box-right']/ul/li/a"
            elif 'fgj' in url:
                xpath = "//div[@class='list']/ul/li"
            else:
                xpath = "//div[@class='col-2-2']/ul/li"
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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td/a', f'tr[{i}]/td')
                    if 'ggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1 + "/span/text()")[0].strip().replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']','').replace(
                            '日', '').replace('/', '-')[:10]

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
        print('珠海\t', e)
        driver.close()
        return zhuhai(name)


# todo  汕头  公共资源中心 | 发改委 |人民政府（响应慢） |住建局
def shantou(name):
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
            'https://www.shantou.gov.cn/stsggzyjyzx/zwgk/gzdt/index.html': 3,  # 公共资源中心  工作动态
            'https://www.shantou.gov.cn/stsggzyjyzx/zwgk/tzgg/index.html': 3,  # 公共资源中心  通知公告
            'https://www.shantou.gov.cn/stsggzyjyzx/zwgk/zcfg/index.html': 2,  # 公共资源中心  政策法规
            'https://www.shantou.gov.cn/cnst/ywdt/styw/index.html': 20,  # 人民政府 汕头要闻
            'https://www.shantou.gov.cn/cnst/ywdt/bmdt/index.html': 20,  # 人民政府 部门动态
            'https://www.shantou.gov.cn/cnst/ywdt/qxdt/index.html': 20,  # 人民政府 区县动态
            'https://www.shantou.gov.cn/cnst/ywdt/cwhy/index.html': 2,  # 人民政府 市政府常务会议
            'https://www.shantou.gov.cn/stsfzhggj/zwgk/gzdt/index.html': 20,  # 发改委 工作动态
            'https://www.shantou.gov.cn/stsfzhggj/zwgk/tzgg/index.html': 20,  # 发改委 通知公告
            'https://www.shantou.gov.cn/zjj/zwgk/gzdt/index.html': 20,  # 住建局  工作动态  20
            'https://www.shantou.gov.cn/zjj/zwgk/bszn/index.html': 3,  # 住建局  办事指南
            'https://www.shantou.gov.cn/zjj/zwgk/gggs/index.html': 10,  # 住建局   公告公示
            'https://www.shantou.gov.cn/zjj/zwgk/wjtz/index.html': 10,  # 住建局   文件通知
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zwgk' in url or 'stsfzhggj' in url or 'zjj' in url:
                xpath = "//div[@class='con-right fr']/div/div[@class='list-right_title fon_1']/a"
            elif 'www' in url:
                xpath = "//div[@class='list_right']/ul/li"
            elif 'cwhy' in url:
                xpath = "//div[@class=' wzlm_right ']/ul/li"
            else:
                xpath = "//div[@class='col-2-2']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if page==1:
                    pass
                else:
                    driver.get(url.replace('index.html',f'index_{page}.html'))
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'zwgk' in url or 'stsfzhggj' in url or 'zjj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("div[@class='list-right_title fon_1']/a",
                                                                 'table/tbody/tr/td[1]') + "/text()")[
                            0].strip().replace('/', '-').replace(' ', '').replace('\n', '').replace('发布时间：','')
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
                        publictime_times = int(time.mktime(time.strptime(publictime.replace('    ',''), "%Y-%m-%d")))
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
                    #                 try:
                    #                     driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                    #                 except:
                    #                     driver.find_element_by_xpath(f"//div[@id='page_div']/a[@id='next']").click()
                    #             except:
                    #                 try:
                    #                     driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                    #                 except:
                    #                     driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('下一页'))
                    #     break
    except Exception as e:
        print('汕头\t', e)
        driver.close()
        return shantou(name)


# todo  佛山  公共资源中心 | 发改委 |人民政府（响应慢）
def foshan(name):
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
            'http://ggzy.foshan.gov.cn/zwgk/xwdt/tzgg/index.html': 11,  # 公共资源中心  通知公告
            'http://ggzy.foshan.gov.cn/zwgk/xwdt/zxdt/index.html': 7,  # 公共资源中心  中心动态
            'http://www.foshan.gov.cn/zwgk/zwdt/jryw/index.html': 50,  # 人民政府  今日要闻
            'http://www.foshan.gov.cn/zwgk/zwdt/bmdt/': 50,  # 人民政府  部门动态
            'http://www.foshan.gov.cn/zwgk/zcwj/zcjd/tpjd/index.html': 1,  # 人民政府   政策解读 > 图片解读
            'http://fsdr.foshan.gov.cn/xxgk/tzgg/index.html': 8,  # 发改委   通知公告
            'http://fsdr.foshan.gov.cn/xxgk/zwxw/index.html': 15,  # 发改委   政务新闻
            'http://fsdr.foshan.gov.cn/zmhd/jd/index.html': 1,  # 发改委  政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='ewb-con-bd']/ul/li/div/a"
            elif 'fsdr' in url:
                xpath = "//div[@class='listPageBox']/div/ul/li"
            else:
                xpath = "//div[@class='main-l']/ul/li"
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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'ggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("div/a", 'span') + "/text()")[0].strip().replace('/',
                                                                                                                  '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                               '').replace(
                            '（', '').replace('）', '').replace('/', '-')

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
                                    driver.find_element_by_xpath(f"//span[@class='s3']/a[@class='next']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('佛山\t', e)
        driver.close()
        return foshan(name)


# todo   佛山(ij)   住建局
def foshan1(name):
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

            'http://fszj.foshan.gov.cn/zwgk/gzdt/index.html': 6,  # 住建局 工作动态
            'http://fszj.foshan.gov.cn/zwgk/txgg/': 20,  # 住建局 通知公告
            'http://fszj.foshan.gov.cn/zwgk/zcwj/jsgc/index.html': 1  # 住建局 政策文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='m_right']/ul/li"
            xpathj = "//div[@class='m_right']/ul/li[1]"
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
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('·  ', '').replace('\n',
                                                                                                         '').replace(
                            '\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('.',
                                                                                                                '-').replace(
                            '\t', '').replace('\r', '')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city, xpath1)
                            else:
                                po += 1
                                break
                        if (j - 1) * 5 + i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.find_element_by_xpath("//div[@class='page_1']/div[2]/a[3]").click()
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页'))
    except Exception as e:
        print('佛山\t', e)
        driver.close()
        return foshan1(name)


# todo  江门  公共资源中心 | 发改委 |人民政府（响应慢） |住建局
def jiangmeng(name):
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
            'http://www.jiangmen.gov.cn/bmpd/jmsggzyjyzx/zwgk/zxdt/index.html': 6,  # 公共资源中心  中心动态
            'http://www.jiangmen.gov.cn/bmpd/jmsggzyjyzx/zwgk/tzgg/tzgg/': 3,  # 公共资源中心  通知公告
            'http://www.jiangmen.gov.cn/bmpd/jmsggzyjyzx/zwgk/zcjd/': 1,  # 公共资源中心 政策解读
            'http://www.jiangmen.gov.cn/home/zwyw/index.html': 20,  # 人民政府 政务要闻
            'http://www.jiangmen.gov.cn/home/bmdt/': 20,  # 人民政府 部门动态
            'http://www.jiangmen.gov.cn/home/sqdt/pkzx/index.html': 20,  # 人民政府 区市动态 蓬江资讯
            'http://www.jiangmen.gov.cn/home/sqdt/gxjhzx/': 20,  # 人民政府 区市动态 高新江海资讯
            'http://www.jiangmen.gov.cn/home/sqdt/xhzx/': 20,  # 人民政府 区市动态 新会资讯
            'http://www.jiangmen.gov.cn/home/sqdt/tszx/': 20,  # 人民政府 区市动态 台山资讯
            'http://www.jiangmen.gov.cn/home/sqdt/kpzx/': 20,  # 人民政府 区市动态 开平资讯
            'http://www.jiangmen.gov.cn/home/sqdt/hszx/': 20,  # 人民政府 区市动态 鹤山资讯
            'http://www.jiangmen.gov.cn/home/sqdt/epzx/': 20,  # 人民政府 区市动态 恩平资讯
            'http://www.jiangmen.gov.cn/home/tzgg/index.html': 7,  # 人民政府 通知公告
            'http://www.jiangmen.gov.cn/newzwgk/fggw/bmwj/': 4,  # 人民政府 法规公文 > 部门文件
            'http://www.jiangmen.gov.cn/bmpd/jmsfzhggj/gzdt/index.html': 8,  # 发改委 工作动态
            'http://www.jiangmen.gov.cn/bmpd/jmsfzhggj/gggs/': 16,  # 发改委 公告公示
            'http://www.jiangmen.gov.cn/bmpd/jmsfzhggj/zcwj/': 16,  # 发改委 政策文件
            'http://www.jiangmen.gov.cn/bmpd/jmszfhcxjsj/zwgk/gzdt/index.html': 20,  # 住建局 工作动态
            'http://www.jiangmen.gov.cn/bmpd/jmszfhcxjsj/zwgk/gztg/index.html': 5,  # 住建局 通知公告
            'http://www.jiangmen.gov.cn/bmpd/jmszfhcxjsj/zcfg/zcjd/': 2,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='col-2-2']/ul/li"
            else:
                xpath = "//div[@class='pageList']/ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'zwgk' in url or 'stsfzhggj' in url or 'zjj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("div[@class='list-right_title fon_1']/a",
                                                                 'table/tbody/tr/td[1]') + "/text()")[
                            0].strip().replace('/', '-')
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
        print('江门\t', e)
        driver.close()
        return jiangmeng(name)


# todo  湛江  公共资源中心 | 发改委 |人民政府 |住建局
def zhanjiang(name):
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
            'http://ggzy.zhanjiang.gov.cn/gzdt/index.htm': 3,  # 公共资源中心  工作动态
            'http://ggzy.zhanjiang.gov.cn/tzgg/index.htm': 3,  # 公共资源中心  通知公告
            'http://ggzy.zhanjiang.gov.cn/zcfgJsgc/index.htm': 1,  # 公共资源中心  政策法规
            'https://www.zhanjiang.gov.cn/jryw/rdgz/index.html': 68,  # 人民政府  热点关注
            'https://www.zhanjiang.gov.cn/jryw/csjj/index.html': 8,  # 人民政府  城市聚焦
            'https://www.zhanjiang.gov.cn/jryw/bmsd/index.html': 20,  # 人民政府  部门速递
            'https://www.zhanjiang.gov.cn/jryw/qxdt/index.html': 100,  # 人民政府  区县动态
            'https://www.zhanjiang.gov.cn/xxgk/fggw/zcjd/bmjd/index.html': 12,  # 人民政府  部门解读
            'https://www.zhanjiang.gov.cn/zjfgj/sy/gzdt/index.html': 9,  # 发改委  工作动态
            'https://www.zhanjiang.gov.cn/zjfgj/sy/gggs/index.html': 5,  # 发改委  公告公示
            'https://www.zhanjiang.gov.cn/zjfgj/sy/fzgg/index.html': 20,  # 发改委  发展改革
            'https://www.zhanjiang.gov.cn/zjj/sy/gzdt/index.html': 16,  # 住建局  工作动态
            'https://www.zhanjiang.gov.cn/zjj/sy/gsgg/index.html': 11,  # 住建局  公告公示
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='right-con']/form/ul/li"
            elif 'zjj' in url or 'zjfgj' in url:
                xpath = "//div[@class='col-xs-12 col-md-12 col-lg-12']/ul/li"
            else:
                xpath = "//div[@class='overview_news_gg']/div/div[@class='overview_xq_t']/div/a"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/h1/text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(
                            xpath1.replace("overview_xq_t", 'overview_time').replace("div/a", 'span') + "/text()")[
                            0].strip().replace('/', '-')
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
        print('湛江\t', e)
        driver.close()
        return zhanjiang(name)


# todo  茂名  公共资源中心 | 发改委 |人民政府|住建局
def maoming(name):
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
            'http://ggzy.zhanjiang.gov.cn/gzdt/index.htm': 3,  # 公共资源中心  工作动态
            'http://www.maoming.gov.cn/ywdt/rdyw/index.html': 37,  # 人民政府  热点要闻
            'http://www.maoming.gov.cn/ywdt/bmdt/index.html': 20,  # 人民政府  部门动态
            'http://www.maoming.gov.cn/ywdt/xqdt/index.html': 20,  # 人民政府  县区动态
            'http://www.maoming.gov.cn/zwgk/zcjd/jd/index.html': 2,  # 人民政府  政策解读
            'http://fgj.maoming.gov.cn/zwgk/xxgkml/zwdt/gzdt/index.html': 12,  # 发改委  工作动态
            'http://fgj.maoming.gov.cn/fzgh/tzgg/index.html': 14,  # 发改委  通知公告
            'http://jianshe.maoming.gov.cn/xwdt/gzdt/index.html': 5,  # 住建局  工作动态
            'http://jianshe.maoming.gov.cn/xwdt/zjxw/index.html': 5,  # 住建局  住建新闻
            'http://jianshe.maoming.gov.cn/xwdt/zcjd/index.html': 1,  # 住建局  政策解读
            'http://jianshe.maoming.gov.cn/tzgg/tz/index.html': 2,  # 住建局  通知
            'http://jianshe.maoming.gov.cn/tzgg/gg/index.html': 2,  # 住建局  公告
            'http://jianshe.maoming.gov.cn/tzgg/gs/index.html': 2,  # 住建局  公示
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgj' in url:
                xpath = "//ul/span[@id='lblListInfo']/li/div/a"
            elif 'jianshe' in url:
                xpath = "//div[@class='cleft']/ul/li"
            else:
                xpath = "//div[@class='GcList']//ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'fgj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("/a", '[2]'))[0][:10].strip().replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        if 'jianshe' in url:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']',
                                                                                                                   '').replace(
                                '日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/font/text()")[0].strip().replace('[', '').replace(']',
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
        print('茂名\t', e)
        driver.close()
        return maoming(name)


# todo  肇庆  公共资源中心 | 发改委 |人民政府 |住建局（进不去）
def zhaoqing(name):
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
            'http://ggzy.zhaoqing.gov.cn/zxdt/zxdt/index.html': 4,  # 公共资源中心 中心动态
            'http://ggzy.zhaoqing.gov.cn/zxdt/tzgg/index.html': 4,  # 公共资源中心 通知公告
            'http://ggzy.zhaoqing.gov.cn/zcfg/jsgc/index.html': 1,  # 公共资源中心 政策法规 > 建设工程
            'http://www.zhaoqing.gov.cn/xwzx/zqyw/index.html': 100,  # 人民政府 肇庆要闻
            'http://www.zhaoqing.gov.cn/xwzx/tzgg/index.html': 9,  # 人民政府 通知公告
            'http://www.zhaoqing.gov.cn/xxgk/zcjd/snzc/index.html': 4,  # 人民政府  政策解读 > 市内政策
            'http://www.zhaoqing.gov.cn/xwzx/zwdt/': 30,  # 人民政府  政务动态
            'http://www.zhaoqing.gov.cn/xwzx/bmdt/': 16,  # 人民政府  部门动态
            'http://www.zhaoqing.gov.cn/xwzx/xsqdt/': 30,  # 人民政府  县市区动态
            'http://zjj.zhaoqing.gov.cn/xwdt/rdjj/index.html': 12,  # 住建局  热点聚焦
            'http://zjj.zhaoqing.gov.cn/zwgk/tzgg/index.html': 13,  # 住建局  通知公告
            'http://zjj.zhaoqing.gov.cn/zwgk/zcfg/gfxwj/index.html': 1,  # 住建局  政策法规 > 规范性文件
            'http://zjj.zhaoqing.gov.cn/zwgk/zcfg/bwwj/': 1,  # 住建局  政策法规 >部委文件
            'http://zjj.zhaoqing.gov.cn/zwgk/zcjd/index.html': 1,  # 住建局  政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='column-info-list']/ul/li"
            elif 'zjj' in url:
                xpath = "//div[@class='glc_ccc']/ul/li"
            else:
                xpath = "//div[@class='lm f-l']/ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'fgj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("/a", '[2]') + '/text()')[0][:10].strip().replace('/',
                                                                                                                   '-')
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('肇庆\t', e)
        driver.close()
        return zhaoqing(name)


# todo  惠州  公共资源中心 | 发改委 |人民政府（响应慢） |住建局
def huizhou(name):
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
            'https://zyjy.huizhou.gov.cn/PublicServer/public/backstageManagement/backstageManagement.html?dataType=workNews': 30,
            # 公共资源中心 工作要闻
            'https://zyjy.huizhou.gov.cn/PublicServer/public/backstageManagement/backstageManagement.html?dataType=notice': 4,
            # 公共资源中心 通知公告
            'http://www.huizhou.gov.cn/zwgk/hzsz/zwyw/index.html': 20,  # 人民政府 政务要闻
            'http://www.huizhou.gov.cn/zwgk/hzsz/jgdt/': 20,  # 人民政府 机关动态
            'http://www.huizhou.gov.cn/zwgk/hzsz/xqyw/': 20,  # 人民政府 县区要闻
            'http://jhj.huizhou.gov.cn/zwgk/gzdt/index.html': 20,  # 发改委 工作要闻
            'http://jhj.huizhou.gov.cn/zwgk/bmwj/tzgg/index.html': 9,  # 发改委 通知公告
            'http://jhj.huizhou.gov.cn/zwgk/bmwj/zcfg/index.html': 10,  # 发改委 政策法规
            'http://zjj.huizhou.gov.cn/zwgk/gzdt/index.html': 20,  # 住建局 工作动态
            'http://zjj.huizhou.gov.cn/zwgk/xqdt/index.html': 20,  # 住建局 县区动态
            'http://zjj.huizhou.gov.cn/zmhd/hygq/zcjd/index.html': 1,  # 住建局 政策解读
            'http://zjj.huizhou.gov.cn/zwgk/bmwj/tzgg/index.html': 16,  # 住建局  通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zyjy' in url:
                xpath = "//table/tbody/tr/td[1]/span[@class='hasHover']"
            elif 'jhj' in url or 'zjj' in url:
                xpath = "//td[@id='div_list']/ul/li[@class='li_art_title']"
            else:
                xpath = "//div[@class='artList']/ul/li[@class='li_art_title']"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'zyjy' in url:
                        driver.find_element_by_xpath(f"{xpath1}/a").click()
                        b_handle = driver.current_window_handle  # 获取当前页句柄
                        handles = driver.window_handles  # 获取所有页句柄
                        s_handle = None
                        for handle in handles:
                            if handle != b_handle:
                                s_handle = handle
                        driver.switch_to.window(s_handle)  # 在新窗口操作
                        href = driver.current_url  # 2级页面的url
                        driver.close()
                        driver.switch_to.window(b_handle)  # 在新窗口操作
                        # href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace("[1]/span[@class='hasHover']", '[2]') + '/text()')[
                            0].strip().replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        if 'www' in url or 'jhj' in url or 'zjj' in url:
                            publictime = html_1.xpath(xpath1.replace('li_art_title', 'li_art_date') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('惠州\t', e)
        driver.close()
        return huizhou(name)


# todo  梅州  公共资源中心（进不去） | 发改委 |人民政府 |住建局
def meizhou(name):
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
            'https://www.meizhou.gov.cn/zwgk/zfjg/sggzyjyzx/xwzx/zxdt/index.html': 3,  # 公共资源中心 中心动态
            'https://www.meizhou.gov.cn/zwgk/zfjg/sggzyjyzx/xwzx/tzgg/': 2,  # 公共资源中心 通知公告
            'https://www.meizhou.gov.cn/zwgk/gzdt/zwyw/index.html': 150,  # 人民政府 政务要闻
            'https://www.meizhou.gov.cn/zwgk/gzdt/qxdt/': 98,  # 人民政府 区县动态
            'https://www.meizhou.gov.cn/zwgk/gzdt/bmdt/': 20,  # 人民政府 部门动态
            'https://www.meizhou.gov.cn/hygq/zcjd/mzzc/index.html': 3,  # 人民政府 政策解读 > 梅州政策
            'https://www.meizhou.gov.cn/zwgk/zfjg/sfzhggj/zfxxgkml/gzdt/index.html': 6,  # 发改委 工作动态
            'https://www.meizhou.gov.cn/zwgk/zfjg/sfzhggj/tzgggs/index.html': 8,  # 发改委 通知 公告 公示
            'https://www.meizhou.gov.cn/zwgk/zfjg/szfhcxjsj/zfxxgkml/gzdt/index.html': 8,  # 住建局 工作动态
            'https://www.meizhou.gov.cn/zwgk/zfjg/szfhcxjsj/gsgg/index.html': 5,  # 住建局 公示公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='list-rBox']/ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')

                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    publictime = html_1.xpath(f"{xpath1}/p/text()")[0].strip().replace('[', '').replace(']',
                                                                                                        '').replace('日',
                                                                                                                    '').replace(
                        '/', '-')

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
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('梅州\t', e)
        driver.close()
        return meizhou(name)


# todo  汕尾  公共资源中心（进不去） | 发改委 |人民政府 |住建局(无法访问)
def shanwei(name):
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
            'http://www.shanwei.gov.cn/swdpb/yaowen/tzgg/index.html': 4,  # 发改委 通知公告
            'http://www.shanwei.gov.cn/swsfgj/gkmlpt/index#475': 4,  # 发改委 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'gkmlpt' in url:
                xpath = "//table[@class='table-content']/tbody/tr/td[@class='first-td']/a"
            else:
                xpath = "//div[@class='con-right fr']/div/div[@class='list-right_title fon_1']/a"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')

                        if 'gkmlpt' in url:
                            publictime = html_1.xpath(xpath1.replace("div[@class='list-right_title fon_1']/a",
                                                                     'table/tbody/tr/td[1]') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1.replace("[@class='first-td']/a", '[2]') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']',
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('汕尾\t', e)
        driver.close()
        return shanwei(name)


# todo  汕尾  公共资源中心
def shanwei1(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        url = 'http://www.swggzy.cn/noticesList/getNotices'
        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '87',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'JSESSIONID=271639F69CE56A3A2B9DEC9693F5FCD7; _gscu_1847771377=947094383g4eyd49; _gscbrs_1847771377=1; _gscs_1847771377=94709438nq8rit49|pv:3',
            'Host': 'www.swggzy.cn',
            'Origin': 'http://www.swggzy.cn',
            'Referer': 'http://www.swggzy.cn/noticesList?rootId=fdc5d45849fa4b55be2fc756465ce1c9&columnId=b4865a5c9f724d1997734442b8f6e17a&area=all',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        xpaths = {
            "91abc264173f4a48b0ef34bd908e6959": 3,  # 中心动态
            "b4865a5c9f724d1997734442b8f6e17a": 1,  # 通知公告
        }
        for xpath1, pages in zip(xpaths.keys(), xpaths.values()):

            for page in range(1, pages + 1):
                data = {
                    'area': 'all',
                    'searchTitle': '',
                    'columnId': f'{xpath1}',
                    'pageIndex': f'{page - 1}',
                    'pageSize': '20'
                }
                con = requests.post(url, headers=headers, data=data).content.decode('utf-8')
                conts = json.loads(con)['attributes']['notices']
                for cont in conts:
                    title = cont['title']
                    publictime = cont['releaseTime']
                    href = cont['href']

                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'jxcq' in url:
                                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                link = 'http://www.swggzy.cn' + href
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime,
                                                   url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                            else:
                                chuli1(publictime, href, url, title, city)


    except Exception as e:
        print('汕尾\t', e)
        return shanwei1(name)


# todo  河源  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def heyuan(name):
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
            'http://www.heyuan.gov.cn/ywdt/szxw/index.html': 20,  # 人民政府 时政新闻
            'http://www.heyuan.gov.cn/ywdt/bmdt/index.html': 20,  # 人民政府 部门动态
            'http://www.heyuan.gov.cn/ywdt/xqdt/index.html': 20,  # 人民政府 县区动态
            'http://www.heyuan.gov.cn/ywdt/tzgg/index.html': 14,  # 人民政府 通知公告
            'http://www.heyuan.gov.cn/zwgk/jdhy/zcjd/index.html': 3,  # 人民政府 政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'gkmlpt' in url:
                xpath = "//table[@class='table-content']/tbody/tr/td[@class='first-td']/a"
            else:
                xpath = "//div[@class='tab-cnt-item current']/ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'ee' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')

                        if 'gkmlpt' in url:
                            publictime = html_1.xpath(xpath1.replace("div[@class='list-right_title fon_1']/a",
                                                                     'table/tbody/tr/td[1]') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1.replace("[@class='first-td']/a", '[2]') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']',
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('河源\t', e)
        driver.close()
        return heyuan(name)


# todo  阳江  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def yangjiang(name):
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
            'http://www.yjggzy.cn/Query/ArticleQuery2/9208c89cecda4c5a80baee2c9e3a2141': 1,  # 公共资源中心 最新动态
            'http://www.yjggzy.cn/Query/ArticleQuery2/0be72aef000043c18798d79fd1084181': 1,  # 公共资源中心 政策法规 建设工程
            'http://www.yangjiang.gov.cn/zwgk/ywdt/yjyw/index.html': 100,  # 人民政府 阳江要闻
            'http://www.yangjiang.gov.cn/zwgk/ywdt/bmzx/': 50,  # 人民政府 部门资讯
            'http://www.yangjiang.gov.cn/zwgk/ywdt/xqdt/': 50,  # 人民政府 县区动态
            'http://www.yangjiang.gov.cn/zwgk/ywdt/gggs/': 12,  # 人民政府 公告公示
            'http://www.yangjiang.gov.cn/zwgk/gzwj/zcjd/': 4,  # 人民政府 政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www.yjggzy' in url:
                xpath = "//div[@class='Rbox']/ul/li"
            else:
                xpath = "//div[@class='ty_content_1_co_r_co_1']/ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'ee' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')

                        if 'gkmlpt' in url:
                            publictime = html_1.xpath(xpath1.replace("div[@class='list-right_title fon_1']/a",
                                                                     'table/tbody/tr/td[1]') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1.replace("[@class='first-td']/a", '[2]') + f"/text()")[
                                0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t',
                                                                                                         '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']',
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
                                    driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('阳江\t', e)
        driver.close()
        return yangjiang(name)


# todo  清远  公共资源中心 | 发改委  |人民政府 |住建局
def qingyuan(name):
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
            'https://www.qyggzy.cn/tzggL.jsp': 3,  # 公共资源中心 通知公告
            'http://www.gdqy.gov.cn/gdqy/zxzx/tzgg/index.html': 6,  # 人民政府 通知公告
            'http://www.gdqy.gov.cn/gdqy/zxzx/zwyw/index.html': 20,  # 人民政府 政务要闻
            'http://www.gdqy.gov.cn/gdqy/zxzx/bmdt/index.html': 20,  # 人民政府 政务联播
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qysfzhggj/gzdta/index.html': 9,  # 发改委 工作动态
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qysfzhggj/tzgga/index.html': 12,  # 发改委 通知公告
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qysfzhggj/zwgk/zcfg/index.html': 1,  # 发改委 政策法规
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qyszjj/zwgk/gzdt/index.html': 9,  # 住建局 工作动态
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qyszjj/zwgk/bmwj/': 7,  # 住建局 部门文件
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qyszjj/zwgk/tzgg/index.html': 11,  # 住建局 通知公告
            'http://www.gdqy.gov.cn/xxgk/zzjg/zfjg/qyszjj/zwgk/gsgg/': 2,  # 住建局 公示公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www.qyggzy' in url:
                xpath = "//div[@class='article-content']/ul/li"
            elif 'xxgk' in url:
                xpath = "//div[@class='col-xs-9 col-md-9 col-lg-9']/ul/li"
            else:
                xpath = "//div[@class='pageList']/ul/li"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')

                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    if 'www.qyggzy' in url:
                        publictime = html_1.xpath(xpath1 + f"div/text()")[0].strip().replace('[', '').replace(']',
                                                                                                              '').replace(
                            '日', '').replace('/', '-')
                    else:
                        publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(
                            ']', '').replace('日', '').replace('/', '-')
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
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('清远\t', e)
        driver.close()
        return yangjiang(name)


# todo  东莞  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def dongguan(name):
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
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/GovNews/list?fcGovtype=Notice&noticeType=1&KindIndex=0&noticeType=1&KindIndex=0': 11,
            # 公共资源中心 通知公告
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/GovNews/list?fcGovtype=Notice&noticeType=2&KindIndex=1': 1,
            # 公共资源中心 监督机构公告
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/GovRules/list?fcGovtype=policeRules&fcPoliciesregulationstype=67DC9C9382C9432E81DD2402CC1D32E2': 2,
            # 公共资源中心 政策法规

            'http://www.dg.gov.cn/jjdz/dzyw/index.html': 246,  # 人民政府 东莞要闻
            'http://www.dg.gov.cn/jjdz/xwfb/index.html': 10,  # 人民政府 新闻发布
            'http://www.dg.gov.cn/jjdz/zwgg/index.html': 13,  # 人民政府 政务公告
            'http://www.dg.gov.cn/zwgk/jdhy/zcjd/szfjqbm/index.html': 5,  # 人民政府 政策解读 > 市政府及其部门
            'http://dgdp.dg.gov.cn/gkmlpt/index#22': 10,  # 发改委 工作动态
            'http://dgdp.dg.gov.cn/gkmlpt/index#21': 14,  # 发改委 通知公告
            'http://dgdp.dg.gov.cn/fzgg/index.html': 15,  # 发改委 发展改革
            'http://zjj.dg.gov.cn/gkmlpt/index#797': 9,  # 住建局 工作动态
            'http://zjj.dg.gov.cn/gkmlpt/index#796': 24,  # 住建局 通知公告
            'http://zjj.dg.gov.cn/gkmlpt/index#783': 24,  # 住建局 政策文件

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//table[@id='old_data']/tbody/tr/td[2]/a"
            elif 'fzgg' in url:
                xpath = "//div[@class='con-right fr']/div/div[@class='list-right_title fon_1']/a"
            elif 'dgdp' in url or 'zjj' in url:
                xpath = "//tbody/tr/td[@class='first-td']/a"
            else:
                xpath = "//ul/li/div[@class='sjtp']/div/div/a"

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
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')

                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r',
                        '')
                    if 'ggzy' in url:
                        publictime = html_1.xpath(xpath1.replace('[2]/a', '[3]') + f"/text()")[0].strip().replace('[',
                                                                                                                  '').replace(
                            ']', '').replace('日', '').replace('/', '-')
                    elif 'www' in url:
                        publictime = html_1.xpath(xpath1.replace('div/a', 'span') + f"/text()")[0].strip().replace('[',
                                                                                                                   '').replace(
                            ']', '').replace('日', '').replace('/', '-')
                    elif 'fzgg' in url:
                        publictime = html_1.xpath(xpath1.replace("div[@class='list-right_title fon_1']/a",
                                                                 'table/tbody/tr/td[1]') + f"/text()")[
                            0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    elif 'dgdp' in url or 'zjj' in url:
                        publictime = html_1.xpath(xpath1.replace("@class='first-td']/a", '2]') + f"/text()")[
                            0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(
                            ']', '').replace('日', '').replace('/', '-')
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
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('东莞\t', e)
        driver.close()
        return dongguan(name)

# todo  中山  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def zhongshan(name):
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
            'http://ggzyjy.zs.gov.cn/Application/NewPage/PageSubItem.jsp?node=80': 7,      # 公共资源中心 通知公告
            'http://ggzyjy.zs.gov.cn/Application/NewPage/PageSubItem.jsp?node=81': 6,      # 公共资源中心 中心动态
            'http://ggzyjy.zs.gov.cn/Application/NewPage/PageSubItem.jsp?node=173': 1,      # 公共资源中心 政策解读
            'http://www.zs.gov.cn/zwgk/gzdt/zsyw/index.html': 20,      # 人民政府  中山要闻
            'http://www.zs.gov.cn/zwgk/gzdt/bmdt/index.html': 85,      # 人民政府  部门动态
            'http://www.zs.gov.cn/zwgk/gzdt/zqdt/index.html': 121,      # 人民政府   镇区动态
            'http://www.zs.gov.cn/zwgk/fggw/szfwj/index.html': 10,      # 人民政府   市政府文件
            'http://www.zs.gov.cn/zwgk/gzdt/tzgg/index.html': 18,      # 人民政府    通知公告
            'http://www.zs.gov.cn/fgj/zwdt/index.html': 20,    # 发改委 政务动态
            'http://www.zs.gov.cn/fgj/zcgw/zcjd/': 2,    # 发改委 政策解读
            'http://www.zs.gov.cn/fgj/gggs/': 20,    # 发改委 公告公示
            'http://jsj.zs.gov.cn/xwzx/wzts/index.html': 2,    # 住建局  新闻中心 > 温馨提示
            'http://jsj.zs.gov.cn/xwzx/xwbd/': 23,    # 住建局  新闻中心 > 新闻报道

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy' in url:
                xpath = "//div[@class='nav_list']/ul/li"
            elif 'jsj' in url:
                xpath = "//tbody[@id='gj']/tr/td[2]/div/a"
            else:
                xpath = "//div[@class='section']/ul/li"

            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 if 'fgj' in url and i%5==0:
                    pass
                 else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'jsj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/div/a','[3]/div') + f"/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
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
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('中山\t', e)
        driver.close()
        return zhongshan(name)

# todo  潮州  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def chaozhou(name):
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
            'http://www.czggzy.com/xwdtL.jsp': 4,      # 公共资源中心 工作动态
            'http://www.czggzy.com/tzggL.jsp': 2,      # 公共资源中心 通知公告
            'http://www.czggzy.com/zcfgL.jsp?j=J': 1,      # 公共资源中心 政策法规
            'http://www.chaozhou.gov.cn/ywdt/czyw/': 20,      # 人民政府 潮州要闻
            'http://www.chaozhou.gov.cn/zwgk/zwdt/qsdt/index.html': 8,      # 人民政府 全市动态
            'http://www.chaozhou.gov.cn/zwgk/zwdt/bmdt/': 20,      # 人民政府 部门动态
            'http://www.chaozhou.gov.cn/zwgk/zwdt/qxdt/': 20,      # 人民政府 县区动态
            'http://www.chaozhou.gov.cn/zwgk/gsgg/': 20,      # 人民政府  公示公告
            'http://www.chaozhou.gov.cn/zwgk/szfgz/sfgj/tzgg/': 5,      # 发改委  通知公告
            'http://www.chaozhou.gov.cn/zwgk/szfgz/sfgj/bmwj/': 7,      # 发改委  部门文件
            'http://www.chaozhou.gov.cn/zwgk/szfgz/szfcxjsj/tzgg/': 10,      # 住建局  通知公告
            'http://www.chaozhou.gov.cn/zwgk/szfgz/szfcxjsj/bmdt/': 3,      # 住建局  部门动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'chaozhou' in url:
                xpath = "//ul[@class='ul_news']/li/a"
            else:
                xpath = "//div[@class='article-content']/ul/li"

            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 if 'fgj' in url and i%5==0:
                    pass
                 else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'chaozhou' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/p//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1+ f"b/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'www' in url:
                            publictime = html_1.xpath(xpath1 + f"div/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
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
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('潮州\t', e)
        driver.close()
        return chaozhou(name)

# todo  揭阳  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def jieyang(name):
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
            'http://jysggzy.jieyang.gov.cn/TPFront/xwzx/001002/': 1,      # 公共资源中心 中心动态
            'http://www.jysggzy.com/TPFront/xwzx/001003/': 2,      # 公共资源中心 通知公告
            'http://www.jysggzy.com/TPFront/xwzx/001004/': 1,      # 公共资源中心  图片新闻
            'http://www.jieyang.gov.cn/xwdt/jyxw/index.html': 20,      # 公共资源中心  揭阳新闻
            'http://www.jieyang.gov.cn/xwdt/qxbmdt/': 20,      # 公共资源中心  区县部门动态
            'http://www.jieyang.gov.cn/xwdt/gsgg/': 20,      #   公示公告
            'http://www.jieyang.gov.cn/jyfg/zwgk/gzdt/szyw/index.html': 20,     # 发改委  时政要闻
            'http://www.jieyang.gov.cn/jyfg/zwgk/gzdt/jgzdt/': 4,     # 发改委  局工作动态
            'http://www.jieyang.gov.cn/jyfg/zwgk/zcwj/zcjd/index.html': 1,     # 发改委 政策解读
            'http://www.jieyang.gov.cn/zjj/zwzx/tzgg/': 20,     # 住建局 通知公告
               }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jysggzy' in url:
                xpath = "//div[@class='categorypagingcontent']/div[1]/ul/li/div/a"
            else:
                xpath = "//div[@class='list']/ul/li"

            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 if 'fgj' in url and i%5==0:
                    pass
                 else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[', f'div[{i}]/div[')
                    if 'jysggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a','span')+ f"/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'www' in url:
                            publictime = html_1.xpath(xpath1 + f"div/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
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
                                                              driver.find_element_by_link_text('[下一页]'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('揭阳\t', e)
        driver.close()
        return jieyang(name)

# todo  云浮  公共资源中心（无） | 发改委（无）  |人民政府 |住建局（无）
def yunfu(name):
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
            'http://ggzy.yunfu.gov.cn/yfggzy/ggl/009003/': 3,      # 公共资源中心 工作动态
            'http://ggzy.yunfu.gov.cn/yfggzy/ggl/009002/': 2,      # 公共资源中心 通知公告
            'http://ggzy.yunfu.gov.cn/yfggzy/ggl/009001/': 1,      # 公共资源中心 滚动图片
            'http://www.yunfu.gov.cn/yfsrmzf/jcxxgk/zxzx/zwxw/index.html': 30,      # 人民政府 政务新闻
            'http://www.yunfu.gov.cn/yfsrmzf/jcxxgk/zxzx/tzgg/index.html': 3,      # 人民政府 通知公告
            'http://www.yunfu.gov.cn/yfsrmzf/jcxxgk/zxzx/bmdt/index.html': 20,      # 人民政府 部门动态
            'http://www.yunfu.gov.cn/yfsrmzf/jcxxgk/zxzx/xsqxwlb/index.html': 20,      # 人民政府 县（市、区）新闻联播
            'http://www.yunfu.gov.cn/fgj/zwgk/ztxw/index.html': 9,      # 发改委 专题新闻
            'http://www.yunfu.gov.cn/fgj/zwgk/gggs/index.html': 16,      # 发改委 公告公示
            'http://www.yunfu.gov.cn/fgj/zwgk/gfxwjzcjd/index.html': 2,      # 发改委 规范性文件政策解读
            'http://www.yunfu.gov.cn/zjj/xwzx/index.html': 10,      # 住建局 新闻中心
            'http://www.yunfu.gov.cn/zjj/gsgg/tzgg/index.html': 16,      # 住建局 通知公告
            'http://www.yunfu.gov.cn/zjj/zcfg/zcwj/index.html': 2,      # 住建局 政策文件
            'http://www.yunfu.gov.cn/zjj/zcjd/zcjd/index.html': 1,      # 住建局 政策解读
               }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath = "//div[@class='r-bd border']/ul/li/div/a"
            elif 'yfsrmzf' in url:
                xpath = "//div[@class='bd']/ul/li/h3/a"
            elif 'zjj' in url:
                xpath = "//table[@class='list_table']/tbody/tr/td/div/a"
            else:
                xpath = "//div[@class='ny_right']/div/li"

            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                 # if 'fgj' in url and i%5==0:
                 #    pass
                 # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('/div/li', f'/div/li[{i}]')
                    if 'ggzy' in url or 'yfsrmzf' in url or 'zjj' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'ggzy' in url:
                            publictime = html_1.xpath(xpath1.replace('div/a','span')+ f"/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        elif 'zjj' in url:
                            publictime = html_1.xpath(xpath1.replace('td/div/a','th')+ f"/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1.replace('h3/a','span')+ f"/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'www' in url:
                            publictime = html_1.xpath(xpath1 + f"div/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            publictime = html_1.xpath(xpath1 + f"span/text()")[0].strip().replace('[', '').replace(']', '').replace('日', '').replace('/', '-')
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
                                    driver.find_element_by_xpath(f"//li[@class='next1']/a[@class='next']").click()
                                except:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                        break
    except Exception as e:
        print('云浮\t', e)
        driver.close()
        return yunfu(name)


guangdong('广东省')
guangzhou('广州')

shaoguan('韶关')
shenzhen('深圳')
zhuhai('珠海')
shantou('汕头')
foshan('佛山')
foshan1('佛山')
jiangmeng('江门')
zhanjiang('湛江')
maoming('茂名')
zhaoqing('肇庆')
huizhou('惠州')
meizhou('梅州')
shanwei('汕尾')
shanwei1('汕尾')
heyuan('河源')
yangjiang('阳江')
qingyuan('清远')
dongguan('东莞')
zhongshan('中山')
chaozhou('潮州')
jieyang('揭阳')
yunfu('云浮')
