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
pro = '内蒙'

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

# todo  内蒙  公共资源中心 | 发改委 |人民政府 |住建局
def neimeng(name):
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
            'http://ggzyjy.nmg.gov.cn/newsInfo/getInfoNewsList': 5,  # 公共资源中心  通知公告
            'http://ggzyjy.nmg.gov.cn/newsInfo/getWorkNewsList': 3,  # 公共资源中心  工作动态
            'http://ggzyjy.nmg.gov.cn/newsInfo/mszx': 5,  # 公共资源中心  盟市风采
            'http://www.nmg.gov.cn/col/col365/index.html': 46,  # 人民政府  今日关注  166
            'http://www.nmg.gov.cn/col/col151/index.html': 73,  # 人民政府  部门动态
            'http://www.nmg.gov.cn/col/col152/index.html': 207,  # 人民政府  地区动态
            'http://www.nmg.gov.cn/col/col360/index.html': 11,  # 人民政府  通知公告
            'http://fgw.nmg.gov.cn/xxgk/zxzx/tzgg/': 38,  # 人民政府  通知公告
            'http://fgw.nmg.gov.cn/xxgk/zxzx/qqfgwdt/': 46,  # 人民政府  发改动态
            'http://zjt.nmg.gov.cn/website/main/channel.aspx?fcol=101005': 33,  # 住建局  通知公告
            'http://zjt.nmg.gov.cn/website/main/channel.aspx?fcol=101002': 11,  # 住建局  建设新闻
            'http://zjt.nmg.gov.cn/website/main/channel.aspx?fcol=101011': 17,  # 住建局  盟市动态
            'http://zjt.nmg.gov.cn/website/main/channel.aspx?fcol=101010': 12,  # 住建局  厅工作动态


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy' in url:
                xpath="//div[4]/table/tbody/tr/td[@class='text_left']"
                length = len(html_2.xpath(xpath)) + 2
                ii=2
                g = 1
            elif 'fgw' in url:
                xpath="//table[3]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr/td[1]"
                length = len(html_2.xpath(xpath)) + 1
                ii=1
                g = 3
            elif 'zjt' in url:
                xpath="//div[@class='m']/div/ul/li"
                length = len(html_2.xpath(xpath)) +1
                ii=1
                g=1
            else:
                xpath = '//*[@id="6425"]/div/div/div[1]/a'
                length = len(html_2.xpath(xpath)) + 1
                ii = 1
                g = 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(ii, length,g):
                    # if 'www' in url and i%6==0:
                    #     pass
                    # else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('div/div[1]', f'div[{i}]/div[1]').replace('tr/td[@', f'tr[{i}]/td[@').replace('table/tbody/tr/td[1]', f'table[{i}]/tbody/tr/td[1]')
                        if 'www' in url :
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1.replace('[1]/a','[2]/div[2]')+"/text()")[0].strip().replace('/', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            try:
                                title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/font/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            if 'ggzyjy' in url:
                                publictime = html_1.xpath(xpath1.replace("[@class='text_left']",'')+"[3]/text()")[0].strip().replace('/', '-')

                            elif 'fgw' in url:
                                publictime = html_1.xpath(xpath1.replace('td[1]','td[2]')+"/text()")[0].strip().replace('/', '-')

                            else:
                                publictime = html_1.xpath(f"{xpath1}/u/text()")[0].strip().replace('/', '-')

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
                                            driver.find_element_by_xpath(f"//tbody/tr/td[8]/a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('内蒙\t', e)
        driver.close()
        return neimeng(name)


# todo  呼和浩特  公共资源中心 | 发改委 |人民政府 |住建局
def huhehaote(name):
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
            'http://ggzy.huhhot.gov.cn/hsweb/011/011001/011001001/MoreInfo.aspx?CategoryNum=011001001': 5,  # 公共资源中心  通知公告
            'http://ggzy.huhhot.gov.cn/hsweb/011/011002/MoreInfo.aspx?CategoryNum=011002': 2,  # 公共资源中心  工作动态
            'http://ggzy.huhhot.gov.cn/hsweb/011/011006/MoreInfo.aspx?CategoryNum=011006': 5,  # 公共资源中心  图片新闻
            'http://www.huhhot.gov.cn/zwdt/zwyw/': 67,  # 公共资源中心  政务要闻
            'http://www.huhhot.gov.cn/zwdt/bmdt/': 67,  # 公共资源中心  部门动态
            'http://www.huhhot.gov.cn/zwdt/qxqdt/': 67,  # 公共资源中心  旗县区动态
            'http://www.huhhot.gov.cn/zwgk/tzgg/': 10,  # 公共资源中心  通知公告
            'http://zfcxjsj.huhhot.gov.cn/zjdt/ywdt/': 63,  # 住建局  业务动态
            'http://zfcxjsj.huhhot.gov.cn/zwgk_91/tzgg/': 38,  # 住建局  通知公告
            'http://zfcxjsj.huhhot.gov.cn/zwgk_91/bmhy/': 1,  # 住建局  部门会议
            'http://zfcxjsj.huhhot.gov.cn/zwgk_91/zcjd/': 1,  # 住建局  政策解读

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath="//div[@id='right']/table[2]/tbody/tr/td[2]/a"
            elif 'zfcxjsj' in url:
                xpath="/html/body/div[4]/div/div[2]/ul/li/div[1]"
            else:
                xpath = "//div[@class='rightcontent_box']/ul/li"
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
                        if 'ggzy' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+"/text()")[0].strip().replace('/', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            try:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/font/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            if 'zfcxjsj' in url:
                                publi= html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/', '-')
                                publictime=re.findall('发布日期：(.*?) ',publi)[0]
                            else:
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
        print('呼和浩特\t', e)
        driver.close()
        return huhehaote(name)

# todo   呼和浩特(ij)   住建局
def huhehaote1(name):
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
            'http://fgw.huhhot.gov.cn/fgdt/fgdt_4447/': 30,  # 发改委  发改动态
            'http://fgw.huhhot.gov.cn/fgdt/tzgg/': 5,  # 发改委  通知公告
            'http://fgw.huhhot.gov.cn/zwdt/ssxw/': 23,  # 发改委  时事新闻
            'http://fgw.huhhot.gov.cn/zwdt/wztt/': 19,  # 发改委  网站头条
            'http://fgw.huhhot.gov.cn/swgk/zwgk/zcjd/': 3,  # 发改委  政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='WuNavBot']/ul/li"
            xpathj = "//div[@class='WuNavBot']/ul/li[1]"
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
                        href = html_1.xpath(f"{xpath1}/h3/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/h3/a//text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/em/text()")[0].strip().replace('\n','').replace('.','-').replace('\t','').replace('\r','')
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
        print('呼和浩特\t',e)
        driver.close()
        return huhehaote1(name)


# todo  包头  公共资源中心 | 发改委 |人民政府 |住建局
def baotou(name):
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
            'https://www.btggzyjy.cn/zxdt/secondPage.html': 31,  # 公共资源中心  中心动态
            'http://www.baotou.gov.cn/zxzx/ttxw1.htm': 31,  # 人民政府  热点关注
            'http://www.baotou.gov.cn/zxzx/jrbt.htm': 183,  # 人民政府  今日包头
            'http://www.baotou.gov.cn/zxzx/qxqgz.htm': 233,  # 人民政府  旗县区工作
            'http://www.baotou.gov.cn/zxzx/bmdt.htm': 233,  # 人民政府  部门动态




        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'baotou' in url:
                xpath="//div[@class='hdjl_listright']/div/a"
            else:
                xpath = "//div[@class='ewb-span15 ewb-ml20']/ul/li"
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace(']/div/a', f']/div[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-')

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
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                break
    except Exception as e:
        print('包头\t', e)
        driver.close()
        return baotou(name)

# todo  乌海  公共资源中心 | 发改委 |人民政府 |住建局
def wuhai(name):
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
            'http://www.whggzy.com/PurchaseAdvisory/ImportantNotice/index.html?utm=sites_group_front.2ef5001f.0.0.25a9da60c4b311eab7dc85d69c51c6ce': 2,  # 公共资源中心 重要通知
            'http://www.whggzy.com/PurchaseAdvisory/WorkDynamics/index.html?utm=sites_group_front.2ef5001f.0.0.25a9da60c4b311eab7dc85d69c51c6ce': 2,  # 公共资源中心 工作动态
            'http://www.whggzy.com/PurchaseAdvisory/MostImportant/index.html?utm=sites_group_front.2ef5001f.0.0.25a9da60c4b311eab7dc85d69c51c6ce': 1,  # 公共资源中心 网站头条
            'http://www.wuhai.gov.cn/wuhai/whyw75/whyw12/index.html': 106,  # 人民政府 乌海要闻
            'http://www.wuhai.gov.cn/wuhai/whyw75/bmdt/index.html': 129,  # 人民政府 部门动态
            'http://www.wuhai.gov.cn/wuhai/whyw75/zzqyw/index.html': 20,  # 人民政府 自治区要闻
            'http://www.wuhai.gov.cn/wuhai/xxgk4/jbxxgk46/tzgg48/index.html': 6,  # 人民政府 公示公告
            'http://www.wuhai.gov.cn/wuhai/xxgk4/jbxxgk46/813695/index.html': 4,  # 人民政府 政策解读
            'http://fgw.wuhai.gov.cn/fgw/507589/507595/index.html': 16,  # 发改委 发改动态
            'http://fgw.wuhai.gov.cn/fgw/507589/507597/index.html': 1,  # 发改委 通知公告
            'http://fgw.wuhai.gov.cn/fgw/507589/rdgz13/whs/index.html': 35,  # 发改委 热点关注 > 乌海市
            'http://fgw.wuhai.gov.cn/fgw/507589/rdgz13/598344/index.html': 1,  # 发改委 热点关注 > 自治区
            'http://zjw.wuhai.gov.cn/site/news/tznews': 9,  # 住建局 通知公告
            'http://zjw.wuhai.gov.cn/site/news/gsnews': 3,  # 住建局 公示信息
            'http://zjw.wuhai.gov.cn/site/news/gznews': 3,  # 住建局 工作动态

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'whggzy' in url:
                xpath="//div[@class='list-container']/ul/li"
            elif 'fgw' in url:
                xpath="//div[@id='conRight']/div/div[2]/ul/li"
            elif 'zjw' in url:
                xpath="//div[@class='publicList']/ul/li/h3/a"
            else:
                xpath = "//div[@id='b556f83431b54e01bff8a482baea3021']/div[2]/ul/li"
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]')
                        if 'zjw' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1.replace('h3/a','h4/span[2]')+"/text()")[0].strip().replace('/', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-')

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
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('乌海\t', e)
        driver.close()
        return wuhai(name)

# todo  赤峰  公共资源中心 | 发改委 |人民政府 |住建局
def chifeng(name):
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
            'http://ggzy.chifeng.gov.cn/EpointWeb_CF/gzdt_cf/': 2,  # 公共资源中心 工作动态
            'http://ggzy.chifeng.gov.cn/EpointWeb_CF/tzgg_cf/': 3,  # 公共资源中心 通知公告
            'http://www.chifeng.gov.cn/channels/4.html': 69,  # 人民政府 赤峰要闻
            'http://www.chifeng.gov.cn/channels/5.html': 74,  # 人民政府 部门动态
            'http://www.chifeng.gov.cn/channels/6.html': 241,  # 人民政府 旗县动态
            'http://www.chifeng.gov.cn/channels/7.html': 8,  # 人民政府 通知公告
            'http://www.chifeng.gov.cn/channels/24.html': 8,  # 人民政府 政策文件
            'http://fgw.chifeng.gov.cn/dtzx/fgdt/': 22,  # 发改委 发改动态
            'http://fgw.chifeng.gov.cn/dtzx/tzgg/': 6,  # 发改委 通知公告
            'http://zjj.chifeng.gov.cn/index.php?m=home&c=lanmu&a=index&lanmuid=440': 16,  # 住建局 动态要闻
            'http://zjj.chifeng.gov.cn/index.php?c=home&c=lanmu&a=index&lanmuid=335': 17,  # 住建局 通知公告
            'http://zjj.chifeng.gov.cn/index.php?c=home&c=lanmu&a=index&lanmuid=905': 1,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath="//div[@class='right-position-content']/div/table/tbody/tr/td[2]/a"
            elif 'fgw' in url:
                xpath="//div[@class='list']/ul/li/a"
            elif 'zjj' in url:
                xpath="//div[@class='cc']/ul[10]/li[@class='hl']"
            else:
                xpath = "//div[@class='zy_list']/ul/li"
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tr/td[', f'tr[{i*2-1}]/td[')
                        if 'ggzy' in url or 'fgw' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            # title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            #     '\r', '')
                            if 'fgw' in url:
                                title = html_1.xpath(f"{xpath1}/text()")[2].strip().replace('\n', '').replace('\t','').replace(
                                    '\r', '')
                                publictime = html_1.xpath(xpath1+"/span/text()")[0].strip().replace('/', '-').replace('[', '').replace(']', '')
                            else:
                                title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                    '\r', '')
                                publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+"/text()")[0].strip().replace('/', '-').replace('[', '').replace(']', '')
                        elif 'zjj' in url:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1.replace('hl', 'hr') + f"/text()")[0].strip().replace( '[', '').replace(']', '').replace('日', '').replace('/', '-')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[1].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/a/span/text()")[0].strip().replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-').replace('[', '').replace(']', '')

                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

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
                                        if 'www' in url:
                                            driver.find_element_by_xpath(f"//a[@class='next page-numbers']").click()
                                        else:
                                            try:
                                                driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                            except:
                                                try:
                                                    driver.find_element_by_xpath("//td[contains(string(),'下页')]").click()
                                                    # driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                                except:
                                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))

                                break
    except Exception as e:
        print('赤峰\t', e)
        driver.close()
        return chifeng(name)

# todo  通辽  公共资源中心 | 发改委 |人民政府 |住建局
def tongliao(name):
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
            'http://www.tongliao.gov.cn/tl/tlyw/list.shtml': 186,  # 人民政府 通辽要闻
            'http://www.tongliao.gov.cn/tl/bmdt/list.shtml': 249,  # 人民政府 部门动态
            'http://www.tongliao.gov.cn/tl/qxdt/list.shtml': 422,  # 人民政府 旗县动态
            'http://www.tongliao.gov.cn/tl/tzgg/list.shtml': 65,  # 人民政府 通知公告
            'http://fgw.tongliao.gov.cn/fgw/tzgg/list_fgw.shtml': 9,  # 发改委 通知公告
            'http://fgw.tongliao.gov.cn/fgw/fgdt/list_fgw.shtml': 10,  # 发改委 动态信息
            'http://fgw.tongliao.gov.cn/fgw/sgszl/list_fgw.shtml': 1,  # 发改委 双公示信息
            'http://zhujianju.tongliao.gov.cn/zjw/zhkx/list.shtml': 20,  # 住建局 综合快讯
            'http://zhujianju.tongliao.gov.cn/zjw/gsgg/list.shtml': 11,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath="//div[@class='main bgfff']/ul/li"
            elif 'zhujianju' in url:
                xpath="//div[@class='bd']/ul/li"
            else:
                xpath = "//div[@class='zwlistcon m1']/ul/li"
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

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-').replace('[', '').replace(']', '')


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
                                        if 'ggzy' in url:
                                            xy = "//td[contains(string(),'下页')]"
                                            driver.find_element_by_xpath(xy).click()
                                        try:
                                            driver.find_element_by_xpath(f"//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('»'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('通辽\t', e)
        driver.close()
        return tongliao(name)
def tongliao1():
    city='通辽'
    urls = {
        'http://ggzy.tongliao.gov.cn/tlsggzy/jyxw/about.html?categoryNum=008&pageIndex=1': 26,  # 公共资源中心 中心动态
        'http://ggzy.tongliao.gov.cn/tlsggzy/tzgg/about.html?categoryNum=008&pageIndex=1': 5,  # 公共资源中心 通知公告
    }
    for url1, pages in zip(urls.keys(), urls.values()):
      for page in range(1, pages + 1):
        headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'ggzy.tongliao.gov.cn',
            'Referer': 'http://ggzy.tongliao.gov.cn/tlsggzy/jyxw/about.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        }
        data={
            'categoryNum': '008',
            'pageIndex': f'{page}'
        }
        url=url1.replace('pageIndex=1',f'pageIndex={page}')
        con =requests.get(url,headers=headers,params=data).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
        conts=re.findall('"wb-data-infor">                                            <a href="(.*?)" title="(.*?)" target="_blank">(.*?)</a>                                        </div>                                        <span class="wb-data-date">(.*?)</span>',con)
        for cont in conts:
            href =cont[0]
            link='http://ggzy.tongliao.gov.cn'+href
            title = cont[1]
            publictime = cont[3]
            publictime_times = int(time.mktime(time.strptime(publictime.replace('[', '').replace(']', ''), "%Y-%m-%d")))
            if publictime_times >= jiezhi_time:
                select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                if select == None:
                    uid = uuid.uuid4()
                    Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                       biaoti=title, tianjiatime=insertDBtime, zt='0')
                    print(f'--{city}-【{title}】写入成功')


# todo  鄂尔多斯  公共资源中心 | 发改委(404) |人民政府 |住建局
def eerduosi(name):
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
            'http://ggzyjy.ordos.gov.cn/TPFront/xwzx/007002/': 1,  # 公共资源中心 中心动态
            'http://ggzyjy.ordos.gov.cn/TPFront/xwzx/007003/?categorynum=007003': 1,  # 公共资源中心 重要通知
            'http://ggzyjy.ordos.gov.cn/TPFront/zcfg/003002/?categorynum=003002': 1,  # 公共资源中心 政策法规
            'http://www.ordos.gov.cn/xw_127672/jreeds/': 66,  # 人民政府 今日鄂尔多斯
            'http://www.ordos.gov.cn/xw_127672/swgwhd/': 25,  # 人民政府 市委公务活动
            'http://www.ordos.gov.cn/xw_127672/zfgwhd/': 22,  # 人民政府 政府公务活动
            'http://www.ordos.gov.cn/xw_127672/qqdt/': 424,  # 人民政府 旗区动态
            'http://www.ordos.gov.cn/xw_127672/bmdt/': 230,  # 人民政府 部门动态
            'http://www.ordos.gov.cn/xw_127672/gsgg/': 16,  # 人民政府 公示公告
            'http://zjj.ordos.gov.cn/gzdt_77008/': 15,  # 住建局 新闻中心
            'http://zjj.ordos.gov.cn/tzgg_77006/': 6,  # 住建局 通知公告
            'http://zjj.ordos.gov.cn/cxtc/': 4,  # 住建局 城乡建设
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy' in url:
                xpath="//div[@class='mid-block']/table/tbody/tr/td[3]/table/tbody/tr[3]/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/a"
            elif 'zjj' in url:
                xpath="//div[@class='lm_r fr bd1g']/ul/li"
            else:
                xpath = "//div[@class='yzgl_right_box']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if i==8 and page==31:
                        pass
                    else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tbody/tr/td[2]/a', f'tbody/tr[{i}]/td[2]/a')
                        if 'ggzyjy' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+"/text()")[0].strip().replace('/', '-').replace('[', '').replace(']', '')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('年', '-').replace('月', '-').replace('日', '').replace('/', '-').replace('[', '').replace(']', '')


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
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('鄂尔多斯\t', e)
        driver.close()
        return eerduosi(name)

# def eerduosi1():
#     name='鄂尔多斯'
#     urls = {
#         'http://ggzyjy.ordos.gov.cn/TPFront/xwzx/007002/?Paging=1': 3,  # 公共资源中心 中心动态
#         'http://ggzyjy.ordos.gov.cn/TPFront/xwzx/007003/?Paging=1': 3,  # 公共资源中心 重要通知
#         'http://ggzyjy.ordos.gov.cn/TPFront/zcfg/003002/?Paging=1': 1,  # 公共资源中心 政策法规
#     }
#     for url1, pages in zip(urls.keys(), urls.values()):
#         for page in range(1,pages+1):
#           headers={
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Connection': 'keep-alive',
#             'Cookie': '_gscu_294525365=91586384mxje6z14; _gscu_232331937=95237591mv7ql844; UM_distinctid=1736b91e83b7a7-0a194ca638a317-f7d1d38-13c680-1736b91e83c8ce; ASP.NET_SessionId=nukorcgoscduc4otwi0y2vtt; Hm_lvt_ca237d329bd2fbf34d1ba22211b30e31=1594619632,1595236547,1596092011,1596681825; Hm_lvt_a9bd5e433cf283aed81d69d137fd12f1=1594619632,1595236547,1596092011,1596681825; _gscbrs_294525365=1; _gscs_294525365=96681824f4vj0d16|pv:2; Hm_lpvt_ca237d329bd2fbf34d1ba22211b30e31=1596682202; Hm_lpvt_a9bd5e433cf283aed81d69d137fd12f1=1596682202',
#             'Host': 'ggzyjy.ordos.gov.cn',
#             'Upgrade-Insecure-Requests': '1',
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
#         }
#           data={
#             'Paging':f'{page}'
#           }
#           url=url1.replace('Paging=1',f'Paging={page}')
#           con=requests.get(url,headers=headers,params=data).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
#           conts=re.findall('',con)
#           for cont in conts:
#               href = cont[0]
#               title = cont[0]
#               publictime = cont[0]
#               select = Mysql.select_xw_nr1(biaoti=title, dijishi=name)  # 查询标题是否存在
#
#               if select == None:
#                   publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
#                   # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
#                   if publictime_times >= jiezhi_time:
#                       if 'jxcq' in url:
#                           insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
#                           link = 'http://www.jxcq.org' + href
#                           uid = uuid.uuid4()
#                           Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=name, fabutime=publictime,
#                                              url=link,
#                                              biaoti=title, tianjiatime=insertDBtime, zt='0')
#                           print(f'--{name}-【{title}】写入成功')
# eerduosi1()
# todo  呼伦贝尔  公共资源中心 | 发改委(404)  |住建局
def hulunbeier(name):
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
            'http://www.hlbeggzyjy.org.cn/dtxw/subpage.html': 1,  # 公共资源中心 动态新闻
            'http://www.hlbeggzyjy.org.cn/tzgg/subpage.html': 1,  # 公共资源中心 通知公告
            'http://zjj.hlbe.gov.cn/newslist/126/1': 2,  # 住建局  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hlbeggzyjy' in url:
                xpath="//div[@class='ewb-right-bd']/ul/li/div/a"
            elif 'zjj' in url:
                xpath="//div[@class='met-news-list']/ul/li/h4/a"
            else:
                xpath = "//div[@class='yzgl_right_box']/ul/li"
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

                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        if 'hlbeggzyjy' in url:
                            publictime = html_1.xpath(xpath1.replace('div/a','span')+"/text()")[0].strip().replace('/', '-').replace('[', '').replace(']', '')
                        else:

                            publictime = html_1.xpath(xpath1.replace('h4/a','p/span')+f"/text()")[0].strip().replace('发布时间：', '').replace('/', '-').replace('[', '').replace(']', '')


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
                                        if 'www' in url:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页  >>'))
                                            except:
                                                driver.find_element_by_xpath("//td[contains(string(),'下页')]").click()
                                        else:

                                                try:
                                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页»'))
                                                except:
                                                    driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('呼伦贝尔\t', e)
        driver.close()
        return hulunbeier(name)
# todo  呼伦贝尔   人民政府
def hulunbeier1(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")

        urls = {
            'http://www.hlbe.gov.cn/content/channel/53db0d059a05c2a06a7d9883/page-1/': 72,  # 人民政府 今日呼伦贝尔
            'http://www.hlbe.gov.cn/content/channel/53db00cd9a05c2ed6683fff8/page-1/': 407,  # 人民政府 部门动态
            'http://www.hlbe.gov.cn/content/channel/53db00bb9a05c2ab69621acb/page-1/': 701,  # 人民政府 旗市区动态
            'http://www.hlbe.gov.cn/content/channel/53db004e9a05c2b4698afee4/page-1/': 701,  # 人民政府 通知公告

        }
        for url1, pages in zip(urls.keys(), urls.values()):
          for page in range(1, pages + 1):
            url=url1.replace('-1/',f'-{page}/')
            con=requests.get(url).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
            conts=re.findall('<li><span>(.*?)</span><a href="(.*?)" title="(.*?)" target="_blank"',con)
            for cont in conts:
                title=cont[2]
                publictime=cont[0][1:-1]
                link='http://www.hlbe.gov.cn'+cont[1]

                select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

                if select == None:
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        uid = uuid.uuid4()
                        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                           biaoti=title, tianjiatime=insertDBtime, zt='0')
                        print(f'--{city}-【{title}】写入成功')


    except Exception as e:
        print('呼伦贝尔\t', e)
        driver.close()
        return hulunbeier(name)


# todo  巴彦淖尔  公共资源中心 |
def bayazhuoer(name):
    global driver
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")

        urls = {
            'http://ggzyjy.bynr.gov.cn/zwxx/moreinfo.html': 9,  # 公共资源中心 政务信息
        }
        for url1, pages in zip(urls.keys(), urls.values()):
          for page in range(1, pages + 1):
                if page==1:
                    url=url1
                else:
                    url=url1.replace('moreinfo.html',f'{page}/.html')
                con=requests.get(url).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
                conts=re.findall(' <li class="clearfix">                                           <a href="(.*?)" title="(.*?)" target="_blank">(.*?)</a>                                           <span class="r ewb-news-date">(.*?)</span>                                        </li>   ',con)
                for cont in conts:
                    title=cont[1]
                    publictime=cont[3]
                    link='http://ggzyjy.bynr.gov.cn'+cont[0]
                    select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')


    except Exception as e:
        print('巴彦淖尔\t', e)
        driver.close()
        return bayazhuoer(name)
# todo  巴彦淖尔  公共资源中心 | 发改委(404) |人民政府 |住建局
def bayazhuoer1(name):
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
            'http://www.bynr.gov.cn/dtxw/zwdt/': 67,  # 人民政府 政务动态
            'http://www.bynr.gov.cn/dtxw/tpxw/': 6,  # 人民政府 图片新闻
            'http://www.bynr.gov.cn/dtxw/qqdt/': 67,  # 人民政府 旗区动态
            'http://www.bynr.gov.cn/dtxw/bmdt/': 67,  # 人民政府 部门动态
            'http://www.bynr.gov.cn/xxgk/zcfg/zcjd_1/': 21,  # 人民政府 政策解读
            'http://fgw.bynr.gov.cn/sites/fgw/list.jsp?ColumnID=13&SiteID=fgw': 21,  # 发改委 发改动态
            'http://fgw.bynr.gov.cn/sites/fgw/list.jsp?ColumnID=10&SiteID=fgw': 10,  # 发改委 通知公告
            'http://fgw.bynr.gov.cn/sites/fgw/list.jsp?ColumnID=11&SiteID=fgw': 8,  # 发改委 政策解读
            'http://zjj.bynr.gov.cn/zjwgzdt/zjwgzdtxx/': 12,  # 住建局 住建动态
            'http://zjj.bynr.gov.cn/zjwgzdt/zjwtpxw/': 2,  # 住建局 图片新闻
            'http://zjj.bynr.gov.cn/zjwzcfg/zcfg/': 3,  # 住建局 政策法规
            'http://zjj.bynr.gov.cn/zjwzcfg/zcjd/': 2,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath="//div[@class='yzgl_right']/ul/li/div"
            elif 'zjj' in url:
                xpath="//table[@class='mag_01 line1']/tbody/tr[2]/td[2]/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr/td/a"
            else:
                xpath = "//div[@class='list-right-list']/ul/li/a"
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
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('tbody/tr/td/a', f'tbody/tr[{i}]/td/a')


                        if 'fgw' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/p/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            publictime = html_1.xpath(xpath1.replace('/a','/a/span')+"/text()")[0].strip().replace('/', '-').replace('【', '').replace('】', '')
                        elif 'zjj' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            publictime = html_1.xpath(xpath1.replace('/a','[2]')+"/text()")[0].strip().replace('/', '-').replace('【', '').replace('】', '')
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(  '\r', '')
                            publictime = html_1.xpath(xpath1+"/span/text()")[0].strip().replace('发布时间：', '').replace('/', '-').replace('[', '').replace(']', '')


                        select = Mysql.select_xw_nr1(biaoti=title,dijishi=name)  # 查询标题是否存在
                        link = url + href.replace('./', '')
                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                if 'www' in url:
                                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                                    uid = uuid.uuid4()
                                    Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime,
                                                       url=link, biaoti=title, tianjiatime=insertDBtime, zt='0')
                                    print(f'--{city}-【{title}】写入成功')
                                else:
                                    chuli(publictime, href, driver, url, title, city,xpath1)
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
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页  >>'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('巴彦淖尔\t', e)
        driver.close()
        return bayazhuoer1(name)

# todo  乌兰察布  公共资源中心 | 发改委|人民政府 |住建局(无)
def wulanchabu(name):
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
            'http://ggzy.wulanchabu.gov.cn/tzgg?area=001': 2,  # 公共资源中心 通知公告
            'http://ggzy.wulanchabu.gov.cn/zxdt?area=001': 3,  # 公共资源中心 工作动态
            'http://ggzy.wulanchabu.gov.cn/jyzk/zcfg?lawsType=1&city=': 2,  # 公共资源中心 政策法规
            'http://www.wulanchabu.gov.cn/active/fpage_3.jsp?psize=20&showpagenum=true&fid=9345&pos=1': 120,  # 人民政府 今日乌兰察布
            'http://www.wulanchabu.gov.cn/active/fpage_3.jsp?psize=20&showpagenum=true&fid=13357': 10,  # 人民政府 公告公示
            'http://www.wulanchabu.gov.cn/active/fpage_3.jsp?psize=20&showpagenum=true&fid=9347': 114,  # 人民政府 部门动态
            'http://www.wulanchabu.gov.cn/active/fpage_1.jsp?psize=30&showpagenum=true&fid=17606': 2,  # 人民政府 政策解读
            'http://fgw.wulanchabu.gov.cn/Article/ShowClass.asp?ClassID=21': 1,  # 住建局 通知公告
            'http://fgw.wulanchabu.gov.cn/Article/ShowClass.asp?ClassID=1': 2,  # 住建局 政策法规
            'http://fgw.wulanchabu.gov.cn/Article/ShowClass.asp?ClassID=3': 2,  # 住建局 政策解读
            'http://fgw.wulanchabu.gov.cn/Article/List_26.html': 3,  # 住建局 动态要闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath="//table[@id='p2']/tbody/tr/td/a"
            elif 'www' in url:
                xpath="//table[@class='recordlist']/tbody/tr/td/a"
            else:
                xpath = "//table[@class='qingchunzhongxueA_biangkuan bg_phototitle01']/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr/td/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'ggzy' in url and i==1:
                        pass
                    elif 'www' in url and i%6==0:
                        pass
                    else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('/tr/td/a', f'/tr[{i}]/td/a')


                        # if 'ggzy' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'ggzy' in url:
                            publictime = html_1.xpath(xpath1.replace('/a','[3]')+"//text()")[0].strip().replace('/', '-').replace('【', '').replace('】', '')
                        elif 'fgw' in url:
                            publictime = html_1.xpath(xpath1.replace('/a','[4]')+"//text()")[0].strip().replace('/', '-').replace('【', '').replace('】', '')
                        else:
                            publictime = html_1.xpath(xpath1.replace('/a','[2]')+"//text()")[0].strip().replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '').replace(' ', '')
                        # else:
                        #     href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        #     title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(  '\r', '')
                        #     publictime = html_1.xpath(xpath1+"/span/text()")[0].strip().replace('发布时间：', '').replace('/', '-').replace('[', '').replace(']', '')


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
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页  >>'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('乌兰察布\t', e)
        driver.close()
        return wulanchabu(name)

# todo  兴安盟  公共资源中心 | 发改委 | 人民政府 |住建局
def xinganmeng(name):
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
            'http://www.xamggzyjyzx.org.cn/xamggzy/zwgk/018001/': 1,  # 公共资源中心 通知公告
            'http://www.xamggzyjyzx.org.cn/xamggzy/zwgk/018002/': 1,  # 公共资源中心 工作动态
            'http://www.xamggzyjyzx.org.cn/xamggzy/zwgk/018005/': 1,  # 公共资源中心 宣传动态
            'http://www.xamggzyjyzx.org.cn/xamggzy/zcfg/': 1,  # 公共资源中心 政策法规
            'http://www.xam.gov.cn/xam/index/_300518/index.html': 18,  # 人民政府 今日兴安
            'http://www.xam.gov.cn/xam/index/_300522/index.html': 45,  # 人民政府 旗县动态
            'http://www.xam.gov.cn/xam/index/_300526/index.html': 14,  # 人民政府 部门动态
            'http://www.xam.gov.cn/xam/index/3230752/index.html': 5,  # 人民政府 通知公告
            'http://fgw.xam.gov.cn/fgw/xwdt7/1119974/index.html': 7,  # 发改委 发改动态
            'http://fgw.xam.gov.cn/fgw/1119945/1119954/index.html': 3,  # 发改委 政策法规
            'http://fgw.xam.gov.cn/fgw/1119945/1119937/index.html': 5,  # 发改委 通知公告
            'http://zjj.xam.gov.cn/jsj/1021392/1021427/1021430/index.html': 5,  # 住建局 工作动态
            'http://zjj.xam.gov.cn/jsj/1021392/1021427/1021384/index.html': 5,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath="//div[@class='list-body-hd']/ul/li/a"
            elif 'fgw' in url or 'zjj' in url:
                xpath="//div[@class='zd_mod2_main']/ul/li/span/a"
            else:
                xpath = "//div[@id='11dfefffae6d49f4a03b819f85ec7563']/div[3]/ul/li/span/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    # if 'ggzy' in url and i==1:
                    #     pass
                    # elif 'www' in url and i%6==0:
                    #     pass
                    # else:

                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul/li[{i}]').replace('/tr/td/a', f'/tr[{i}]/td/a')


                        if 'www' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/span[1]/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            publictime = html_1.xpath(xpath1+"/span[2]/text()")[0].strip().replace('/', '-').replace('【', '').replace('】', '')

                        else:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(  '\r', '')
                            publictime = html_1.xpath(xpath1.replace('/a','[2]')+"/text()")[0].strip().replace('发布时间：', '').replace('/', '-').replace('[', '').replace(']', '')


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
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('兴安盟\t', e)
        driver.close()
        return xinganmeng(name)

neimeng('内蒙')
huhehaote('呼和浩特')
huhehaote1('呼和浩特')
baotou('包头')
chifeng('赤峰')
tongliao('通辽')
tongliao1()
eerduosi('鄂尔多斯')
hulunbeier('呼伦贝尔')
hulunbeier1('呼伦贝尔')
bayazhuoer('巴彦淖尔')
bayazhuoer1('巴彦淖尔')
wulanchabu('乌兰察布')
xinganmeng('兴安盟')