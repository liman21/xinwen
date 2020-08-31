import time, uuid
from dao import Mysql
from lxml import etree
from selenium import webdriver
from datetime import datetime
from openpyxl import load_workbook
import re, os, shutil

gjzs = ['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子', '保险']
now = datetime.now()
from bs4 import BeautifulSoup


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


def  chuli(publictime,href,driver,url,title,city,xpath1):
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
        print('蚌埠\t', e)
pro = '贵州'
jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 15
# jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))

# todo  贵州 人民政府
def guizhou(name):
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
            'http://www.guizhou.gov.cn/xwdt/jrgz/': '68',  # 今日关注
            'http://www.guizhou.gov.cn/xwdt/gzyw/': '67',  # 贵州要闻
            'http://www.guizhou.gov.cn/xwdt/mtkgz/': '67',  # 媒体看贵州
            'http://www.guizhou.gov.cn/xwdt/djfb/': '67',  # 独家发布
            'http://www.guizhou.gov.cn/xwdt/tzgg/': '15',  # 通知公告
            'http://www.guizhou.gov.cn/xwdt/zy/ldjh/index.html': '67',  # 领导讲话
            'http://www.guizhou.gov.cn/xwdt/zy/ldhd/': '67',  # 领导活动
            'http://www.guizhou.gov.cn/xwdt/dt_22/bm/index.html': '67',  # 部门动态
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/gy/': '67',  # 地方动态 贵阳
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/zy/': '67',  # 地方动态 遵义
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/lps/': '67',  # 地方动态 六盘水
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/as/': '67',  # 地方动态 安顺
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/bj/': '67',  # 地方动态 毕节
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/tr/': '67',  # 地方动态 铜仁
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/qdn/': '67',  # 地方动态 黔东南
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/qn/': '67',  # 地方动态 黔南
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/qxn/': '67',  # 地方动态 黔西南
            'http://www.guizhou.gov.cn/xwdt/dt_22/df/gaxq/': '67',  # 地方动态 贵安新区
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='right-list-box']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, int(pages)):
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
                    title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select is None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime,href,driver,url,title,city,xpath1)

                        else:
                            po += 1
                            break
                    else:
                        print(f'【{title}】已存在')
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            driver.find_element_by_xpath("//a[@class='up leaidx'][2]").click()
                        break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return guizhou(name)


# todo  贵州 公共资源中心| 住建厅 |发改委
def guizhou1(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        urls = {
            'http://ggzy.guizhou.gov.cn/zhdt/gzyw/': '11',  # 贵州要闻
            'http://ggzy.guizhou.gov.cn/zhdt/xwdt/': '60',  # 省中心状态
            'http://ggzy.guizhou.gov.cn/zhdt/szyw/': '116',  # 市州状态
            'http://ggzy.guizhou.gov.cn/zhdt/xydt/': '34',  # 行业资讯
            'http://ggzy.guizhou.gov.cn/zhdt/tzgg/': '26',  # 通知公告
            'http://ggzy.guizhou.gov.cn/zhdt/csdt/': '66',  # 处室动态
            'http://zfcxjst.guizhou.gov.cn/jszx/jqdt/': '36',  # 住建厅 近期动态
            'http://zfcxjst.guizhou.gov.cn/jszx/zxwj/': '69',  # 住建厅 最新文件
            'http://zfcxjst.guizhou.gov.cn/zwgk/hygq/xwfbh/': '12',  # 住建厅 新闻发布
            'http://zfcxjst.guizhou.gov.cn/zwgk/hygq/zcjd/': '3',  # 住建厅 政策解读
            'http://fgw.guizhou.gov.cn/fzggdt/ywbd/': '26',  # 发改委 图片新闻
            'http://fgw.guizhou.gov.cn/fzggdt/tpxw/': '18',  # 发改委 要闻报道
            'http://fgw.guizhou.gov.cn/fzggdt/tzgg/': '38',  # 发改委 通知公告
            'http://fgw.guizhou.gov.cn/fzggdt/wndt/': '21',  # 发改委 委内动态
            'http://fgw.guizhou.gov.cn/fzggdt/zcfb/': '13',  # 发改委 政策发布
            'http://fgw.guizhou.gov.cn/zwgk/xxgkml/zdgk/zcjd/list.html': '11',  # 发改委 政策解读
            'http://fgw.guizhou.gov.cn/zwgk/xxgkml/zdgk/zcwj/list.html': '4',  # 发改委 政策文件
        }
        for url, pages in zip(urls.keys(), urls.values()):

            driver.get(url)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zfcxjst' in url:
                xpath = "//div[@class='NewsList']/ul/li/a"
            elif 'xxgkml' in url:
                xpath = "//tr/td[1]/h1/a"
            elif 'fgw' in url:
                xpath = "//div[@class='right_list f_r f14']/dl/dd/ul/li/a"
            else:
                xpath = "//div/div/div[@class='xxqb_box2lbbt']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('//div/d', f'//div[{i}]/d').replace(']/a', f']/').replace('i/a',
                                                                                                     f'i/').replace(
                        '1/a', f'1/').replace('r/t', f'r[{i}]/t')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    if 'fgw' in url:
                        title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n', '').replace(
                            '                                    ', '').replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                    else:
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                    if 'xxgkml' in url:
                        publictime = html_1.xpath(f"//table[@id='data']/tbody/tr[{i}]/td[2]/text()")[0].strip()
                    elif 'fgw' in url:
                        publictime = html_1.xpath(f"{xpath1}a/i/text()")[0].strip()[1:-1]
                    else:
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip().replace('\n', '')[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        uid = uuid.uuid4()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                             chuli(publictime,href,driver,url,title,city,xpath1)

                        else:
                            po += 1
                            break
                    else:
                        print(f'【{title}】已存在')

                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if len(html_1.xpath(f"//a[@class='up'][2]")) > 0:
                                driver.find_element_by_xpath("//a[@class='up'][2]").click()
                            else:
                                po += 1
                                break
                        break

    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return guizhou1(name)


# todo  贵阳 人民政府
def guiyang(name):
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
            'http://www.guiyang.gov.cn/zwgk/zwgkxwdt/zwgkxwdtjrgy/': '68',  # 今日贵阳
            'http://www.guiyang.gov.cn/zwgk/zwgkxwdt/zwgkxwdtbmdt/': '68',  # 部门动态
            'http://www.guiyang.gov.cn/zwgk/zwgkxwdt/zwgkxwdtqxdt/': '68',  # 区县动态
            'http://www.guiyang.gov.cn/zwgk/zwgktzgg/zwgktzgggggs/': '26',  # 政务公告
            'http://www.guiyang.gov.cn/zwgk/zwgktzgg/zwgktzggbmgg/': '68',  # 部门公告
            'http://www.guiyang.gov.cn/zwgk/zwgktzgg/zwgktzggqsxgg/': '66',  # 区市县公告
            'http://zhujianju.guiyang.gov.cn/zfxxgk_5618855/fdzdgknr_5618858/gzdt/': '51',  # 住建厅 工作动态
            'http://zhujianju.guiyang.gov.cn/zfxxgk_5618855/fdzdgknr_5618858/gsgg_5618880/tzgg/': '9',  # 住建厅 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zhujianju' in url:
                xpath = "//div[@class='zfxxgk_zdgkc']/ul/li/a"
                xy = "//div[@id='pages']/a[@class='next']"
            else:
                xpath = '//*[@id="gy_lmy_right"]/ul/li/a'
                xy = "//a[@class='btn-next']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                    if 'zhujianju' in url:
                        publictime = html_1.xpath(f"{xpath1}b/text()")[0].strip()[:10]
                    else:
                        publictime = html_1.xpath(f"{xpath1}a/div/text()")[0].strip()[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                             chuli(publictime,href,driver,url,title,city,xpath1)


                        else:
                            po += 1
                            break
                    else:
                        print(f'【{title}】已存在')
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if len(html_1.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()
                            else:
                                po += 1
                                break

                        break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return guiyang(name)


# todo  贵州 公共资源中心| 住建厅 |发改委
def guiyang1(name):
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
            'http://ggzy.guiyang.gov.cn/xxgk/tzgg/': '12',  # 通知公告
            'http://ggzy.guiyang.gov.cn/xxgk/gzdt/': '39',  # 工作动态
            'http://ggzy.guiyang.gov.cn/xxgk/tpxw/': '6',  # 图片新闻
            'http://ggzy.guiyang.gov.cn/zcfg/zcjd/': '2',  # 政策解读
            'http://ggzy.guiyang.gov.cn/zcfg/zcfg/': '2',  # 政策法规
            'http://fgw.guiyang.gov.cn/fgdt/gzdt/': '40',  # 发改委 工作动态
            'http://fgw.guiyang.gov.cn/fgdt/tzgg/': '15',  # 发改委 通知公告
            'http://fgw.guiyang.gov.cn/fgdt/qxdt/': '2',  # 发改委 区县动态
            'http://fgw.guiyang.gov.cn/zwgk/xxgkml/zdgk/zcjd/': '3',  # 发改委 政策解读
            'http://fgw.guiyang.gov.cn/zwgk/xxgkml/zdgk/zcwj/': '16',  # 发改委 政策文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'xxgkml' in url:
                xpath = "//tr[@class='c']/td/a"
            elif 'fgw' in url:
                xpath = "//div[@class='NewsList']/ul/li/a"
            else:
                xpath = "//li[@class='right_li pr']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/a', f'][{i}]/a').replace(']/t', f'][{i}]/t').replace('i/a', f'i[{i}]/a')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    if 'xxgkml' in url:
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//tr[@class='c'][{i}]/td[4]/text()")[0].strip().replace('\n', '')[
                                     :10]
                    else:
                        title = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        if 'fgw' in url:
                            publictime = html_1.xpath(f"//ul/li[{i}]/span/text()")[0].strip().replace('\n', '')[:10]
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '')[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        uid = uuid.uuid4()
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime,href,driver,url,title,city,xpath1)

                        else:
                            po += 1
                            break
                    else:
                        print(f'【{title}】已存在')
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if len(html_1.xpath("//a[@class='up'][2]")) > 0:
                                driver.find_element_by_xpath("//a[@class='up'][2]").click()
                            else:
                                po += 1
                                break
                        break
    except Exception as e:
        print(f'[{name}] 出错了\n ', e)
        driver.close()
        return guiyang1(name)


# todo  六盘水 人民政府 | 发改委
def liupanshui(name):
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
            'http://www.gzlps.gov.cn/yw/jrld/': '172',  # 今日凉都
            'http://www.gzlps.gov.cn/yw/bmdt/': '102',  # 部门动态
            'http://www.gzlps.gov.cn/yw/xqdt/': '116',  # 区县动态
            'http://www.gzlps.gov.cn/yw/tzgg/': '14',  # 通知公告
            'http://www.gzlps.gov.cn/yw/mtgz_35303/': '12',  # 媒体关注
            'http://www.gzlps.gov.cn/yw/sspl/': '13',  # 时事评论
            'http://www.gzlps.gov.cn/zw/jcxxgk/zcwj/zcjd/sjzcjd/': '84',  # 国家政策解读
            'http://www.gzlps.gov.cn/zw/jcxxgk/zcwj/zcjd/bjzcjd/': '10',  # 省级政策解读
            'http://www.gzlps.gov.cn/zw/jcxxgk/zcwj/zcjd/bj/': '3',  # 本级政策解读
            'http://fgw.gzlps.gov.cn/gzdt_42194/bmdt_42195/index.html': '8',  # 发改委 部门动态
            'http://fgw.gzlps.gov.cn/tzgg_42196/': '3',  # 发改委 通知公告
            'http://fgw.gzlps.gov.cn/zwgk_42198/fgwj_42238/flfg/': '2',  # 发改委 法律法规
            'http://fgw.gzlps.gov.cn/zwgk_42198/fgwj_42238/zcjd_42241/': '3',  # 发改委  政策解读
            'http://fgw.gzlps.gov.cn/zwgk_42198/zfxxgk_42199/xxgkml_42202/bmwj_42210/list.html': '2',  # 发改委  部门文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zfxxgk' in url:
                xpath = "//tr/td[1]/h1[@class='indexs']/a"
            elif 'fgw' in url:
                xpath = "//ul[@class='text-list']/li/a"
            else:
                xpath = "//div[@class='NewsList']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]/').replace('r/t', f'r[{i}]/t')
                    if 'zfxxgk' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('                                ',
                                                                                    '').replace('·', '').replace('\n',
                                                                                                                 '').replace(
                            '%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//table[@id='data']/tbody/tr[{i}]/td[2]/text()")[0].strip().replace(
                            '\n', '')[:10]
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip().replace('\n', '')[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                             chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:

                            t=0
                            for pp in range(8, 14):
                                xy = f"//li[{pp}]/a[@class='up']"
                                if len(html_1.xpath(xy)) > 0:
                                    t += 1
                                    driver.find_element_by_xpath(xy).click()
                                    break
                            if t == 0:
                                print('点击下一页出错了')
                        break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return liupanshui(name)


# todo  六盘水 公共资源中心| 住建厅 |发改委
def liupanshui1(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        urls = {
            'http://ggzy.gzlps.gov.cn/xxgk/tzgg/': '2',  # 通知公告
            'http://ggzy.gzlps.gov.cn/xxgk/gzdt/': '8',  # 工作动态
            'http://ggzy.gzlps.gov.cn/zcfg/': '4',  # 政策法规
            'http://zjj.gzlps.gov.cn/gzdt_43007/bmdt_43008/': '14',  # 住建厅 部门动态
            'http://zjj.gzlps.gov.cn/gzdt_43007/tzgg_43009/': '19',  # 住建厅 通知公告
            'http://zjj.gzlps.gov.cn/zwgk_43012/fgwj_43043/zcfg_43045/': '4',  # 住建厅 政策法规
            'http://zjj.gzlps.gov.cn/zwgk_43012/zfxxgk_43013/xxgkml_43016/list.html': '2',  # 住建厅 部门文件
            'http://zjj.gzlps.gov.cn/zwgk_43012/fgwj_43043/zcjd_43047/': '2',  # 住建厅 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            width = driver.execute_script("return document.documentElement.scrollWidth")
            height = driver.execute_script("return document.documentElement.scrollHeight")
            driver.set_window_size(width, height)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zfxxgk' in url:
                xpath = "//tr/td/h1/a"
            elif 'fgwj' in url:
                xpath = "//ul[@class='list']/li/a"
            elif 'zjj' in url:
                xpath = "//ul[@class='zongul']/li/a"
            else:
                xpath = "//div[@class='NewsList']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]').replace('r/t', f'r[{i}]/t')
                    if 'zfxxgk' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//table[@id='data']/tbody/tr[{i}]/td[2]/text()")[0].strip().replace(
                            '\n', '')[:10]
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '')[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                             chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            try:
                                driver.find_element_by_xpath("//a[@class='up'][2]").click()
                            except Exception as e:
                                print(e)

                        break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return liupanshui1(name)


# todo  遵义 人民政府 | 发改委
def zunyi(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        urls = {
            'http://www.zunyi.gov.cn/xwdt/ttxw/': '51',  # 头条新闻
            'http://www.zunyi.gov.cn/xwdt/zyyw/': '51',  # 遵义要闻
            'http://www.zunyi.gov.cn/xwdt/qxdt/': '51',  # 区县动态
            'http://www.zunyi.gov.cn/xwdt/bmdt/': '51',  # 部门动态
            'http://www.zunyi.gov.cn/xwdt/tzgg/': '9',  # 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='PageMainBox aBox']/ul/li"
            length = len(html_2.xpath(xpath))
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0: break
                for j in range(1, 5):
                    for i in range(1, 6):
                        con = driver.page_source
                        html_1 = etree.HTML(con)
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()

                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '')[:10]
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
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
                            else:
                                po += 1
                                break
                        else:
                            print(f'【{title}】已存在')
                        if (j - 1) * 5 + i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                xy=f"//div[@id='HTML_LB_PAGE']/a[{page + 1}]"
                                if len(html_1.xpath(xy)) > 0:
                                    driver.find_element_by_xpath(xy).click()  # 点击2级页面

                                    b_handle = driver.current_window_handle  # 获取当前页句柄
                                    driver.close()  # 关闭当前窗口
                                    handles = driver.window_handles  # 获取所有页句柄
                                    s_handle = None
                                    for handle in handles:
                                        if handle != b_handle:
                                            s_handle = handle
                                    driver.switch_to.window(s_handle)
                            break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return zunyi(name)


# todo  遵义 公共资源中心| 住建厅 |发改委
def zunyi1(name):
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
            'http://ggzyjy.zunyi.gov.cn/zhxw/': '6',  # 公共资源中心 综合新闻
            'http://ggzyjy.zunyi.gov.cn/tzgg/': '2',  # 公共资源中心 通知公告
            'http://ggzyjy.zunyi.gov.cn/xydt/': '4',  # 公共资源中心 行业动态
            'http://zjj.zunyi.gov.cn/gzdt/': '9',  # 住建厅 工作动态
            'http://zjj.zunyi.gov.cn/tzgg/': '4',  # 住建厅 通知公告
            'http://fgw.zunyi.gov.cn/tzgg/': '5',  # 发改委 通知公告
            'http://fgw.zunyi.gov.cn/gzdt/': '23',  # 发改委 工作动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zjj' in url:
                xpath = "//tr/td[2]/a"
                xy = "//span[@id='pagebox']/a[5]"
            elif 'fgw' in url:
                xpath = "//div[@class='box']/ul/li/h3"
                xy = "//div[@class='fenye page']/a[7]"
            else:
                xpath = "//ul[@class='list']/li/a"
                xy = "//a[@class='up'][2]"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]').replace('r/t', f'r[{i}]/t').replace('i/h',
                                                                                                 f'i[{i}]/h').replace(
                        ']/a', f']')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    if re.findall('\./', href):
                        href = href[2:]
                    else:
                        href = href
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                    if 'fgw' in url:
                        publictime = html_1.xpath(f"//div[@class='box']/ul/li[{i}]/span/text()")[0].strip().replace(
                            '\n', '')[1:-1]
                    elif 'zjj' in url:
                        publictime = html_1.xpath(f"//tr[{i}]/td[@class='dash_line_h']/text()")[0].strip().replace('\n',
                                                                                                                   '')[
                                     :10]
                    else:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '')[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                             chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            po += 1
                            break
                    else:
                        print(f'【{title}】已存在')
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if len(html_1.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()

                        break
    except Exception as e:
        print(f'[{name}] 出错了 ', e)
        driver.close()
        return zunyi1(name)


# todo  安顺 人民政府 | 公共资源 |发改委
def anshun(name):
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
            'http://www.anshun.gov.cn/xwzx/jrgz/': '27',  # 今日关注
            'http://www.anshun.gov.cn/xwzx/asyw/': '51',  # 安顺要闻
            'http://www.anshun.gov.cn/xwzx/bmdt/': '51',  # 部门动态
            'http://www.anshun.gov.cn/xwzx/xqzc/': '51',  # 县区之窗
            'http://www.anshun.gov.cn/xwzx/snyw/': '24',  # 省内要闻
            'http://www.anshun.gov.cn/xwzx/gggs/': '10',  # 公告公示
            'http://www.anshun.gov.cn/xwzx/tpxw/': '20',  # 图片新闻
            'http://www.anshun.gov.cn/jdhy/zcjd/': '5',  # 政策解读
            'http://www.anshun.gov.cn/jdhy/hygq/': '5',  # 回应关切
            'http://www.anshun.gov.cn/jdhy/xwfbh/': '4',  # 新闻发布会
            'http://ggzy.anshun.gov.cn/xwdt/gzdt/': '6',  # 公共资源中心 工作动态
            'http://www.ggzy.anshun.gov.cn/xwdt/xydt/': '2',  # 公共资源中心 行业动态
            'http://www.ggzy.anshun.gov.cn/xwdt/tzgg/': '3',  # 公共资源中心 通知公告
            'http://www.ggzy.anshun.gov.cn/xwdt/qtxw/': '2',  # 公共资源中心  其他新闻
            'http://www.ggzy.anshun.gov.cn/xwdt/tpxw/': '4',  # 公共资源中心  图片新闻
            'http://fgw.anshun.gov.cn/fgdt/fgyw/': '14',  # 发改委  发改要闻
            'http://fgw.anshun.gov.cn/fgdt/tpxw/': '4',  # 发改委  图片新闻
            'http://fgw.anshun.gov.cn/fgdt/gzdtv2/': '42',  # 发改委  工作动态
            'http://fgw.anshun.gov.cn/fgdt/tzggv2/': '4',  # 发改委  通知公告
            'http://fgw.anshun.gov.cn/zwgk/zfxxgk/xxgkml/zcjd/': '3',  # 发改委  政策解读
            'http://fgw.anshun.gov.cn/zwgk/zfxxgk/xxgkml/bmwj/': '2',  # 发改委   部门文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'tpxw' in url:
                xpath = "//div[@class='lby_ycnr_con']/a"
            elif 'jdhy' in url:
                xpath = "//ul/li/h2"
            elif 'fgw' in url:
                xpath = "//div[@class='guidance_list']/ul/li/a"
            else:
                xpath = "//div[@class='NewsList']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]').replace(']/a', f']/a[{i}]').replace('i/h', f'i[{i}]/h')
                    if 'tpxw' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        rq = re.findall(r'/t(\d+)_', href)[0]
                        publictime = rq[:-4] + '-' + rq[4:6] + '-' + rq[-2:]
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '')[:10]
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime,href,driver,url,title,city,xpath1)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if len(html_1.xpath(f"//a[@class='up'][2]")) > 0:
                                driver.find_element_by_xpath("//a[@class='up'][2]").click()
                        break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return anshun(name)


# todo  毕节 人民政府  | 公共资源 | 发改委 | 住建局
def bijie(name):

    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)
        urls = {
            'http://www.bijie.gov.cn/yw/ttxw/': '15',  # 头条新闻
            'http://www.bijie.gov.cn/yw/bjyw/': '117',  # 毕节要闻
            'http://www.bijie.gov.cn/yw/bmdt/': '244',  # 部门动态
            'http://www.bijie.gov.cn/yw/qxdt/qxgq/': '55',  # 区县动态 七星关区
            'http://www.bijie.gov.cn/yw/qxdt/dfx_5125392/': '244',  # 区县动态 大方县
            'http://www.bijie.gov.cn/yw/qxdt/qxx_5125393/': '30',  # 区县动态 黔西县
            'http://www.bijie.gov.cn/yw/qxdt/zjx_5125394/': '46',  # 区县动态 织金县
            'http://www.bijie.gov.cn/yw/qxdt/jsx_5125395/': '46',  # 区县动态 金沙县
            'http://www.bijie.gov.cn/yw/qxdt/hzx_5125396/': '28',  # 区县动态  赫章县
            'http://www.bijie.gov.cn/yw/qxdt/nyx_5125397/': '150',  # 区县动态 纳雍县
            'http://www.bijie.gov.cn/yw/qxdt/wnx/': '26',  # 区县动态 威宁县
            'http://www.bijie.gov.cn/yw/qxdt/bldj_5125399/': '31',  # 区县动态 百里杜鹃
            'http://www.bijie.gov.cn/yw/qxdt/jhhxq/': '39',  # 区县动态 金海湖新区
            'http://www.bijie.gov.cn/yw/mtgz/': '5',  # 媒体关注
            'http://www.bijie.gov.cn/yw/tpxw/': '16',  # 图片新闻
            'http://www.bijie.gov.cn/yw/tzgg/zwgg/': '9',  # 政务公告
            'http://www.bijie.gov.cn/gk/xxgkml/jcxxgk/zcjd/bj/': '4',  # 政策解读 » 本级
            'http://www.bijie.gov.cn/gk/xxgkml/jcxxgk/zcjd/sj/': '8',  # 政策解读 » 省级
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/dt_5127733/zxdt/': '8',  # 公共资源中心 » 中心动态
            'http://www.bijie.gov.cn/bm/bjsggzyjyzx/dt_5127733/tzgg_5127735/': '3',  # 公共资源中心 » 通知公告
            'http://www.bijie.gov.cn/bm/bjsfzggw/dt/bmdt_5126121/': '8',  # 发改委 » 部门动态
            'http://www.bijie.gov.cn/bm/bjsfzggw/dt/tzgg_5126122/': '3',  # 发改委 » 通知公告
            'http://www.bijie.gov.cn/bm/bjszfcxjsj/dt_5126674/bmdt_5126675/': '5',  # 住建局 » 部门动态
            'http://www.bijie.gov.cn/bm/bjszfcxjsj/dt_5126674/tzgg_5126676/': '21',  # 住建局 » 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'xxgkml' in url:
                xpath = "//div[@class='zcjd_list']/ul/li/h2/a"
                length = 11
            else:
                xpath = "//div[@class='NewsList']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            pages = int(pages)
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    if 'xxgkml' not in url and i % 6 == 0:
                        pass
                    else:
                        con = driver.page_source
                        html_1 = etree.HTML(con)
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]').replace('i/h2/a', f'i[{i}]/h2')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        if re.findall('\./', href):
                            href = href[2:]
                        else:
                            href = href
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '')[:10]
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                 chuli(publictime,href,driver,url,title,city,xpath1)
                            else:
                                po += 1
                                break
                        if ('xxgkml' not in url and i == lengt+3) or ('xxgkml'  in url and i == lengt):
                            if lengt  < len(html_2.xpath(xpath)):
                                break
                            else:
                                if len(html_1.xpath(f"//a[@class='up'][2]")) > 0:
                                    driver.find_element_by_xpath("//a[@class='up'][2]").click()
                            break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return bijie(name)

# todo  铜仁 人民政府  | 公共资源 | 发改委 | 住建局
def tongren(name):

    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)
        urls = {
            'http://jyzx.trs.gov.cn/xwzx/gzdt/': 8,  # 公共资源 工作动态
            'http://jyzx.trs.gov.cn/xwzx/zyxw/': 4,  # 公共资源 重要新闻
            'http://jyzx.trs.gov.cn/xwzx/qxdt/': 2,  # 公共资源 区县动态
            'http://jyzx.trs.gov.cn/xwzx/tzgg/': 2,  # 公共资源 通知公告
            'http://jyzx.trs.gov.cn/xwzx/qxtz/': 1,  # 公共资源 区县通知
            'http://www.trs.gov.cn/xwzx/trsyw/': 216,  # 人民政府  铜仁市要闻
            'http://www.trs.gov.cn/xwzx/bmdt/': 145,  # 人民政府 部门动态
            'http://www.trs.gov.cn/xwzx/qxyw/': 153,  # 人民政府 区县要闻
            'http://www.trs.gov.cn/xwzx/tzgg/gsgg/': 14,  # 人民政府 公示公告
            'http://fgw.trs.gov.cn/fgdt/fgdt_5137519/': 14,  # 发改委  发改动态
            'http://fgw.trs.gov.cn/zcfg_500454/zcjd/': 5,  # 发改委  政策解读
            'http://fgw.trs.gov.cn/xxgk_500454/xxgkml/zdgk/tzgg/': 17,  # 发改委  发改动态
            'http://trsjs.trs.gov.cn/gzdt_500582/bmdt/': 8,  # 住建局  部门动态
            'http://trsjs.trs.gov.cn/gzdt_500582/gsgg/': 7,  # 住建局  公示公告
                   }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jyzx' in url:
                xpath = "//div[@id='right']/div[1]/table/tbody/tr/td[2]/a"
            elif 'xxgk_500454' in url:
                xpath = "//tbody[@id='idData']/tr/td[3]/a"
            elif 'fgw' in url:
                xpath = "//div[@class='NewsList']/ul/li"
            elif 'zjj' in url:
                xpath = "//div[@class='NewsList']/ul/li"
            else:
                xpath = "//div[@class='right']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    # if 'xxgkml' not in url and i % 6 == 0:
                    #     pass
                    # else:
                        con = driver.page_source
                        html_1 = etree.HTML(con)
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr/td[{i}][')
                        if 'jyzx' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        elif 'xxgk_500454' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[3]/a','[5]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n', '').replace('\t',
                                                                                                                           '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1+ f"/span/text()")[0].strip().replace('\n', '')[:10]

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
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                      driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return tongren(name)

# todo  黔南 人民政府  | 公共资源 | 发改委(无) | 住建局(无)
def qiannan(name):

    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)
        urls = {
            'http://ggzy.qiannan.gov.cn/xwzx_500203/yw/': 3,  # 公共资源 要闻
            'http://ggzy.qiannan.gov.cn/xwzx_500203/gzdt/': 3,  # 公共资源 工作动态
            'http://ggzy.qiannan.gov.cn/xwzx_500203/tzgg/tzgg_5125157/index.html': 3,  # 公共资源 通知公告
            'http://www.qiannan.gov.cn/xwdt/qnyw/': 122,  # 人民政府 黔南要闻
            'http://www.qiannan.gov.cn/xwdt/bmdt/': 101,  # 人民政府 部门动态
            'http://www.qiannan.gov.cn/xwdt/xsdt/': 256,  # 人民政府 县市动态
            'http://www.qiannan.gov.cn/xwdt/tzgg/': 36,  # 人民政府 通知公告
            'http://www.qiannan.gov.cn/xwdt/tpxw/': 13,  # 人民政府 图片新闻
                   }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ff' in url:
                xpath = "//div[@class='NewsList']/ul/li"
            else:
                xpath = "//div[@class='NewsList']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    if 'qiannan' not in url and i % 6 == 0:
                        pass
                    else:
                        con = driver.page_source
                        html_1 = etree.HTML(con)
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr/td[{i}][')
                        if 'jyzx' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        elif 'xxgk_500454' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[3]/a','[5]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n', '').replace('\t',
                                                                                                                           '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1+ f"/span/text()")[0].strip().replace('\n', '')[:10]

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
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                      driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return qiannan(name)

# todo  黔东南 人民政府  | 公共资源 | 发改委| 住建局
def qiandongnan(name):

    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)
        urls = {
            'http://ggzyjyzx.qdn.gov.cn/xwdt/': 6,  # 公共资源 新闻动态
            'http://ggzyjyzx.qdn.gov.cn/zxxx/tzgg/': 3,  # 公共资源 通知公告
            'http://www.qdn.gov.cn/xwzx/tzgg/gstg/': 10,  # 人民政府 公示通告
            'http://www.qdn.gov.cn/xxgk/zdgk/zcjd/zcjd_47822/': 1,  # 人民政府 州级政策解读
            'http://fgw.qdn.gov.cn/xwzx/ywdt/': 12,  # 发改委 要闻动态
            'http://fgw.qdn.gov.cn/xwzx/tzgg/': 1,  # 发改委 通知公告
            'http://fgw.qdn.gov.cn/xwzx/xsdt/': 5,  # 发改委 县市动态
            'http://qdnzzj.qdn.gov.cn/gzdt/bmdt/': 7,  # 住建局 部门动态
            'http://qdnzzj.qdn.gov.cn/gzdt/tzgg/': 15,  # 住建局 通知公告

                   }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'qdn' in url:
                xpath = "//div[@class='text-list']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'fgw' in url:
                xpath = "//div[@class='RightCon Box border MT15 f_r']/div[@class='Box']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath = "//div[@class='NewsList']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    if 'fgw' not in url and i % 6 == 0:
                        pass
                    else:
                        con = driver.page_source
                        html_1 = etree.HTML(con)
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr/td[{i}][')
                        if 'jyzx' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        elif 'xxgk_500454' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[3]/a','[5]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n', '').replace('\t',
                                                                                                                           '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1+ f"/span/text()")[0].strip().replace('\n', '')[:10]

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
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                      driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return qiandongnan(name)


# todo  黔西南 人民政府  | 公共资源 | 发改委(无) | 住建局
def qianxinan(name):

    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        width = driver.execute_script("return document.documentElement.scrollWidth")
        height = driver.execute_script("return document.documentElement.scrollHeight")
        driver.set_window_size(width, height)
        urls = {
            'http://ggzyjy.qxn.gov.cn/zhyw/': 6,  # 公共资源 综合要闻
            'http://ggzyjy.qxn.gov.cn/tzgg_500593/?v=1595408571875': 1,  # 公共资源 通知公告
            'http://ggzyjy.qxn.gov.cn/zwgk_500593/xxgkml/fgwj/': 2,  # 公共资源 政策法规
            'http://www.qxn.gov.cn/zwxx/jzyw/': 87,  # 人民政府 黔西南要闻
            'http://www.qxn.gov.cn/zwxx/xsdt/': 50,  # 人民政府 县市动态
            'http://www.qxn.gov.cn/zwxx/bmdt/': 292,  # 人民政府 部门动态
            'http://www.qxn.gov.cn/zwgk/zfjg/zfzggw_5134990/bmxxgkml/zwxx/': 14,  # 发改委 政务信息
            'http://www.qxn.gov.cn/zwgk/zfjg/zfzggw_5134990/bmxxgkml/bmgg_5134999/': 1,  # 发改委 部门公告
            'http://www.qxn.gov.cn/zwgk/zfjg/zzfcxjsj_5135158/bmxxgkml_5136493/bmgg_5135165/': 5,  # 住建局 部门公告
            'http://www.qxn.gov.cn/zwgk/zfjg/zzfcxjsj_5135158/bmxxgkml_5136493/zwxx_5135162/': 5,  # 住建局 政务信息

                   }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www.qxn' in url:
                xpath = "//div[@class='con']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'fgw' in url:
                xpath = "//div[@class='RightCon Box border MT15 f_r']/div[@class='Box']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath = "//div[@class='NewsList']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                if po > 0: break
                for i in range(1, length):
                    if 'fgw' not in url and i % 6 == 0:
                        pass
                    else:
                        con = driver.page_source
                        html_1 = etree.HTML(con)
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('tr/td[', f'tr/td[{i}][')
                        if 'jyzx' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[2]/a','[3]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        elif 'xxgk_500454' in url:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('%', '').replace('\n','').replace('\t','').replace('\r','')
                            publictime = html_1.xpath(xpath1.replace('[3]/a','[5]')+f"/text()")[0].strip().replace('\n', '')[:10]
                        else:
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('%', '').replace('\n', '').replace('\t',
                                                                                                                           '').replace(
                                '\r', '')
                            publictime = html_1.xpath(xpath1+ f"/span/text()")[0].strip().replace('\n', '').replace('日', '').replace('年', '-').replace('月', '-').replace(']', '').replace('[', '')[:10]

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
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                      driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
    except Exception as e:
        print(f'[{name}] 出错了\n  ', e)
        driver.close()
        return qianxinan(name)

# def start():
    # guizhou1("贵州")
    # guiyang("贵阳")
    # guiyang1("贵阳")
    # liupanshui("六盘水")
    # liupanshui1("六盘水")   # element not interactable  (Session info: headless chrome=80.0.3987.106)
    # zunyi("遵义")
    # zunyi1("遵义")
    # anshun("安顺")  # element not interactable  (Session info: headless chrome=80.0.3987.106)
    # bijie("毕节")

from threading import Thread

t1 = Thread(target=guizhou, args=("贵州",))
t2 = Thread(target=guizhou1, args=("贵州",))
t3 = Thread(target=guiyang, args=("贵阳",))
t4 = Thread(target=guiyang1, args=("贵阳",))

t5 = Thread(target=liupanshui, args=("六盘水",))
t6 = Thread(target=liupanshui1, args=("六盘水",))
t7 = Thread(target=zunyi, args=("遵义",))
t8 = Thread(target=zunyi1, args=("遵义",))

t9 = Thread(target=anshun, args=("安顺",))
t10 = Thread(target=bijie, args=("毕节",))
t11 = Thread(target=tongren, args=("铜仁",))
t12 = Thread(target=qiannan, args=("黔南",))
t13 = Thread(target=qiandongnan, args=("黔东南",))
t14 = Thread(target=qianxinan, args=("黔西南",))

threadl = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14]



def ready3():
    # tt = Thread(target=start)
    # threadl.append(tt)
    for x in threadl:
        x.start()
ready3()
# liupanshui1('六盘水')