import time, html, uuid,requests,json
from dao import Mysql
from lxml import etree
from selenium import webdriver
import urllib.request
from urllib.parse import quote
from datetime import datetime
from bs4 import BeautifulSoup
from openpyxl import load_workbook
import re, os, itertools, shutil

gjzs = ['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子', '保险']
now = datetime.now()
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
    except Exception as e:
        print('蚌埠\t', e)
pro = '湖南'
# 爬取#近一個月
# jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 15
jiezhi_time = int(time.mktime(time.strptime('2019-01-01', "%Y-%m-%d")))

# todo  湖南 公共资源中心 |发改委 |产权交易  |住建局
def hunan(name):
    try:
        city = '湖南'
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        # chromeOptions.add_argument(('--proxy-server=' + str(ipmax())))
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

        urls = {
            'https://www.hnsggzy.com/zyxw/index.jhtml': 115,  # 公共资源中心 重要新闻
            'https://www.hnsggzy.com/tzgg/index.jhtml': 20,  # 公共资源中心 通知公告
            'https://www.hnsggzy.com/zcfggc/index.jhtml': 1,  # 公共资源中心 政策法规
            'http://fgw.hunan.gov.cn/fgw/tslm_77952/hgzh/index.html': 25,  # 发改委 时政要闻
            'http://113.246.57.9:9013/common/search/70909': 20,  # 发改委 通知公告
            'http://113.246.57.9:9013/common/search/70906': 43,  # 发改委 工作动态
            'http://www.hnaee.com/hnaee/1/2/default.htm': 12,  # 产权交易 > 本所动态
            'http://www.hnaee.com/hnaee/1/3/default.htm': 2,  # 产权交易 > 行业新闻
            'http://zjt.hunan.gov.cn/zjt/xxgk/tzgg/index.html': 20,  # 住建局 > 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'common' in url:
                xpath = "//li/div/a"
                xy = "//a[@class='next']"
            elif 'fgw' in url:
                xpath = "//ul[@class='tyl-main-right-list-a']/li/a"
                xy = "//li[@class='prev_page'][2]/a"
            elif 'hnaee' in url:
                xpath = "//div[@class='neirong']/ul/li/a"
                xy = "//div[@id='pagination']/span/a[1]"
            elif 'zjt' in url:
                xpath = "//tr/td[2]"
                xy = "//li[@class='prev_page'][2]/a"
            else:
                xpath = "//li/div/a"
                xy = "//div[@class='list-box-b']/a[3]"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break

                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]/').replace('//li/div/a', f'//li[{i}]/div/').replace('r/td[2]', f'r[{i}]/td[2]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    if 'common' in url:
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('[通知公告 ]  ', '').replace(
                            '[政务动态 ]  ', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//li[{i}]/div[@class='date']/text()")[0].strip()
                    elif 'fgw' in url:
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            publictime = html_1.xpath(f'/html/body/div[3]/div/div/div/div[4]/div[2]/ul/li[{i}]/span/text()')[0].strip()
                        except:
                            publictime = html_1.xpath(f'//*[@id="CBody"]/div[4]/div/div/div/div[4]/div[2]/ul/li[{i}]/span/voice/text()')[0].strip()
                    elif 'hnsggzy' in url:
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('[通知公告 ]  ', '').replace(
                            '[政务动态 ]  ', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//li[{i}]/div/div[@class='list-times']/text()")[0].strip()
                    elif 'zjt' in url:
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//tr[{i}]/td[3]/text()")[0].strip()
                    else:
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime.replace('.', '-'), "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif 'hnaee' in url:
                            link = url.replace('default.htm','')+href
                        else:
                            link = 'http' + re.findall(r'http(.*?)\.gov', url)[0] + '.gov.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            Mysql.update_xw_url(url=link,biaoti=title)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                xy="//li[@class='next_page']/a"
                                xy1="//ul[@class='pages-list']/li[10]/a"
                                if len(html_1.xpath(xy))>0:
                                    driver.find_element_by_xpath(xy).click()
                                elif len(html_1.xpath(xy1))>0:
                                    driver.find_element_by_xpath(xy1).click()
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
        print('蚌埠\t', e)
        driver.close()
        return hunan(name)


# todo  湖南 人民政府
def hunan1(name):
    try:
        city = '湖南'
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
            'http://www.hunan.gov.cn/hnszf/hnyw/sy/hnyw1/gl_fgsjpx.html': 5,  # 人民政府 湖南要闻
            'http://www.hunan.gov.cn/hnszf/xxgk/tzgg/swszf/tzgg_rb.html': 1,  # 人民政府 通知公告 > 省委、省政府
            'http://www.hunan.gov.cn/hnszf/xxgk/tzgg/szbm/tzgg_rb.html': 25,  # 人民政府 通知公告 > 省直部门
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'tzgg' in url:
                ii=6
                xpath = "//div[@class='ty-list clearfix']/ul/li/a"
            else:
                ii=7
                xpath = "//div[@class='yl-listbox']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, ii):
                    for j in range(1, 4):
                        lenth = len(html_2.xpath(xpath))
                        xpath1=xpath.replace('ul/li/a',f'ul[{j}]/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'http://www.hunan.gov.cn' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()

                                chuli(publictime,href,driver,url,title,city,xpath1)
                            else:
                                print(f'【{title}】已存在')
                            if (j - 1) * 5 + i == lenth:
                                if lenth < length - 1:
                                    break
                                else:
                                    # t = 0
                                    # for pp in range(5, 9):
                                    #     xy = f"//div[@class='jspIndex4']/a[{pp}]"
                                    #     if html_1.xpath(xy + '/text()')[0] == '>':
                                    #         t += 1
                                    #         driver.find_element_by_xpath(xy).click()
                                    #         break
                                    # if t == 0 and int(pages) != 1:
                                    #     print('点击下一页出错了')
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('>'))
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return hunan1(name)


# hunan1('湖南')

# todo  长沙 公共资源中心 | 人民政府 | 住建局
def changsha(name):
    try:
        city = '长沙'
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
            'http://csggzy.changsha.gov.cn/xxgk/gzdt/': 22,  # 公共资源中心 政务要闻
            'http://csggzy.changsha.gov.cn/xxgk/tzgg/': 6,  # 公共资源中心 通知公告
            'http://www.changsha.gov.cn/szf/ywdt/zwdt/': 50,  # 人民政府 政务动态
            'http://www.changsha.gov.cn/szf/ywdt/tpxx/': 21,  # 人民政府 图片新闻
            'http://www.changsha.gov.cn/szf/tzgg/': 3,  # 人民政府 通知公告
            'http://www.changsha.gov.cn/jdhy/zcjd/': 5,  # 人民政府 通知公告
            'http://szjw.changsha.gov.cn/zfxxgk/gzdt/zhdt/': 20,  # 住建局 综合动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='bd_new bd_a80 right_list']/ul/li/a"
                length = 24
            elif 'szjw' in url:
                xpath = "//div[@class='bd_new bd_a80 right_list']/ul/li/a"
                length = 36
            else:
                xpath = "//div[@class='list-box show']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):

                    lengt = len(html_1.xpath(xpath))
                    if 'www' in url and i % 6 == 0:
                        pass
                    else:
                        if 'szjw' in url:
                            ii = i * 2 - 1
                            xpath1 = xpath.replace('i/a', f'i[{ii}]/')
                        else:
                            xpath1 = xpath.replace('i/a', f'i[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'csggzy' in url:
                            publictime = html_1.xpath(f"{xpath1}i/text()")[0].strip()[1:-1]
                        else:
                            publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()

                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if re.findall('http', href):
                                link = href
                            elif './'in href:
                                link = url+href.replace('./','')
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
                            else:
                                link = 'http' + re.findall(r'http(.*?)\.gov', url)[0] + '.gov.cn/'+href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                chuli(publictime,href,driver,url,title,city,xpath1)
                            else:
                                Mysql.update_xw_url(url=link, biaoti=title)
                            if 'www' not in url and i == lengt or ('www' in url and i == lengt + 3):
                                if lengt < len(html_2.xpath(xpath)):
                                    break
                                else:
                                    if page!=pages:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                    # if 'www' in url:
                                    #     xy = f"//div[@class='div_cutPage']/a[{page + 1}]"
                                    # else:
                                    #     xy = "//div[@class='list-box-b']/a[3]"
                                    # if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[
                                    #     0] == '下一页':
                                    #     driver.find_element_by_xpath(xy).click()
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return changsha(name)
# todo  长沙 行政审批局 | 发改委
def changsha1(name):
    try:
        city = '长沙'
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
            'http://xzspj.changsha.gov.cn/zfxxgk/zwdt/gzdt1/': 27,  # 行政审批局 工作动态
            'http://xzspj.changsha.gov.cn/zfxxgk/zwdt/tzgg1/': 3,  # 行政审批局 通知公告
            'http://fgw.changsha.gov.cn/zfxxgk/gzdt_38518/gzdt/': 33,  # 发改委 工作动态
            'http://fgw.changsha.gov.cn/zfxxgk/gzdt_38518/qxdt/': 5,  # 发改委 区县动态
            'http://fgw.changsha.gov.cn/zfxxgk/gzdt_38518/szyw/': 5,  # 发改委 时政要闻
            'http://fgw.changsha.gov.cn/zfxxgk/gzdt_38518/tpxw_31443/': 8,  # 发改委 图片新闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//ul[@class='list_ul']/li/a"
            else:
                xpath = "//div[@class='zwgk-main-right-mainmain']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+ 1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/a', f'[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'fgw' in url:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    else:
                        publictime = html_1.xpath(f"{xpath1}/p/text()")[0].strip()
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
                            link = url+href.replace('./','')

                        else:
                            link = 'http' + re.findall('http(.*?)cn', url)[0] + 'cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            Mysql.update_xw_url(url=link, biaoti=title)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                          driver.find_element_by_link_text('>'))
                                # xy = "//a[@class='next']"
                                #
                                # if len(html_1.xpath(xy)) > 1:
                                #     driver.find_element_by_xpath(xy+'[1]').click()
                                # elif len(html_1.xpath(xy)) > 0:
                                #     driver.find_element_by_xpath(xy).click()

                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return changsha1(name)


# changsha1('长沙')

# todo  株洲 公共资源中心
def zhuzhou(name):
    try:
        city = '株洲'
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
            'http://www.zzzyjy.cn/011/secondPage.html': 2,  # 公共资源中心 重要通知
            'http://www.zzzyjy.cn/010/secondPage.html': 15,  # 公共资源中心 本埠资讯
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//li[@class='ewb-list-node clearfix']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_2.xpath(xpath))
                    xpath1 = xpath.replace('/a', f'[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}a/text()")[1].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http' + re.findall('http(.*?)cn', url)[0] + 'cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            print(f'【{title}】已存在')
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('>'))
                            break

                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return zhuzhou(name)


# todo  株洲 行政审批局 | 发改委 | 人民政府 |住建局
def zhuzhou1(name):
    try:
        city = '株洲'
        print(f"{name}程序已启动，稍等几秒")
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,
                                  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://xzspfwj.zhuzhou.gov.cn/c13285/index.html': 4,  # 行政审批局 工作动态
            'http://fgw.zhuzhou.gov.cn/c14780/index.html': 10,  # 发改委 头条新闻
            'http://fgw.zhuzhou.gov.cn/c14781/index.html': 10,  # 发改委 本委动态
            'http://fgw.zhuzhou.gov.cn/c14782/index.html': 10,  # 发改委 时事要闻
            'http://fgw.zhuzhou.gov.cn/c14783/index.html': 10,  # 发改委 区县发改
            'http://fgw.zhuzhou.gov.cn/c14784/index.html': 3,  # 发改委 通知公告
            "http://www.zhuzhou.gov.cn/c15124/index.html": 166,  # 人民政府 工作动态
            "http://www.zhuzhou.gov.cn/c15125/index.html": 66,  # 人民政府 部门动态
            "http://www.zhuzhou.gov.cn/c15126/index.html": 108,  # 人民政府 市县区动态
            "http://www.zhuzhou.gov.cn/c15654/index.html": 3,  # 人民政府 最新发布
            "http://www.zhuzhou.gov.cn/c15659/index.html": 3,  # 人民政府 发布预告
            "http://www.zhuzhou.gov.cn/c15152/index.html": 1,  # 人民政府 政策解读
            "http://zjj.zhuzhou.gov.cn//c13824/index.html": 10,  # 住建局 工作动态
            "http://zjj.zhuzhou.gov.cn//c13825/index.html": 10,  # 住建局 通知公告
            "http://zjj.zhuzhou.gov.cn//c13884/index.html":2,  # 住建局 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'c15152' in url:
                xpath = "//div[@class='xxgk-list']/ul/li"
                ll = 15
            elif 'fgw' in url:
                xpath = "//ul[@class='uli14 nowrapli list-date padding-hz-5 list-dashed']/li/a"
                ll = 15
            elif 'www' in url:
                xpath = "//ul[@id='news_list']/li/a"
                ll = 15
            elif 'zjj' in url:
                xpath = "//div[@class='xxgk-list']/ul/li/a"
                ll = 15
            else:
                xpath = "//ul[@class='list']/li/a"
                ll = 10
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/li/a', f'/li[{i}]/')
                    if 'c15152' in url:
                        href = html_1.xpath(f"{xpath}[{i}]/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}[{i}]/a/voice[@class='Voice-Voicer-Pointer-Label']/text()")[
                            0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = \
                            html_1.xpath(f"{xpath1}[{i}]/span/voice[@class='Voice-Voicer-Pointer-Label']/text()")[
                                0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if re.findall('\./', href):
                            link = href[2:]
                        elif re.findall('http', href):
                            link = href
                        else:
                            link = 'http' + re.findall('(.*?)\.gov.cn', url)[0] + '.gov.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                # xy = "//div[@id='pages']/a[@class='next']"
                                # if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[0] == '>':
                                #     driver.find_element_by_xpath(xy).click()
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return zhuzhou1(name)


# zhuzhou1('株洲')


# todo  湘潭 公共资源中心 | 发改委 | 住建局
def xiangtan(name):
    try:
        city = '湘潭'
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
            'http://ggzy.xiangtan.gov.cn/2451/2464/2465/index.htm': 14,  # 公共资源中心 工作动态
            'http://ggzy.xiangtan.gov.cn/2451/2464/2466/index.htm': 4,  # 公共资源中心 通知公告
            'http://ggzy.xiangtan.gov.cn/2451/2464/18056/index.htm': 1,  # 公共资源中心 图片新闻
            'http://xtfgw.xiangtan.gov.cn/13153/13160/13168/index.htm': 24,  # 发改委 动态信息
            'http://xtfgw.xiangtan.gov.cn/13153/13160/13169/index.htm': 4,  # 发改委 通知公告
            'http://xtjs.xiangtan.gov.cn/6512/6518/6527/index.htm': 23,  # 住建局 动态信息
            'http://xtjs.xiangtan.gov.cn/6512/6518/6528/index.htm': 6,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//tr/td[2]/a"

            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1=xpath.replace("//tr/td[2]/a",f"//tr[{i}]/td[2]")
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    try:
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    except:
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(xpath1.replace('td[2]','td[3]')+f"/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                # t = 0
                                # for pp in range(5, 9):
                                #     xy = f"//div[@class='jspIndex4']/a[{pp}]"
                                #     if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[0] == '>':
                                #         t += 1
                                #         driver.find_element_by_xpath(xy).click()
                                #         break
                                # if t == 0 and pages != 1:
                                #     print('点击下一页出错了')
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return xiangtan(name)


# todo  湘潭 人民政府
def xiangtan1(name):
    try:
        city = '湘潭'
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
            'http://www.xiangtan.gov.cn/109/171/172/index.htm': 149,  # 人民政府 政务新闻
            'http://www.xiangtan.gov.cn/109/171/173/index.htm': 233,  # 人民政府 区县动态
            'http://www.xiangtan.gov.cn/109/171/174/index.htm': 203,  # 人民政府 部门动态
            'http://www.xiangtan.gov.cn/109/181/index.htm': 7,  # 人民政府 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//ul[@class='s_list']/li/a"
            length = len(html_2.xpath(xpath)) + 1

            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, 6):
                    for j in range(1, 5):
                        lenth = len(html_2.xpath(xpath))
                        xpath1=xpath.replace("t']/li/a",f"t'][{j}]/li[{i}]/")
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        if re.findall('http', href):
                            link = href
                        else:
                            link=url.replace('index.htm','')+href
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            if select == None:
                                uid = uuid.uuid4()
                                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')

                            else:
                                Mysql.update_xw_url(url=link, biaoti=title)
                            if (j - 1) * 5 + i == lenth:
                                if lenth < length - 1:
                                    break
                                else:

                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('>'))
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return xiangtan1(name)


# xiangtan('湘潭')

# todo  衡阳 公共资源中心 | 发改委 | 人民政府 |住建局
def hengyang(name):
    try:
        city = '衡阳'
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
            'http://ggzy.hengyang.gov.cn/xwzx/xwdt/index.html': 4,  # 中心要闻
            'http://ggzy.hengyang.gov.cn/xwzx/tzgg/index.html': 3,  # 通知公告
            'http://ggzy.hengyang.gov.cn/xwzx/xyxx/index.html': 1,  # 行业信息
            'http://fgw.hengyang.gov.cn/xxgk/gzdt/gzdt/index.html': 2,  # 发改委 工作动态
            'http://fgw.hengyang.gov.cn/xxgk/gzdt/tpzx/index.html': 1,  # 发改委 图片资讯
            'http://fgw.hengyang.gov.cn/xxgk/gzdt/tzgg/index.html': 2,  # 发改委 通知公告
            'http://www.hengyang.gov.cn/xxgk/dtxx/ttxx/index.html': 19,  # 人民政府 头条信息
            'http://www.hengyang.gov.cn/xxgk/dtxx/tpxw/index.html': 50,  # 人民政府 图片新闻
            'http://www.hengyang.gov.cn/xxgk/dtxx/hydt/index.html': 50,  # 人民政府 衡阳动态
            'http://www.hengyang.gov.cn/xxgk/dtxx/bmdt/index.html': 50,  # 人民政府 部门动态
            'http://www.hengyang.gov.cn/xxgk/dtxx/xsqdt/index.html': 50,  # 人民政府 县市区动态
            'http://www.hengyang.gov.cn/xxgk/dtxx/tzgg/index.html': 50,  # 人民政府 通知公告
            'http://zjw.hengyang.gov.cn/xxgk/gzdt/tzgg/index.html': 9,  # 住建局 通知公告
            'http://zjw.hengyang.gov.cn/xxgk/gzdt/zjyw/index.html': 2,  # 住建局  住建要闻
            'http://zjw.hengyang.gov.cn/xxgk/gzdt/tpzx/index.html': 1,  # 住建局   图片资讯
            'http://zjw.hengyang.gov.cn/xxgk/zcwjjjd/zcjgfxwj/index.html': 1,  # 住建局  政策文件及解读 > 政策及规范性文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'www' in url:
                xpath = "//ul[@class='qiexian']/li/a"
            elif 'zjw' in url:
                xpath = "//ul[@class='tz_con']/li/a"
            else:
                xpath = "//li[@class='nyLine']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace('/a', f'[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if re.findall('http', href):
                            link = href
                        else:
                            link = 'http' + re.findall('(.*?)\.gov.cn', url)[0] + '.gov.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                xy = "//div[@id='pages']/a[@class='next']"
                                if html_1.xpath(xy + '/text()')[0] == '>':
                                    driver.find_element_by_xpath(xy).click()
                                if page != pages:
                                    try:
                                        xy = "//td[contains(string(),'下页')]"
                                        driver.find_element_by_xpath(xy).click()
                                    except:
                                        xy = "//div[@id='pages']/a[@class='next']"
                                        if html_1.xpath(xy + '/text()')[0] == '>':
                                            driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return hengyang(name)


# todo  邵阳 公共资源中心 | 住建局
def shaoyang(name):
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
            'https://ggzy.shaoyang.gov.cn/newsList.html?index=2&type=%E4%BF%A1%E6%81%AF%E5%85%AC%E5%BC%80&xtype=%E6%96%B0%E9%97%BB%E4%B8%AD%E5%BF%83': 8,
            # 新闻动态
            'https://ggzy.shaoyang.gov.cn/newsList.html?index=2&type=%E4%BF%A1%E6%81%AF%E5%85%AC%E5%BC%80&xtype=%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A': 3,
            # 通知公告
            'https://zj.shaoyang.gov.cn/zj/zjyw/list.shtml': 8,  # 住建局 住建要闻
            'https://zj.shaoyang.gov.cn/zj/tzgg/list.shtml': 8,  # 住建局 通知公告
            'https://zj.shaoyang.gov.cn/zj/jzgcgl/list.shtml': 2,  # 住建局  建筑工程管理
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'zj' in url:
                xpath = "//div[@class='nylb']/ul/li/a"
            else:
                xpath = "//ul[@id='list']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(2, length):
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace('/a', f'[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if re.findall('http', href):
                            link = href
                        else:
                            link = 'http' + re.findall(r'http(.*?)\.gov', url)[0] + '.gov.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                                # if 'zj' in url:
                                #     for pp in range(2, 4):
                                #         xy = f"//div[@class='pagination_index'][{pp}]/span/a"
                                #         if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[
                                #             0] == '下一页':
                                #             driver.find_element_by_xpath(xy).click()
                                #             break
                                # else:
                                #     xy = "//a[@class='pageNum'][10]"
                                #     if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[
                                #         0] == '下一页':
                                #         driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return shaoyang(name)


# todo  邵阳   行政审批局  | 发改委
def shaoyang1(name):
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
            'https://zwzx.shaoyang.gov.cn/zwzx/gzdt/gzdt.shtml': 55,  # 工作动态
            'https://zwzx.shaoyang.gov.cn/zwzx/tzgg/list0.shtml': 3,  # 通知公告
            'https://zwzx.shaoyang.gov.cn/zwzx/zcfg/list.shtml': 2,  # 政策法规
            'https://fgw.shaoyang.gov.cn/fgw/tzgg/list_no.shtml': 6,  # 发改委 通知公告
            'https://fgw.shaoyang.gov.cn/fgw/gzdt/list_no.shtml': 9,  # 发改委 工作动态
            'https://fgw.shaoyang.gov.cn/fgw/zwgk/list.shtml': 2,  # 发改委 政务公开
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)

            if 'gzdt' in url:
                xpath = "//ul[@id='tab_xwqh_1']/li/a"
                ks = 2
            elif 'fgw' in url:
                xpath = "//div[@class='nylist']/ul/li/a"
                ks = 1
            else:
                xpath = "//dl/dd/a"
                ks = 1
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(ks, length):

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]/').replace('//dl/dd/a', f'//dl[{i}]/dd/')
                    if 'gzdt' in url or 'fgw' in url:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(xpath1.replace('dd/',"dd[@class='nydate']")+f"/text()")[0].strip()[3:13]
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                                # xy = "//div[@class='pagination_index'][2]/span/a"
                                # if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[0] == '下一页':
                                #     driver.find_element_by_xpath(xy).click()
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return shaoyang1(name)


# todo  岳阳   公共资源中心 | 人民政府  | 发改委 |住建局
def yueyang(name):
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
            'http://ggzy.yueyang.gov.cn/55993/index.htm': 6,  # 公共资源中心 中心动态
            'http://ggzy.yueyang.gov.cn/56113/index.htm': 1,  # 公共资源中心 政策法规
            'http://fgw.yueyang.gov.cn/8739/8740/default.htm': 10,  # 发改委 工作动态
            'http://fgw.yueyang.gov.cn/8739/8742/default.htm': 6,  # 发改委 通知公告
            'http://www.yylq.gov.cn/21487/21488/21499/default.htm': 50,  # 人民政府 政务动态
            'http://www.yylq.gov.cn/21487/21488/21743/default.htm': 40,  # 人民政府 部门动态
            'http://www.yylq.gov.cn/21487/21490/21504/default.htm': 6,  # 人民政府 通知公告
            'http://www.yueyang.gov.cn/jsj/54027/54028/54036/index.htm': 4,  # 住建局 行业动态
            'http://jsj.yueyang.gov.cn/54027/54028/54035/index.htm': 7,  # 住建局 建设动态
            'http://jsj.yueyang.gov.cn/54027/54028/54042/index.htm': 1,  # 住建局 政策法规
            'http://jsj.yueyang.gov.cn/54027/54028/54039/index.htm': 3,  # 住建局 通知
            'http://jsj.yueyang.gov.cn/54027/54028/54040/index.htm': 1,  # 住建局 建设文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)

            if 'fgw' in url:
                xpath = "//tr/td[@class='line4'][2]"
            elif 'www' in url:
                xpath = "//ul[@class='m-gl-list-t m-list-t-skin-1']/li/a"
            elif 'jsj' in url:
                xpath = "//ul[@class='news-list']/li/a"
            else:
                xpath = "//ul[@class='list']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]').replace('r/t', f'r[{i}]/t')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'fgw' in url:
                        publictime = html_1.xpath(f"//tr[{i}]/td[@class='line4'][3]/text()")[0].strip()
                    else:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
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
                        else:
                            link = url.replace('default.htm', '').replace('index.htm', '') + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            Mysql.update_xw_url(url=link,biaoti=title)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                                # if 'www' in url:
                                #     xy = "//span[@class='next'][3]"
                                # else:
                                #     xy = "//div[@id='pagination']/a[1]"
                                # if len(html_1.xpath(xy)) > 0:
                                #     driver.find_element_by_xpath(xy).click()
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return yueyang(name)


# todo  常德   公共资源中心 | 人民政府  | 发改委（有问题） | 住建局
def changde(name):
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
            'http://ggzy.changde.gov.cn/tzgg': 1,  # 公共资源中心 通知公告
            'http://ggzy.changde.gov.cn/gzdt': 1,  # 公共资源中心 工作动态
            'https://www.changde.gov.cn/cdzx/cdyw': 192,  # 人民政府 常德要闻
            'https://www.changde.gov.cn/cdzx/bmdt': 51,  # 人民政府 部门动态
            'https://www.changde.gov.cn/cdzx/qxdt': 51,  # 人民政府 区县动态
            'https://www.changde.gov.cn/cdzx/gsgg': 13,  # 人民政府 公示公告
            'http://zfjsw.changde.gov.cn/zhdt/gzdt': 1,  # 住建局 工作动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)

            xpath = "//ul[@class='newsList']/li/a"
            if 'www' in url:
                length = 24
            else:
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if ('www' in url or 'zfjsw' in url) and i % 6 == 0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            if select == None:
                                chuli(publictime,href,driver,url,title,city,xpath1)
                            if i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('>'))
                                    # xy = "//a[@class='next']"
                                    # if len(html_1.xpath(xy)) > 0:
                                    #     driver.find_element_by_xpath(xy).click()
                        else:
                            po += 1
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return changde(name)


# todo  张家界   公共资源中心 | 人民政府  | 发改委（有问题） | 住建局
def zhangjiajie(name):
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

        urls = {
            'http://www.zjjsggzy.gov.cn/Home/NewsList?index=1&type=%E6%96%B0%E9%97%BB%E8%B5%84%E8%AE%AF&xtype=%E9%87%8D%E8%A6%81%E6%96%B0%E9%97%BB': 5,
            # 公共资源中心 重要新闻
            'http://www.zjjsggzy.gov.cn/Home/NewsList?index=1&type=%E6%96%B0%E9%97%BB%E8%B5%84%E8%AE%AF&xtype=%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A': 1,
            # 公共资源中心 通知公告
            'http://www.zjjsggzy.gov.cn/Home/NewsList?index=1&type=%E6%96%B0%E9%97%BB%E8%B5%84%E8%AE%AF&xtype=%E8%A1%8C%E4%B8%9A%E5%8A%A8%E6%80%81': 4,
            # 公共资源中心 行业动态
            'http://www.zjj.gov.cn/c32/index.html': 13,  # 人民政府 新闻中心
            'http://www.zjj.gov.cn/c33/index.html': 30,  # 人民政府 区县联播
            'http://www.zjj.gov.cn/c34/index.html': 30,  # 人民政府 部门动态
            'http://www.zjj.gov.cn/c37/index.html': 15,  # 人民政府 通知公告
            'http://fgw.zjj.gov.cn/c723/index.html': 5,  # 发改委 工作动态
            'http://fgw.zjj.gov.cn/c6686/index.html': 5,  # 发改委 通知公告
            'http://fgw.zjj.gov.cn/c6689/index.html': 1,  # 发改委 政策解读
            'http://zjj.zjj.gov.cn/c1155/index.html': 13,  # 住建局 通知公告
            'http://zjj.zjj.gov.cn/c6655/index.html': 5,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'www.zjj' in url:
                xpath = "//ul[@id='list']/li/a"
            else:
                xpath = "//ul[@class='clear']/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                driver.set_page_load_timeout(4)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    if 'www.zjj' in url:
                        xpath1 = xpath.replace('i/a', f'i[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '')
                    else:
                        href = html_1.xpath(f"{xpath}[{i}]/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath}[{i}]/a/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath}[{i}]/i/text()")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    if len(publictime)>12:
                        break
                    else:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if re.findall('http', href):
                            link = href
                        else:
                            link = 'http' + re.findall('http(.*?)cn', url)[0] + 'cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                # t = 0
                                # if 'zjjsggzy' in url:
                                #     for pp in range(8, 13):
                                #         xy = f"//a[@class='pageNum'][{pp}]"
                                #         if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[
                                #             0] == '下一页':
                                #             t += 1
                                #             driver.find_element_by_xpath(xy).click()
                                #             break
                                #     if t == 0 and pages != 1:
                                #         print('点击下一页出错了')
                                # else:
                                #     xy = "//a[@class='next']"
                                #     driver.find_element_by_xpath(xy).click()

                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        from selenium.common.exceptions import TimeoutException
        try:
            print('蚌埠\t', e)
            driver.close()
            return zhangjiajie(name)

        except TimeoutException:
            # 报错后就强制停止加载
            # 这里是js控制
            driver.execute_script('window.stop()')
            print(driver.page_source)


# todo  益阳   公共资源中心 | 人民政府  | 发改委（有问题） | 住建局
def yiyang(name):
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
            'http://jyzx.yiyang.gov.cn/ggzyjy/31063/31073/index.htm': 8,  # 益阳市公共资源交易中心 工作动态
            'http://jyzx.yiyang.gov.cn/ggzyjy/31063/31072/index.htm': 2,  # 益阳市公共资源交易中心 通知公告
            'http://jyzx.yiyang.gov.cn/ggzyjy/31063/31074/index.htm': 6,  # 益阳市公共资源交易中心 时事要闻
            'http://www.yiyang.gov.cn/yiyang/2/3/72/default.htm': 122,  # 人民政府 政务要闻
            'http://www.yiyang.gov.cn/yiyang/2/3/73/default.htm': 243,  # 人民政府 部门动态
            'http://www.yiyang.gov.cn/yiyang/2/3/74/default.htm': 245,  # 人民政府 区县市动态
            'http://www.yiyang.gov.cn/yiyang/2/3/4/default.htm': 11,  # 人民政府  公示公告
            'http://www.yiyang.gov.cn/yiyang/2/78/99/default.htm': 2,  # 人民政府   政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//ul[@class='tl_list clearfix']/li/a"
            else:
                xpath = "//ul[@class='yy_list']/li/a"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for j in range(1, 4):
                    for i in range(1, 6):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace(']/li/a', f'][{j}]/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
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

                            else:
                                link = url.replace('index.htm', '').replace('default.htm', '') + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            if select == None:
                                uid = uuid.uuid4()
                                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                            else:
                                Mysql.update_xw_url(url=link, biaoti=title)
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('>'))
                                    # t = 0
                                    # for pp in range(5, 9):
                                    #     xy = f"//div[@class='jspIndex4']/a[{pp}]"
                                    #     if html_1.xpath(xy + '/text()')[0] == '>':
                                    #         t += 1
                                    #         driver.find_element_by_xpath(xy).click()
                                    #         break
                                    # if t == 0 and int(pages) != 1:
                                    #     print('点击下一页出错了')
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return yiyang(name)
def yiyang1(name):
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
            'http://www.yiyang.gov.cn/fgw/2475/default.htm': 13,  # 发改委 发改动态
            'http://www.yiyang.gov.cn/fgw/2474/default.htm': 1,  # 发改委 通知公告
            'http://www.yiyang.gov.cn/fgw/2476/default.htm': 1,  # 发改委 宏观综合
            'http://www.yiyang.gov.cn/fgw/2496/2497/default.htm': 1,  # 发改委 公示公告
            'http://www.yiyang.gov.cn/fgw/2496/2498/default.htm': 1,  # 发改委 政策法规
            'http://www.yiyang.gov.cn/fgw/2496/14191/index.htm': 1,  # 发改委 政策解读
            'http://www.yiyang.gov.cn/jsj/3381/default.htm': 2,  # 住建局 工作动态
            'http://www.yiyang.gov.cn/jsj/3382/default.htm': 8,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'jsj' in url:
                xpath = "//div[@class='ftls-r-2']/ul/li/a"
            else:
                xpath = "//ul[@class='clear']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('[', '').replace(']', '')
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if re.findall('http', href):
                            link = href
                        else:
                            link = 'http' + re.findall('http(.*?)cn', url)[0] + 'cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                                # xy = "//div[@id='pagination']/a[1]"
                                # driver.find_element_by_xpath(xy).click()

                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return yiyang1(name)


# todo  郴州 公共资源中心 |发改委 | 住建局
def chenzhou(name):
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
            'http://czggzy.czs.gov.cn/18360/18365/18367/index.htm': 9,  # 公共资源中心 工作动态
            'http://czggzy.czs.gov.cn/18360/18365/18369/index.htm': 4,  # 公共资源中心 通知公告
            'http://fgw.czs.gov.cn/fzggdt/13514/default.htm': 4,  # 发改委 县区动态
            'http://fgw.czs.gov.cn/27320/27328/31633/index.htm': 5,  # 发改委 政务要闻
            'http://fgw.czs.gov.cn/fzggdt/tzgg/default.htm': 2,  # 发改委 通知公告
            'http://fgw.czs.gov.cn/fzggdt/tpxw/default.htm': 6,  # 发改委 图片新闻
            'http://www.nks.czs.gov.cn/zjj/zwgk/gzdt/default.htm': 9,  # 住建局 工作动态
            'http://www.nks.czs.gov.cn/zjj/zwgk/tzgg/default.htm': 18,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'tpxw' in url: xpath = "//li/div/span/a"
            elif 'zjj' in url or 'fgw' in url:
                xpath = "//div[@class='fz-tab']/table/tbody/tr/td[2]"
            else:  xpath = "//ul[@class='clearfix list-ul']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0: break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    if 'tpxw' in url:
                        xpath1 = xpath.replace('//li/div/span/a', f'//li[{i}]/div/span/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(xpath1.replace('/span/',"[@class='tpnrsj']")+f"/text()")[0].strip()
                    elif 'fgw' in url or 'zjj' in url:
                        xpath1 = xpath.replace("//div[@class='fz-tab']/table/tbody/tr/td[2]", f"//tr[{i}]/td[2]/")
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(xpath1.replace("d[2]","d[@class='txt-12'][2]")+f"text()")[0].strip()
                    else:
                        xpath1 = xpath.replace('/a', f'[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            if 'czggzy' in url:
                                link = url.replace('index.htm','') + href
                                uid = uuid.uuid4()
                                insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                                Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                                   biaoti=title, tianjiatime=insertDBtime, zt='0')
                                print(f'--{city}-【{title}】写入成功')
                            else:
                                chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                # if 'fgw' in url or 'zjj' in url:
                                #     xy = "//ul[@class='pager']/li[3]/a"
                                # else:
                                #     xy = "//a[@class='pageNum'][10]"
                                # if len(html_1.xpath(xy)) > 0 :
                                #     driver.find_element_by_xpath(xy).click()
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return chenzhou(name)
# todo  郴州   人民政府
def chenzhou1(name):
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
            'http://www.czs.gov.cn/html/dtxx/zwdt/zwyw/default.htm': 109,  # 政务要闻
            'http://www.czs.gov.cn/html/dtxx/zwdt/bmdt/default.htm': 31,  # 部门动态
            'http://www.czs.gov.cn/html/dtxx/zwdt/xsqdt/default.htm': 418,  # 区县动态
            'http://www.czs.gov.cn/html/dtxx/tzgg/default.htm': 12,  # 通知公告
            'http://www.czs.gov.cn/html/dtxx/11711/default.htm': 94,  # 今日关注
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='yaowennr']/ul/li"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for j in range(1, 4):
                    for i in range(1, 6):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace(']/ul/li', f'][{j}]/ul/li[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            if select == None:
                                chuli(publictime,href,driver,url,title,city,xpath1)
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('>'))
                                    # t = 0
                                    # for pp in range(4, 9):
                                    #     xy = f"//div[@class='jspIndex4']/a[{pp}]"
                                    #     if html_1.xpath(xy + '/text()')[0] == '>':
                                    #         t += 1
                                    #         driver.find_element_by_xpath(xy).click()
                                    #         break
                                    # if t == 0 and int(pages) != 1:
                                    #     print('点击下一页出错了')
                                break
                        else:
                            po += 1
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return chenzhou1(name)


# todo  永州 公共资源中心
def yongzhou(name):
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
            'http://ggzy.yzcity.gov.cn/zwgk/002001/about-zwgk.html': 6,  # 工作动态
            'http://ggzy.yzcity.gov.cn/zwgk/002002/about-zwgk.html': 2,  # 通知公告
            'http://ggzy.yzcity.gov.cn/zwgk/002003/about-zwgk.html': 1,  # 媒体聚焦
            'http://ggzy.yzcity.gov.cn/zwgk/002005/002005001/about-zwgk.html': 1,  # 政策法规-工程建设
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//li[@class='wb-data-list']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace('/a', f'[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    if re.findall('\./', href):
                        link = href[2:]
                    elif re.findall('http', href):
                        link = href
                    else:
                        link = 'http' + re.findall('http(.*?)\.yzcity', url)[0] + '.yzcity.gov.cn' + href
                    title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                # if page != pages:
                                #     try:
                                #         driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                #     except:
                                #         driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                xy = f"//ul[@class='m-pagination-page']/li[{page + 1}]/a"
                                if len(html_1.xpath(xy + '/text()')) > 0:
                                    driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return yongzhou(name)

# todo  永州    发改委 | 行政审批局 |人民政府
def yongzhou1(name):
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
            'http://zwzx.yzcity.gov.cn/zwzx/0201/bmlist2.shtml': 3,  # 行政审批局 通知公告
            'http://zwzx.yzcity.gov.cn/zwzx/0204/bmlist2.shtml': 12,  # 行政审批局 图片新闻
            'http://zwzx.yzcity.gov.cn/zwzx/0202/bmlist2.shtml': 32,  # 行政审批局 工作动态
            'http://fgw.yzcity.gov.cn/fgw/0201/bmlist2.shtml': 25,  # 发改委 通知公告
            'http://fgw.yzcity.gov.cn/fgw/0202/bmlist2.shtml': 20,  # 发改委 工作动态
            'http://fgw.yzcity.gov.cn/fgw/0203/bmlist2.shtml': 13,  # 发改委 区县动态
            'http://fgw.yzcity.gov.cn/fgw/0204/bmlist2.shtml': 12,  # 发改委 图片新闻
            'http://www.yzcity.gov.cn/cnyz/yzyw/list.shtml': 50,  # 人民政府 永州要闻
            'http://www.yzcity.gov.cn/cnyz/xqcz/list.shtml': 50,  # 人民政府 县区传真
            'http://www.yzcity.gov.cn/cnyz/bmkx/list.shtml': 50,  # 人民政府 部门快讯
            'http://www.yzcity.gov.cn/cnyz/gsgg/list.shtml': 9,  # 人民政府 公示公告
            'http://zjj.yzcity.gov.cn/zjj/0202/bmlist2.shtml': 27,  # 住建局 工作动态
            'http://zjj.yzcity.gov.cn/zjj/0201/bmlist.shtml': 40,  # 住建局 公告公示
            'http://zjj.yzcity.gov.cn/zjj/0204/bmlist2.shtml': 10,  # 住建局 图片新闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            if 'www' in url:
                xpath="//div[@class='list_right']/ul/li/a"
            else:
                xpath = "//div/div[@class='list-right_title fon_1']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('v/d', f'v[{i}]/d').replace('i/a', f'i[{i}]/a')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    if re.findall('\./', href): href = href[2:]
                    else: href=href
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    dd = f"//div[@class='list_div mar-top2'][{i}]/table/tbody/tr/td[1]/text()"
                    dd1 = f"//div[@class='list_div mar-top2 '][{i}]/table/tbody/tr/td[1]/text()"
                    dd2 = f"//div[@class='list_right']/ul/li[{i}]/span/text()"
                    if 'www' in url:
                        publictime = html_1.xpath(dd2)[0].strip().replace('\n', '').replace('                    ', '')
                    elif len(html_1.xpath(dd)) > 0:
                        publictime = html_1.xpath(dd)[0].strip().replace('\n', '').replace('                    ', '')[5:]
                    else:
                        publictime = html_1.xpath(dd1)[0].strip().replace('\n', '').replace('                    ', '')[5:]
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                # t = 0
                                # for pp in range(2, 4):
                                #     xy = f"//div[@class='pagination_index'][{pp}]"
                                #     if len(html_1.xpath(xy + '/a/text()')) > 0  and html_1.xpath(xy + '/a/text()')[0] == '下一页':
                                #         t += 1
                                #         driver.find_element_by_xpath(xy).click()
                                #         break
                                #     elif len(html_1.xpath(xy + '/span/a/text()')) > 0  and html_1.xpath(xy + '/span/a/text()')[0] == '下一页':
                                #         t += 1
                                #         driver.find_element_by_xpath(xy).click()
                                #         break
                                #
                                # if t == 0 and int(pages) != 1:
                                #     print('点击下一页出错了')

                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return yongzhou1(name)


# todo  怀化  加载慢  公共资源中心 | 发改委 | 人民政府 | 住建局
def huaihua(name):
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
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c108767/list.shtml': 28,  # 头条新闻
            'http://ggzy.huaihua.gov.cn/ggzyjyzx/c108768/list.shtml': 8,  # 新闻动态
            'http://www.huaihua.gov.cn/fgw/c100576/list.shtml': 31,  # 发改委 头条新闻
            'http://www.huaihua.gov.cn/fgw/c100577/list.shtml': 12,  # 发改委 工作动态
            'http://www.huaihua.gov.cn/huaihua/c101111/list.shtml': 67,  # 人民政府 怀化动态
            'http://www.huaihua.gov.cn/huaihua/c101115/list.shtml': 67,  # 人民政府 部门动态
            'http://www.huaihua.gov.cn/huaihua/c101116/list.shtml': 67,  # 人民政府 县区动态
            'http://www.huaihua.gov.cn/huaihua/c101114/list.shtml': 21,  # 人民政府 通知公告
            'http://www.huaihua.gov.cn/huaihua/c101117/tpxw.shtml': 47,  # 人民政府 图片新闻
            'http://www.huaihua.gov.cn/zjj/c100647/list.shtml': 47,  # 住建局  文件通知
            'http://www.huaihua.gov.cn/zjj/c100640/channelNamelist.shtml': 47,  # 住建局  新闻动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            pages = 28
            po = 0
            for page in range(1, pages+1):
                if po>0:break
                if page == 1:
                    driver.get(url)
                else:
                    driver.get(url.replace('.shtml', f'_{page}.shtml'))
                time.sleep(5)
                con1 = driver.page_source
                html_2 = etree.HTML(con1)

                if 'tpxw' in url:
                    xpath = "/html/body/section/div[2]/div/ul/li/a[2]"
                elif 'cn/huaihua' in url:
                    xpath = "//ul[@class='newsList']/li/a"
                else:
                    xpath = "//div[@class='j-right-list-box']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))

                    xpath1 = xpath.replace('/a', f'[{i}]/')
                    if 'tpxw' in url:
                        href = html_1.xpath(f"/html/body/section/div[2]/div/ul/li[{i}]/a[2]/@href")[0].strip()
                        title = html_1.xpath(f"//li[{i}]/a/h2/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//ul/li[{i}]/span/text()")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('[政务动态] ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    elif re.findall('http', href):
                        href = href
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if re.findall('http', href):
                            link = href
                        else:
                            link = 'http' + re.findall(r'http(.*?)\.gov', url)[0] + '.gov.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            Mysql.update_xw_url(url=link, biaoti=title)
                        # if i == lengt:
                        #     if pages == 2:
                        #         break
                        #     else:
                        #         if lengt < length - 1:
                        #             break
                        #         else:
                        #             xy = "//a[@class='pageNum'][10]"
                        #             if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[0] == '>':
                        #                 driver.find_element_by_xpath(xy).click()
                        #         break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return huaihua(name)

# todo  娄底    公共资源中心 | 行政审批局| 发改委 | 人民政府
def loudi(name):
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
            'http://ldggzy.hnloudi.gov.cn/ldjyzx/zxzx_zxdt/list.shtml': 7,  # 公共资源中心 中心动态
            'http://ldggzy.hnloudi.gov.cn/ldjyzx/zxzx_tzgg/list.shtml': 3,  # 公共资源中心 通知公告
            'http://www.hnloudi.gov.cn/ldspj/07/list.shtml': 7,  # 行政审批局 工作动态
            'http://fgw.hnloudi.gov.cn/ldfgw/1001/list2.shtml': 10,  # 发改委 工作动态
            'http://www.hnloudi.gov.cn/loudi/0601/list.shtml': 67,  # 人民政府 娄底要闻
            'http://www.hnloudi.gov.cn/loudi/0602/list.shtml': 67,  # 人民政府 部门动态
            'http://www.hnloudi.gov.cn/loudi/0603/list.shtml': 67,  # 人民政府 县市区动态
            'http://www.hnloudi.gov.cn/loudi/jdhy/zcjd/list.shtml': 6,  # 人民政府 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//ul[@class='news-list']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('/a', f'[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    if 'cn/loudi/' in url:
                        title = html_1.xpath(f"{xpath1}a/voice/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/voice/text()")[0].strip()
                    else:
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            chuli(publictime,href,driver,url,title,city,xpath1)

                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        xy = "//td[contains(string(),'下页')]"
                                        driver.find_element_by_xpath(xy).click()
                                    except:
                                        xy = "//span[@class='arrow'][7]/a"
                                        if len(html_1.xpath(xy + '/text()')) > 0 and html_1.xpath(xy + '/text()')[0] == '下一页':
                                            driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return loudi(name)

# todo  娄底    发改委 | 人民政府
def loudi1(name):
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
            'http://ldggzy.hnloudi.gov.cn/ldjyzx/xxgk_zfxxgkml/xxgk_list.shtml': 2,  # 娄底公共资源交易中心 法定主动公开内容
            'http://www.hnloudi.gov.cn/ldspj/06/xxgk_list.shtml': 4,  # 行政审批局 法定主动公开内容 通知公告
            'http://www.hnloudi.gov.cn/ldspj/05/xxgk_list.shtml': 2,  # 行政审批局 法定主动公开内容 政策法规
            'http://fgw.hnloudi.gov.cn/ldfgw/1002/xxgk_list.shtml': 20,  # 发改委 时政要闻
            'http://fgw.hnloudi.gov.cn/ldfgw/09/xxgk_list.shtml': 3,  # 发改委 通知公告
            'http://fgw.hnloudi.gov.cn/ldfgw/0802/xxgk_list.shtml': 1,  # 发改委 政策解读
            'http://www.hnloudi.gov.cn/loudi/05/xxgk_list.shtml': 12,  # 人民政府 法定主动公开内容 / 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//ul/li/h4/a"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages + 1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for j in range(1, 4):
                    for i in range(1, 6):
                        lengt = len(html_1.xpath(xpath))
                        xpath1=xpath.replace('/ul/li/h4/a',f'/ul[{j}]/li[{i}]/h4/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'www' in url:
                                link = 'http://www.hnloudi.gov.cn' + href
                            elif 'fgw' in url:
                                link = 'http://fgw.hnloudi.gov.cn' + href
                            else:
                                link = 'http://ldggzy.hnloudi.gov.cn' + href
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            if select == None:
                                uid = uuid.uuid4()
                                chuli(publictime,href,driver,url,title,city,xpath1)
                            if (j - 1) * 5 + i == lengt:
                                if lengt < length - 1:
                                    break
                                else:
                                    if page != pages:
                                        try:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('下一页'))
                                        except:
                                            driver.execute_script("arguments[0].click();",
                                                                  driver.find_element_by_link_text('>'))

                                break

                        else:
                            po += 1
                            break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return loudi1(name)


from threading import Thread

t0 = Thread(target=hunan, args=("湖南",))
t00 = Thread(target=hunan1, args=("湖南",))
t1 = Thread(target=changsha, args=("长沙",))
t2 = Thread(target=changsha1, args=("长沙",))
t3 = Thread(target=zhuzhou, args=("株洲",))
t4 = Thread(target=zhuzhou1, args=("株洲",))
t5 = Thread(target=xiangtan, args=("湘潭",))
t6 = Thread(target=xiangtan1, args=("湘潭",))
t7 = Thread(target=hengyang, args=("衡阳",))
t9 = Thread(target=shaoyang, args=("邵阳",))
t10 = Thread(target=shaoyang1, args=("邵阳",))
t11 = Thread(target=yueyang, args=("岳阳",))

t12 = Thread(target=changde, args=("常德",))
t13 = Thread(target=zhangjiajie, args=("张家界",))
t14 = Thread(target=yiyang, args=("益阳",))
t15 = Thread(target=yiyang1, args=("益阳",))
t16 = Thread(target=chenzhou, args=("郴州",))
t17 = Thread(target=chenzhou1, args=("郴州",))
t18 = Thread(target=yongzhou, args=("永州",))
t19 = Thread(target=yongzhou1, args=("永州",))
t20 = Thread(target=huaihua, args=("怀化",))
t21 = Thread(target=loudi, args=("娄底",))
t22 = Thread(target=loudi1, args=("娄底",))

def start():
    hunan('湖南')
    hunan1('湖南')
    changsha("长沙")
    changsha1("长沙")
    zhuzhou("株洲")
    zhuzhou1("株洲")
    xiangtan('湘潭')
    xiangtan1('湘潭')
    hengyang('衡阳')
    shaoyang('邵阳')
    shaoyang1('邵阳')
    yueyang('岳阳')

    changde('常德')
    zhangjiajie('张家界')
    yiyang('益阳')
    yiyang1('益阳')
    chenzhou('郴州')
    chenzhou1('郴州')
    yongzhou('永州')
    yongzhou1('永州')
    huaihua('怀化')
    loudi('娄底')
    loudi1('娄底')

# threadl = [t0,t00,t1,t2,t3,t4,t5,t6,t7,t9,t10,t11]
#
# tt = Thread(target=start)
# threadl.append(tt)
#
# def ready5():
#     for x in threadl:
#         x.start()
# ready5()

start()
# xiangtan1('湘潭')