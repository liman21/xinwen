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


gjzs = ['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子', '保险']
pro = '福建'
jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 60

# todo  福建 公共资源中心 | 住建局
def fujian(name):
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
            'http://www.fjggzyjy.cn/news/category/41/': 2,  # 公共资源中心 通知公告
            'http://www.fjggzyjy.cn/news/category/67/': 1,  # 公共资源中心 工作动态
            'http://www.fjggzyjy.cn/news/category/40/': 2,  # 公共资源中心 中心新闻
            'http://zjt.fujian.gov.cn/xxgk/gzdt/bmdt/': 12,  # 住建局 部门动态
            'http://zjt.fujian.gov.cn/xxgk/gzdt/sxdt/': 11,  # 住建局 市县动态
            'http://zjt.fujian.gov.cn/xxgk/zcjd/': 2,  # 住建局  政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//a[@class='btn btn-default article-list-single']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    xpath1 = xpath + f'[{i}]'
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath1}/span[@class='article-list-text']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span[@class='article-list-date']/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif './' in href:
                            link = url + href[2:]
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            # go = 0
                            # fo = 0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon = qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo += 1
                            #             print(f'有附件{fj}个')
                            #
                            #         go += 1
                            #         driver.back()
                            #         break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    xy = "//td[contains(string(),'下页')]"
                                    driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('福建\t', e)
        driver.close()
        return fujian(name)


# todo  福建  发改委 | 人民政府 | 产权交易
def fujian1(name):
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
            'http://fgw.fujian.gov.cn/xxgk/gsgg/':15,  # 发改委 公示公告
            'http://fgw.fujian.gov.cn/xxgk/gzdt/sxdt/':10,  # 发改委 市县要闻
            'http://fgw.fujian.gov.cn/xxgk/gzdt/bwdt/':21,  # 发改委 本委要闻
            'http://www.fj.gov.cn/xw/fjyw/': 222,  # 人民政府 福建要闻
            'http://www.fj.gov.cn/xw/zfgzdt/bmdt/': 240,  # 人民政府  部门动态
            'https://www.fjcqjy.com/html/list-content-0OLIA6ZX0Y349BGXG823.html': 240,  # 产权交易  新闻中心
            'https://www.fjcqjy.com/html/list-content-1dp02ajl45g762rs8gdv.html': 3,  # 产权交易  通知
            'https://www.fjcqjy.com/html/list-content-736AG7QP2BXV1R996TW2.html': 1,  # 产权交易  其它资讯
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'sxdt' in url:
                xpath = "//div[3]/div[@class='gz_right_box']/ul/li"
            elif 'www.fj.' in url:
                xpath = "//div[3]/div[@class='box-gl clearflx']/ul/li"
            elif 'www.fjcqjy' in url:
                xpath = "//div[@class='data_list minheight']/ul/li/a"
            else:
                xpath = "//div[2]/div[@class='gz_right_box']/ul/li"
            xpath11 = xpath.replace('/ul/li', '[1]/ul/li/a')  # i
            xpath22 = xpath.replace('/ul/li', '/ul/li[1]/a')  # j
            length = len(html_2.xpath(xpath)) + 1
            length11 = len(html_2.xpath(xpath11)) + 1
            length22 = len(html_2.xpath(xpath22)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, length22):
                    for i in range(1, length11):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace(']/ul/li', f'][{j}]/ul/li[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif './' in href:
                                link = url + href[2:]
                            elif 'www.fjcqjy' in url:
                                link = 'https://www.fjcqjy.com' + href
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')

                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1: break
                                else:
                                    if page != pages:
                                        try:
                                            xy = "//td[contains(string(),'下页')]"
                                            driver.find_element_by_xpath(xy).click()
                                        except:  driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
                        else:
                            po += 1
                            break

    except Exception as e:
        print('福建1\t', e)
        driver.close()
        return fujian1(name)


# todo  福州 公共资源中心 |行政服务中心| 人民政府
def fuzhou(name):
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
            'http://fzsggzyjyfwzx.cn/zytz/index.jhtml':6,  # 公共资源中心 中心通知
            'http://fzsggzyjyfwzx.cn/zxdt/index.jhtml':3,  # 公共资源中心 中心动态
            'http://fzsggzyjyfwzx.cn/zcfggcsz/index.jhtml':1,  # 公共资源中心 市级政策法规
            'http://xzfwzx.fuzhou.gov.cn/zz/zwgk/zxdt/zxxw/':7,  # 福州市行政服务中心 中心新闻
            'http://xzfwzx.fuzhou.gov.cn/zz/zwgk/zxdt/zxgg/':2,  # 福州市行政服务中心 中心公告
            'http://xzfwzx.fuzhou.gov.cn/zz/zwgk/zcjd/': 2,  # 福州市行政服务中心 政策解读
            'http://www.fuzhou.gov.cn/gzdt/rcyw/h': 200,  # 人民政府 榕城要闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'xzfwzx' in url:
                xpath = "//ul[@class='mt10']/li/a"
            elif 'www' in url:
                xpath = "//div[1]/div[@class='gl_news clearflx']/a"
            else:
                xpath = "//li[@class='jygk-li']/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    xpath1=xpath.replace('i/a',f'i[{i}]/').replace(']/a',f'][{i}]/a').replace(']/div/a',f'][{i}]/div/')

                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span/em/i[@class='gl_news_top_tit']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/em/i[@class='fr gl_news_top_rq']/text()")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        if 'zcjd' in url:
                            publictime = html_1.xpath(f"{xpath1}span/text()")[2].strip()
                        elif 'xzfwzx' in url:
                            publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                        else:
                            publictime = html_1.xpath(f"{xpath1}div/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime.replace('[','').replace(']',''), "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif './' in href:
                            link =url+ href[2:]
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    xy = "//td[contains(string(),'下页')]"
                                    driver.find_element_by_xpath(xy).click()
                    else:
                        po += 1
                        break
    except Exception as e:
        print('福州\t', e)
        driver.close()
        return fuzhou(name)
# todo  福州  发改委 | 建设局
def fuzhou1(name):
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
            'http://fgw.fuzhou.gov.cn/zz/fgwzwgk/gzdt/':15,  # 发改委 工作动态
            'http://fgw.fuzhou.gov.cn/zz/fgwzwgk/tzgg/':5,  # 发改委 通知公告
            'http://fzjw.fuzhou.gov.cn/zz/zwgk/zwgk/':37,  # 建设局 工作动态
            'http://fzjw.fuzhou.gov.cn/zz/zwgk/tzgg/':109,  # 建设局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'fzjw' in url:
                xpath="//div/div[2]/div/ul[@class='list']/li/a"
                jj=4
                ii=6
            else:
                xpath = "//table[@class='gl_tit5 mar_t10 pad_b15']//tr"
                jj=5
                ii=5
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                con1 = driver.page_source
                con=con1.replace('avalonHide','')
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, ii):
                        lengt = len(html_2.xpath(xpath))
                        if 'fzjw' in url:
                            xpath1 = xpath.replace("v/ul[@class='list']/li/a", f"v[{j}]/ul[@class='list']/li[{i}]/")
                            href = html_1.xpath(f"{xpath1}a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                        else:
                            xpath1 = xpath.replace(']//tr', f'][{j}]//tr')
                            href = html_1.xpath(f"{xpath1}[{i}]/td[1]/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            title = html_1.xpath(f"{xpath1}[{i}]/td[1]/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f"{xpath1}[{i}]/td[2]/text()")[0].strip().replace('[','').replace(']','')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif './' in href:
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()

                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')

                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.find_element_by_xpath("//td[contains(string(),'下页')]").click()
                                        except:
                                            driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('下一页'))
                                break
                        else:
                            po += 1
                            break

    except Exception as e:
        print('福州1\t', e)
        driver.close()
        return fuzhou1(name)



# todo  厦门 公共资源中心
def xiamen(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,
                                  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        url = 'http://www.xmzyjy.cn/XmUiForWeb2.0/xmebid/default.do'
        driver.get(url)
        time.sleep(1)
        xpaths = {
            "//div[@class='new_tabs']/ul/li[1]":5,  # 公共资源中心 通知公告
            "//div[@class='new_tabs']/ul/li[2]":2,  # 公共资源中心 行业动态
            "//div[@class='new_tabs']/ul/li[3]": 1,  # 公共资源中心 工作动态
        }
        for xpath2, pages in zip(xpaths.keys(), xpaths.values()):
            driver.find_element_by_xpath(xpath2).click()
            time.sleep(2)
            driver.find_element_by_xpath("//div[@id='moreContent']/a").click()  # 查看全部
            time.sleep(1)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='type_data']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 2

            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(2, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('li/a', f'li[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        link = 'http://www.xmzyjy.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')

                        if i - 1 == lengt:
                            driver.find_element_by_xpath("//li[@class='next']/a").click()
                            break
                    else:
                        po += 1
                        break
            driver.find_element_by_xpath("//a[@class='comHomePageTag']").click()
            time.sleep(1)

    except Exception as e:
        print('厦门\t', e)
        driver.close()
        return xiamen(name)
# todo  厦门  发改委 | 政审批管理局 | 人民政府
def xiamen1(name):
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
            'http://as.xm.gov.cn/zwgk/gzdt/':1,  # 政审批管理局 工作动态
            'http://as.xm.gov.cn/zwgk/tzgg/':1,  # 政审批管理局 通知公告
            'http://www.xm.gov.cn/xmyw/':1,  # 人民政府 厦门要闻
            'http://www.xm.gov.cn/zxgg/':1,  # 人民政府 最新通告
            'http://js.xm.gov.cn/xxgk/jsdt/':1,  # 建设局 建设动态
            'http://js.xm.gov.cn/xxgk/zxwj/':1,  # 建设局 建设动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath="//div[@class='gl_list1']/ul/li"
            if 'www' in url:
                jj=4
            else:jj=5
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, 6):
                        lengt = len(html_2.xpath(xpath))
                        if 'www' in url or 'js' in url:
                            xpath1 = xpath.replace(']/ul/li', f']/ul[{j}]/li[{i}]')
                        else:
                            xpath1 = xpath.replace(']/ul/li', f'][{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()[1:-1].replace('\n','').replace('\t','').replace('\r','')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif './' in href:
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')

                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:

                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页>'))
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                            except:
                                                xy = "//td[contains(string(),'下页')]"
                                                driver.find_element_by_xpath(xy).click()
                                        except:
                                            xy = "//td[contains(string(),'下页')]"
                                            driver.find_element_by_xpath(xy).click()
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('厦门1\t', e)
        driver.close()
        return xiamen1(name)
# todo  厦门  发改委
def xiamen2(name):
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
            'http://dpc.xm.gov.cn/xwdt/gzdt/':8,  # 发改委 工作动态
            'http://dpc.xm.gov.cn/xwdt/tzgg/':5,  # 发改委 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath="//div[@class='gl_lis']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_2.xpath(xpath)) + 1
                    xpath1 = xpath.replace('l/li', f'l/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()[1:-1].replace('\n','').replace('\t','').replace('\r','')
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif './' in href:
                            link = url + href[2:]

                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            # go = 0
                            # fo = 0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon = qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo += 1
                            #             print(f'有附件{fj}个')
                            #
                            #         go += 1
                            #         driver.back()
                            #         break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    xy = "//td[contains(string(),'下页')]"
                                    driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('厦门2\t', e)
        driver.close()
        return xiamen2(name)


# todo  三明 公共资源中心 | 发改委
def sanming(name):
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
            'http://smggzy.sm.gov.cn/smwz/zwgk/001004/001004001/':3,  # 公共资源中心 通知公告
            'http://smggzy.sm.gov.cn/smwz/zwgk/001004/001004002/':2,  # 公共资源中心 工作动态
            'http://smggzy.sm.gov.cn/smwz/zwgk/001004/001004003/':2,  # 公共资源中心 行业动态
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//li/a[@class='l']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+ 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    href = html_1.xpath(f"{xpath}/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath}/text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"//li[{i}]/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif './' in href:
                            link = url+href[2:]
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            # go = 0
                            # fo = 0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         # list=[pro,city,publictime,link,title,insertDBtime]
                            #         # tj_excel(rf'D:\lm\\xinwen\数据\\{pro}\\{city}\列表.xlsx',list)
                            #         get_image(link,
                            #                   f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         go += 1
                            #         break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    xy = "//td[contains(string(),'下页')]"
                                    driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('三明\t', e)
        driver.close()
        return sanming(name)
# todo  三明  行政服务中心 (模拟点击)
def     sanming1(name):
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
        url='http://smzwzx.sm.gov.cn/smmh/jsp/secondLevel/list.jsp?category=ZXGK&categoryName=%E4%B8%AD%E5%BF%83%E6%A6%82%E5%86%B5'
        driver.get(url)

        xpaths={
            "1+C3EAE2AF377CF02D301F16F086B2DACB":3,  # 行政服务中心 中心要闻
            "2+5C55729D32DA392BE67EE28985B3E30E":5,  # 行政服务中心 通知公告
            "3+202D5003A0589F7637F2424D3C0AF8B6":154  # 行政服务中心 工作动态
        }
        for xx, pages in zip(xpaths.keys(), xpaths.values()):
            categoryUnid=xx[2:]
            driver.find_element_by_xpath(f"//div[@class='news-sub']/ul/li[{xx[:1]}]/a").click()
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            fenlei=html_2.xpath("//div[@class='news-list-tit']/span/text()")[0].strip()
            if 'smzwzx' in url:
                xpath="//li/a[@class='fl']"
            else:
                xpath = "//li/a[@class='l']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+ 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    href = html_1.xpath(f"{xpath}/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath}/text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                    if 'smzwzx' in url:
                        publictime = html_1.xpath(f"//li[{i}]/span[@class='fr']/text()")[0].strip()
                    else:
                        publictime = html_1.xpath(f"//li[{i}]/span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        unid=re.findall("\('(.*?)'\)",href)[0]
                        link=f'http://smzwzx.sm.gov.cn/smmh/jsp/three/article.jsp?unid={unid}&currutCategory={fenlei}&categoryName=中心概况&topName=首页&category=ZXGK&categoryUnid={categoryUnid}&isSMS=true'
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            # go = 0
                            # fo = 0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon = qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo += 1
                            #             print(f'有附件{fj}个')
                            #
                            #         go += 1
                            #         driver.find_element_by_xpath(xpath0).click()
                            #         break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    xy = "//td[contains(string(),'下页')]"
                                    driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('三明1\t', e)
        driver.close()
        return sanming1(name)
# todo   三明市人民政府 | 住建局(ij)
def sanming2(name):
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
            'http://www.sm.gov.cn/zw/zwxx/sjdt/':268,  # 三明市 人民政府 市级动态
            'http://www.sm.gov.cn/zw/zwxx/xjdt/':124,  # 三明市 人民政府 县级动态
            'http://zjj.sm.gov.cn/xxgk/gzdt/gzdt/':8,  # 三明市 住建局 工作动态
            'http://zjj.sm.gov.cn/xxgk/gzdt/tpxw/':4,  # 三明市 住建局 图片新闻
            'http://zjj.sm.gov.cn/xxgk/tzgg/':5,  # 三明市 住建局 通知公告
            'http://zjj.sm.gov.cn/xxgk/zcjd/':1,  # 三明市 住建局  政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if '/www.sm.gov' in url :
                xpath = "//div[1]/ul[@class='list-sm-gl']/li"
            else:
                xpath="//div[2]/div/ul/li"
            if 'www' in url:
                jj=4
            else:jj=5
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, 6):
                        lengt = len(html_2.xpath(xpath))
                        if 'www' in url:
                            xpath1 = xpath.replace(']/li', f'][{j}]/li[{i}]')
                        else:
                            xpath1 = xpath.replace('div/ul/li', f'div[{j}]/ul[{i}]/li')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif './' in href:
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            xy = "//td[contains(string(),'下页')]"
                                            driver.find_element_by_xpath(xy).click()
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))

                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('三明2\t', e)
        driver.close()
        return sanming2(name)




# todo  泉州 公共资源中心 | 行政服务中心 | 产权交易  | 住建局
def quanzhou(name):
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
            'http://ggzyjy.quanzhou.gov.cn/articleList/articleListPage.do?classNo=4':7,  # 通知公告
            'http://ggzyjy.quanzhou.gov.cn/articleList/articleListPage.do?classNo=1&centerId=-1':2,  # 政策法规

            'http://www.qzcq0595.com/content/xwzx.aspx?RID=100':12,  # 产权交易中心 通知公告   加载过慢
            'http://www.qzcq0595.com/content/xwzx.aspx?xwid=2':1,  # 产权交易中心 中心动态
            'http://www.qzcq0595.com/content/xwzx.aspx?xwid=1':1,  # 产权交易中心 行业新闻
            'http://zfjsj.quanzhou.gov.cn/zwgk/zxdt/':15,  # 住建局 最新动态
            'http://zfjsj.quanzhou.gov.cn/zwgk/wjtz/':17,  # 住建局 文件通知
            'http://zfjsj.quanzhou.gov.cn/zwgk/xsqdt/':9,  # 住建局 县市区动态
            'http://zfjsj.quanzhou.gov.cn/zwgk/gggs/':10,  # 住建局 公告公示
       }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'xzfwzx' in url: ii=2
            else:  ii=1
            if 'www' in url:
                xpath = "//ul/li/span[2]"
            elif 'zfjsj' in url:
                xpath = "//div[@class='gl_ul mar_t20']/ul/li/a"
            else:
                xpath = "//ul[@id='DetailList']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(ii, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    xpath1 = xpath.replace('i/a', f'i[{i}]').replace('r/t', f'r[{i}]/t').replace('i/s', f'i[{i}]/s')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'www' in url:
                        publictime = html_1.xpath(f"//div[@class='lbox1 zxdt_box']/ul/li[{i}]/span[1]/text()")[0].strip()
                    else:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime.replace('[','').replace(']',''), "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
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
                            link = url+href[2:]

                        elif 'content' in url:
                            link = 'http://www.qzcq0595.com/content/'+href
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                        if i == lengt:
                            if page != pages:
                                driver.find_element_by_xpath("//li[@class='ewb-page-li ewb-page-hover'][2]/a").click()
                    else:
                        po += 1
                        break

    except Exception as e:
        print('泉州\t', e)
        driver.close()
        return quanzhou(name)
# todo   泉州 发改委 | 人民政府(ij)
def quanzhou1(name):
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
            'http://fgw.quanzhou.gov.cn/zwgk/gzdt/':19,  # 发改委 工作动态
            'http://fgw.quanzhou.gov.cn/zwgk/tzgg/':14,  # 发改委 通知公告
            'http://xzfwzx.quanzhou.gov.cn/zwgk/zcjd/': 1, # 行政服务中心 政策解读
            'http://xzfwzx.quanzhou.gov.cn/zwgk/gzdt/': 5,  # 行政服务中心 工作动态
            'http://www.quanzhou.gov.cn/zfb/xxgk/zfxxgkzl/qzdt/qzyw/':25,  # 人民政府 泉州要闻
            'http://www.quanzhou.gov.cn/zfb/xxgk/zfxxgkzl/qzdt/xsqdt/':52,  # 人民政府 县（市、区）动态
            'http://www.quanzhou.gov.cn/zfb/xxgk/zfxxgkzl/qzdt/bmdt/':53,  # 人民政府 部门动态
            'http://www.quanzhou.gov.cn/zfb/xxgk/zfxxgkzl/gzdt/zwyw/':28,  # 人民政府 政务要闻
            'http://www.quanzhou.gov.cn/zfb/xxgk/ztxxgk/zcjd/ctxs/':28,  # 人民政府 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'fgw' in url :
                xpath = "//div[@class='gl_list2']/ul/li/a"
                jj = 5
            elif 'xzfwzx' in url:
                xpath = "//div[@class='gl_list1']/ul/li/a"
                jj = 5
            elif 'zcjd' in url :
                xpath = "//div[@class='gl_list']/ul/li/a[1]"
                jj = 5
            elif 'zwyw' in url :
                xpath = "//div[2]/div[@class='wsbs_list6']/ul/li/a"
                jj = 5
            else:
                xpath="//div[1]/div[@class='wsbs_list6']/ul/li/a"
                jj = 8
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
                        if 'zcjd' in url:
                            xpath1 = xpath.replace('/ul/li/a[1]', f'[{j}]/ul/li[{i}]')
                        else:
                            xpath1 = xpath.replace('/ul/li/a', f'[{j}]/ul/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()[1:-1]
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
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
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页  >'))
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                            except:
                                                xy = "//td[contains(string(),'下一页')]"
                                                driver.find_element_by_xpath(xy).click()

                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('泉州1\t', e)
        driver.close()
        return quanzhou1(name)


# todo  漳州 公共资源中心 | 行政服务 | 发改委 |人民政府 |住建局
def zhangzhou(name):
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
            'http://fgw.quanzhou.gov.cn/zwgk/zcfg/': 1,  # 发改委 法规制度
            'http://xzfwzx.zhangzhou.gov.cn/cms/html/zzsxzfwzx/gzdt/index.html':21,  # 行政服务 工作动态
            'http://xzfwzx.zhangzhou.gov.cn/cms/html/zzsxzfwzx/tzgg/index.html':4,  # 行政服务 通知公告
            'http://fgw.zhangzhou.gov.cn/cms/html/zzsfzhggwyh/gzdt/index.html':11,  # 发改委 工作动态
            'http://fgw.zhangzhou.gov.cn/cms/html/zzsfzhggwyh/tzgg/index.html':3,  # 发改委 通知公告
            'http://fgw.zhangzhou.gov.cn/cms/html/zzsfzhggwyh/zcwj/index.html':1,  # 发改委 政策文件
            'http://www.zzgcjyzx.com/Front/tzgg/': 2,  # 公共资源中心 通知
            'http://www.zzgcjyzx.com/Front/zcfg/': 1,  # 公共资源中心 政策法规
            'http://www.zhangzhou.gov.cn/cms/html/zzsrmzf/zzyw/index.html': 153,  # 人民政府 漳州要闻
            'http://www.zhangzhou.gov.cn/cms/html/zzsrmzf/bmdt1/index.html': 382,  # 人民政府 部门动态
            'http://www.zhangzhou.gov.cn/cms/html/zzsrmzf/xsqxw1/index.html': 649,  # 人民政府 县（市、区）新闻
            'http://www.zhangzhou.gov.cn/cms/html/zzsrmzf/gsgg/index.html': 6,  # 人民政府 公示公告
            'http://jsj.zhangzhou.gov.cn/cms/html/zzszfhcxjsj/zxwj/index.html': 27,  # 住建局 最新文件
            'http://jsj.zhangzhou.gov.cn/cms/html/zzszfhcxjsj/gzdt/index.html': 22,  # 住建局 工作动态
            'http://jsj.zhangzhou.gov.cn/cms/html/zzszfhcxjsj/tzgg3/index.html': 14,  # 住建局 通知公告
            'http://jsj.zhangzhou.gov.cn/cms/html/zzszfhcxjsj/zcfg/index.html': 2,  # 住建局 政策法规
            'http://jsj.zhangzhou.gov.cn/cms/html/zzszfhcxjsj/jzgc/index.html': 7,  # 住建局  建筑工程
            'http://jsj.zhangzhou.gov.cn/cms/html/zzszfhcxjsj/csjs/index.html': 1,  # 住建局  城市建设
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'www.zzgcj' in url:
                xpath = "//tbody/tr[2]/td/table/tbody/tr/td[2]/a"
            else:
                xpath = "//ul[@id='resources']/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath))
                    xpath1=xpath.replace('/li',f'/li[{i}]').replace('r/td[2]/a',f'r[{i}]/td[2]')

                    if 'www.zhangzhou' in url:
                        title = html_1.xpath(f"{xpath1}/p/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        href = html_1.xpath(f"{xpath1}/p/a/@href")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'www.zzgc' in url:
                        publictime = html_1.xpath(f"//tr[2]/td/table/tbody/tr[{i}]/td[3]/text()")[0].strip().replace('[','').replace(']','')
                    else:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','')
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
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
                            link = url + href[2:]
                        elif 'zzgcjyzx' in url:
                            link = 'http://www.zzgcjyzx.com' + href
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('漳州\t', e)
        driver.close()
        return zhangzhou(name)


# todo  南平 公共资源中心 | 发改委 |人民政府 |行政服务中心
def nanping(name):
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
            'http://ggzy.np.gov.cn/npztb/xwzx/008002/':1,  # 工作动态
            'http://ggzy.np.gov.cn/npztb/xwzx/008001/':1,  # 图片新闻
            'http://ggzy.np.gov.cn/npztb/xwzx/008003/':2,  # 通知公告
            'http://ggzy.np.gov.cn/npztb/zcfg/':1,  # 政策法规
            'http://fgw.np.gov.cn/cms/html/fgw/fgyw/index.html':4,  # 发改委 发改动态
            'http://www.np.gov.cn/cms/html/npszf/npyw/index.html':135,  # 人民政府 南平要闻
            'http://www.np.gov.cn/cms/html/npszf/tpxw/index.html':32,  # 人民政府 图片新闻
            'http://www.np.gov.cn/cms/html/npszf/mbkx/index.html':61,  # 人民政府 闽北快讯
            'http://www.np.gov.cn/cms/html/npszf/bmdt1/index.html':53,  # 人民政府 部门动态
            'http://www.np.gov.cn/cms/html/npszf/gsgg/index.html':37,  # 人民政府 公示公告
            'http://www.np.gov.cn/cms/html/npszf/xwfbh/index.html':1,  # 人民政府 新闻发布会
            'http://xzfw.np.gov.cn/news.action?fn=newsList&returnType=jsp&unid=07A103CF4FF3D710E902760F43E6606A&categoryParentUnid=EA4BA3D041117EE5421419B8628E5987&page=1&numPerPage=10&title=':1,  # 行政服务中心 图片新闻
            'http://xzfw.np.gov.cn/news.action?fn=newsList&QXcode=&returnType=jsp&numPerPage=10&unid=ABC9E36AD8426426AA61CC6F607C968A&page=1&categoryParentUnid=EA4BA3D041117EE5421419B8628E5987&title=':4,   # 行政服务中心 中心动态
            'http://xzfw.np.gov.cn/news.action?fn=newsList&QXcode=&returnType=jsp&numPerPage=10&unid=50C2E21311FA3CECF0C9EE3F3E5F38F8&page=1&categoryParentUnid=EA4BA3D041117EE5421419B8628E5987&title=':5,   # 行政服务中心 窗口动态
            'http://xzfw.np.gov.cn/news.action?fn=newsList&QXcode=&returnType=jsp&numPerPage=10&unid=139F3F40F2B9714AEF6EACC0E070EBC7&page=1&categoryParentUnid=EA4BA3D041117EE5421419B8628E5987&title=':4,   # 行政服务中心 县区动态
            'http://zjj.np.gov.cn/cms/html/npszfhcxjsw/gzdt/index.html':8,  # 住建局 工作动态
            'http://zjj.np.gov.cn/cms/html/npszfhcxjsw/tzgg/index.html':9,  # 住建局 通知公告
            'http://zjj.np.gov.cn/cms/html/npszfhcxjsw/aqsc/index.html':4,  # 住建局 工程建设
            'http://zjj.np.gov.cn/cms/html/npszfhcxjsw/jzy/index.html':2,  # 住建局 新闻中心>>建 筑 业
            'http://zjj.np.gov.cn/cms/html/npszfhcxjsw/zcfg/index.html':1,  # 住建局 新闻中心>>政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'fgw' in url:
                xpath="//td[@id='resources']/table/tbody/tr"
            elif 'zjj' in url:
                xpath="//tr/td[@class='listbg'][2]"
            elif 'www' in url:
                xpath="//ul[@id='resources']/li"
            elif 'xzfw' in url:
                xpath="//ul[@class='lw-list']/li"
            else:
                xpath = "//li/a/span[@class='link-content']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    if 'xzfw' in url and i == 1:
                        pass
                    else:
                        if 'fgw' in url:
                            xpath1=xpath.replace('e/t',f'e[{i}]/t')
                            href = html_1.xpath(f'{xpath1}/td[1]/a/@href')[0].strip()
                            title = html_1.xpath(f'{xpath1}/td[1]/a/text()')[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f'{xpath1}/td[2]/text()')[0].strip()
                        elif 'zjj' in url:
                            xpath1=f"//tr[{i}]/td[@class='listbg']"
                            href = html_1.xpath(f'{xpath1}[2]/a/@href')[0].strip()
                            title = html_1.xpath(f'{xpath1}[2]/a/text()')[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f'{xpath1}[3]/text()')[0].strip()
                        elif 'www' in url :
                            href = html_1.xpath(f'{xpath}[{i}]/a/@href')[0].strip()
                            title = html_1.xpath(f'{xpath}[{i}]/a/text()')[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f'{xpath}[{i}]/span/text()')[0].strip()
                        elif 'xzfw' in url:
                                href = html_1.xpath(f'{xpath}[{i}]/a/@href')[0].strip().replace('\n','').replace('\t','').replace('\r','')
                                title = html_1.xpath(f"{xpath}[{i}]/a/span[@class='one']/text()")[0].strip()
                                publictime = html_1.xpath(f"{xpath}[{i}]/a/span[@class='three']/text()")[0].strip()
                        else:
                            href = html_1.xpath(f'//*[@id="categorypagingcontent"]/div/div/ul/li[{i}]/a/@href')[0].strip()
                            title = html_1.xpath(f"//li[{i}]/a/span[@class='link-content']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(f'//*[@id="categorypagingcontent"]/div/div/ul/li[{i}]/a/span[2]/text()')[
                                0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif './' in href:
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                # go = 0
                                # fo = 0
                                # for gjz in gjzs:
                                #     if gjz in title:
                                #         print('含有关键字')
                                #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                #         driver.get(link)
                                #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                #         req_con = driver.page_source
                                #         reqcon = qc_js(req_con)
                                #
                                #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                #         if fj > 0:
                                #             fo += 1
                                #             print(f'有附件{fj}个')
                                #
                                #         go += 1
                                #         driver.back()
                                #         break
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                                # if go > 0:
                                #     Mysql.update_xw_nr(biaoti=title, zt='1')
                                # if fo > 0:
                                #     Mysql.update_xw_xz(biaoti=title, xz='1')
                                # else:
                                #     Mysql.update_xw_xz(biaoti=title, xz='0')
                            if i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                break
                        else:
                            po += 1
                            break

    except Exception as e:
        print('南平\t', e)
        driver.close()
        return nanping(name)

# todo  龙岩 公共资源中心(无响应) | 行政服务中心
def longyan(name):
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
            'https://www.lyggzy.com.cn/lyztb/zcfgnew/':1,  # 政策法规
            'https://www.lyggzy.com.cn/lyztb/tzgg/086001/':3,  #  新罗区  通知公告
            'https://www.lyggzy.com.cn/lyztb/zxfc/093001/':1,  # 新罗区 中心风采
            "http://xzfwzx.longyan.gov.cn/dtxx/zxgg/":3, # 行政服务中心  中心公告
            "http://xzfwzx.longyan.gov.cn/dtxx/zxxw/":8, # 行政服务中心  新闻动态
            'http://zjj.longyan.gov.cn/zwgk/ggtz/':10,  # 住建局 公告通知
            'http://zjj.longyan.gov.cn/zwgk/jsdt/':9,  # 住建局 建设动态
            'http://zjj.longyan.gov.cn/zwgk/flfg/':1,  # 住建局 政策法规

            'http://www.longyan.gov.cn/xw/rd2/': 8,  # 人民政府 新闻 > 热点
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'xzfwzx' in url:
                xpath = "//td[@class='bk'][2]/table[3]/tbody/tr/td[1]"

            elif 'zjj' in url :
                xpath = "//td[@class='bk1']/table[2]/tbody/tr/td[1]"
            elif 'rd2' in url :
                xpath = "//div[@class='zfhy_list']/ul/li"
            else:
                xpath = "//li/a[@class='ellipsis']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, 10):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    if 'xzfwzx' in url  or 'zjj' in url:
                        xpath1=xpath.replace('tr/td[1]',f'tr[{i}]/td')
                        href = html_1.xpath(f"{xpath1}[1]/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}[1]/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'zjj' in url:
                            publictime = html_1.xpath(f"{xpath1}[2]/text()")[0].strip()
                        else:
                            publictime = html_1.xpath(f"{xpath1}[2]/div/font/text()")[0].strip()
                    elif 'rd2' in url:
                        xpath1 = xpath.replace('l/li', f'l/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','')
                    else:
                        href = html_1.xpath(f"//li[{i}]/a[@class='ellipsis']/@href")[0].strip()
                        title = html_1.xpath(f"//li[{i}]/a[@class='ellipsis']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//li[{i}]/span[@class='list-date']/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif './' in href:
                            link =url+ href[2:]
                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            # go = 0
                            # fo = 0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link,f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon = qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo += 1
                            #             print(f'有附件{fj}个')
                            #
                            #         go += 1
                            #         driver.back()
                            #         break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #  Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try: driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('龙岩\t', e)
        driver.close()
        return longyan(name)

# todo   龙岩 发改委 | 人民政府(ij)
def longyan1(name):
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
            'http://fgw.longyan.gov.cn/zwgk/fgdt/':19,  # 发改委 工作动态
            'http://fgw.longyan.gov.cn/zwgk/gggs/':2,  # 发改委 公告公示
            'http://fgw.longyan.gov.cn/zwgk/zcwj/':2,  # 发改委 政策文件
            'http://www.longyan.gov.cn/xw/yw2/':34,  # 人民政府 新闻 > 要闻
            'http://www.longyan.gov.cn/xw/mt2/':33,  # 人民政府 新闻 >媒体
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'fgw' in url :
                xpath = "//div[@class='zhong_con_r_ul']/ul/li"
                jj = 5
            else:
                xpath = "//div[@class='zfhy_list']/ul/li"
                jj = 4
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                time.sleep(1)
                if po > 0:
                    break
                for j in range(1, jj):
                    for i in range(1, 6):
                        lengt = len(html_2.xpath(xpath))
                        xpath1 = xpath.replace('/ul/li', f'/ul[{j}]/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
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
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                # go = 0
                                # fo = 0
                                # for gjz in gjzs:
                                #     if gjz in title:
                                #         print('含有关键字')
                                #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                #         driver.get(link)
                                #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                #         req_con = driver.page_source
                                #         reqcon = qc_js(req_con)
                                #
                                #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                #         if fj > 0:
                                #             fo += 1
                                #             print(f'有附件{fj}个')
                                #
                                #         go += 1
                                #         driver.back()
                                #         break
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                                # if go > 0:
                                #     Mysql.update_xw_nr(biaoti=title, zt='1')
                                # if fo > 0:
                                #     Mysql.update_xw_xz(biaoti=title, xz='1')
                                # else:
                                #     Mysql.update_xw_xz(biaoti=title, xz='0')
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('>'))
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('龙岩1\t', e)
        driver.close()
        return longyan1(name)


# todo   宁德(ij)  公共资源中心(无响应)  |发改委 | 住建局 |人民政府
def ningde(name):
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
            'http://fgw.ningde.gov.cn/xwdt/gzdt/':12,  # 发改委 > 工作动态
            'http://fgw.ningde.gov.cn/xwdt/tpxx/':4,  # 发改委 > 图片信息
            'http://fgw.ningde.gov.cn/xxgk/gsgg/tzgg/':7,  # 发改委 > 通知公告
            'http://zjj.ningde.gov.cn/zwgk/gzdt/':22,  # 住建局 >  工作动态
            'http://zjj.ningde.gov.cn/zwgk/tzgg/':24,  # 住建局 >  通知公告
            'http://zjj.ningde.gov.cn/zwgk/zcjd/':1,  # 住建局 >  政策解读
            'http://www.ningde.gov.cn/zwgk/gzdt/jryw/':126,  # 人民政府 > 今日要闻
            'http://www.ningde.gov.cn/zwgk/gzdt/bmdt/':179,  # 人民政府 > 部门动态
            'http://www.ningde.gov.cn/zwgk/gzdt/qxdt/':140,  # 人民政府 > 区县动态
            'http://www.ningde.gov.cn/zwgk/gzdt/zyhy/':16,  # 人民政府 > 重要会议
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'fgw' in url or 'zjj' in url:
                xpath="//div[1]/div/ul/li"
                jj = 4
            else:
                xpath = "//div[1]/ul[@class='list-1 borbot']/li"
                jj = 4
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
                        xpath1 = xpath.replace('v/ul/li',f'v[{j}]/ul/li[{i}]').replace("ot']/li",f"ot'][{j}]/li[{i}]")
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[','').replace(']','')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
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
                                link = url + href[2:]
                            elif href[0] == '/':
                                link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                            else:
                                link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('>'))
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('宁德\t', e)
        driver.close()
        return ningde(name)
# todo  宁德  行政服务中心
def ningde1(name):
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
            'http://ggzyjy.xzfw.ningde.gov.cn/ywgg/noticePage.html':2,  # 宁德市公共资源交易中心 > 公告通知
            "http://xzfw.ningde.gov.cn/icity/icity/pub/index?name=zxxw":17, # 行政服务中心  工作动态
            "http://xzfw.ningde.gov.cn/icity/icity/pub/index?name=tzgg":3, # 行政服务中心  通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'ggzyjy' in url:
                xpath = "//ul[@id='info']/li/div[1]"
            else:
                xpath = "//div[@id='pub_index_detail']/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, 10):
                time.sleep(1)
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_2.xpath(xpath)) + 1
                    xpath1=xpath.replace('/li',f'/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif './' in href:
                            link =url+ href[2:]

                        elif href[0] == '/':
                            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn' + href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            # go = 0
                            # fo = 0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link,f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon = qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo += 1
                            #             print(f'有附件{fj}个')
                            #
                            #         go += 1
                            #         driver.back()
                            #         break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #  Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try: driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('宁德1\t', e)
        driver.close()
        return ningde1(name)



from threading import Thread
#
t0 = Thread(target=fujian, args=("福建",))
t00 = Thread(target=fujian1, args=("福建",))
t10 = Thread(target=fuzhou, args=("福州",))
t100 = Thread(target=fuzhou1, args=("福州",))  # 超出范围
t1 = Thread(target=xiamen, args=("厦门",))
t11 = Thread(target=xiamen1, args=("厦门",))
t111 = Thread(target=xiamen2, args=("厦门",))
t2 = Thread(target=sanming, args=("三明",))
t22 = Thread(target=sanming1, args=("三明",))
t222 = Thread(target=sanming2, args=("三明",))
t3 = Thread(target=quanzhou, args=("泉州",))
t33 = Thread(target=quanzhou1, args=("泉州",))
t4 = Thread(target=zhangzhou, args=("漳州",))
t5 = Thread(target=nanping, args=("南平",))
t6 = Thread(target=longyan, args=("龙岩",))
t66 = Thread(target=longyan1, args=("龙岩",))
t7 = Thread(target=ningde, args=("宁德",))
t77 = Thread(target=ningde1, args=("宁德",))


# def ready1():
#     threadl = [
#         t0,t00 ,t10,t100,
#         t1,
#         t11,
#         t111, t2, t22, t222,
#         t3, t33, t4,t5, t6, t66, t7,t77
#                ]
#     for x in threadl:
#         x.start()
# ready1()
# t100.start()
# t7.start()


fujian('福建')
fujian1('福建')
fuzhou('福州')
fuzhou1('福州')
xiamen('厦门')
xiamen1('厦门')
xiamen2('厦门')
sanming('三明')
sanming1('三明')
sanming2('三明')
quanzhou('泉州')
quanzhou1('泉州')
zhangzhou('漳州')
nanping('南平')
longyan('龙岩')
longyan1('龙岩')
ningde('宁德')
ningde1('宁德')