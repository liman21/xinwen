# -*- coding: utf-8 -*-
import time, uuid
from dao import Mysql
from lxml import etree
from selenium import webdriver
from datetime import datetime
from openpyxl import load_workbook
import re, os, shutil
gjzs=['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子','保险']
now = datetime.now()
from bs4 import BeautifulSoup
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
pro = '山东'
jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 35
# jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))


# todo  山东 公共资源中心
def shandong(name):
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
            'http://ggzyjyzx.shandong.gov.cn/001/001001/moreinfo.html':9,  #  综合新闻
            'http://ggzyjyzx.shandong.gov.cn/001/001002/moreinfo.html':21, # 工作动态
            'http://ggzyjyzx.shandong.gov.cn/016/moreinfo.html':15, # 机关党建
            'http://ggzyjyzx.shandong.gov.cn/002/002008/moreinfo.html':4, # 通知公告
            'http://www.sdcqjy.com/www/article/zxdt/zxdt/': 14,  # 产权交易 中心动态
            'http://www.sdcqjy.com/www/article/zxdt/mtjj/': 2,  # 产权交易 媒体聚焦
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//ul[@id='listBox']/li/a"
            else:
                xpath = "//li[@class='ewb-list-node clearfix']/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/a', f'][{i}]/').replace('i/a', f'i[{i}]/')
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}a/@onclick")[0].strip().replace('goToInfo(','').replace("'","").split(',')
                    else:
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif 'www' in url:
                                link = f'http://www.sdcqjy.com/www/article/?infoId={href[0]}&categoryId={href[1]}'
                            else:
                                link = 'http://ggzyjyzx.shandong.gov.cn/' + href
                            uid = uuid.uuid4()
                            # go = 0
                            # fo=0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon=qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo+=1
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
                            # if fo>0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            xy=f"//ul[@class='m-pagination-page']/li[{page+1}]/a"
                            if len(html_2.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return shandong(name)

# todo  淄博 公共资源中心
def zibo(name):
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
        urls = {
            'http://ggzyjy.zibo.gov.cn/TPFront/ShowInfo/MoreInfo2.aspx?CategoryNum=024001':17,  # 工作动态
            'http://ggzyjy.zibo.gov.cn/TPFront/zwgk/024002/MoreInfo.aspx?CategoryNum=10242':3, # 通知公告
            'http://ggzyjy.zibo.gov.cn/TPFront/zwgk/024009/MoreInfo.aspx?CategoryNum=24009':2, # 政策解读
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if '024001' in url:
                xpath = "//table[@id='moreinfolist21_DataGrid1']/tbody/tr/td[2]/a"
            else:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"

            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('tr/', f'tr[{i}]/')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        if '024001' in url:
                            publictime = html_1.xpath(f"//table[@id='moreinfolist21_DataGrid1']/tbody/tr[{i}]/td[3]/text()")[0].strip().replace('\n', '')
                        else:
                            publictime = html_1.xpath(f"//table[@id='MoreInfoList1_DataGrid1']/tbody/tr[{i}]/td[3]/text()")[0].strip().replace('\n', '')
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'http://ggzyjy.zibo.gov.cn' + href
                            uid = uuid.uuid4()
                            # go = 0
                            # fo=0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon=qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo+=1
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
                            # if fo>0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if len(html_2.xpath(f'//*[@id="moreinfolist21_Pager"]/div[2]/a[{page - 1}]')) > 0:
                                driver.find_element_by_xpath( f'//*[@id="moreinfolist21_Pager"]/div[2]/a[{page - 1}]').click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return zibo(name)

# todo  枣庄 公共资源中心
def zaozhuang(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.zzggzy.com/TPFront/gzdt/071001/':'1',  # 图片信息
            'http://www.zzggzy.com/TPFront/gzdt/071004/':'1',  # 中心动态
            'http://www.zzggzy.com/TPFront/gzdt/071005/':'1',  # 通知公告
            'http://www.zzggzy.com/TPFront/zcfg/072001/':'1',  # 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//tr[2]/td/table/tbody/tr/td[3]"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, int(pages) + 1):
                if po > 0:
                    break
                for i in range(1, 41,2):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    href = html_1.xpath(f"//tr[2]/td/table/tbody/tr[{i}]/td[3]/a/@href")[0].strip()
                    title = html_1.xpath(f"//tr[2]/td/table/tbody/tr[{i}]/td[3]/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"//tr[2]/td/table/tbody/tr[{i}]/td[4]/text()")[0].strip()[1:-1]
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://www.zzggzy.com' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            # go = 0
                            # fo=0
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
                            # # if go > 0:
                            # #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            # if fo > 0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')

                        if i == lengt:
                            if lengt<length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();",
                                                              driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        return zaozhuang(name)

# todo  东营 公共资源中心
def dongying(name):
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
            'http://ggzy.dongying.gov.cn/dyweb/008/MoreInfo.aspx?CategoryNum=008':2,  # 通知公告
            'http://ggzy.dongying.gov.cn/dyweb/007/MoreInfo.aspx?CategoryNum=007':2,  # 工作动态
            'http://ggzy.dongying.gov.cn/dyweb/003/003001/MoreInfo.aspx?CategoryNum=003001':1,  # 政策法规
            'http://shenpi.dongying.gov.cn/col/col39149/index.html':8,  # 部门动态
            'http://shenpi.dongying.gov.cn/col/col39150/index.html':36,  # 窗口动态
            'http://shenpi.dongying.gov.cn/col/col39152/index.html':14,  # 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'shenpi' in url:
                xpath="//div[@class='default_pgContainer']/div[@class='neirong f_l']/a"
            else:
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1=xpath.replace('r/t',f'r[{i}]/t').replace("']/a",f"'][{i}]/a")
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    if 'shenpi' in url:
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        pu=f'{xpath1.replace("neirong f_l", "riqi f_l").replace("/a", "")}/text()'
                        publictime = html_1.xpath(pu)[0].strip().replace('\n', '')
                    else:
                        title = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1.replace('td[2]/a','td[3]')}/text()")[0].strip().replace('\n','')
                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http' + re.findall('http(.*?)\.cn', url)[0] + '.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            gjzs = ['保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源', '保证金', '政采贷', '平台', '电子', '保险']
                            # go = 0
                            # fo=0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link,
                            #         #           f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
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
                                    # try:
                                    #     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页'))
                                    # except:
                                    #     driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                                    if 'shenpi' in url:
                                        xy="//a[@class='default_pgBtn default_pgNext']"
                                    else:
                                        xy=f'//*[@id="MoreInfoList1_Pager"]/table/tbody/tr/td[2]/a[{page-1}]'
                                    driver.find_element_by_xpath(xy).click()

                            break
                    else:
                        po += 1
                        break


    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return dongying(name)

# todo  烟台 公共资源中心
def yantai(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.yantai.gov.cn/tzgg/index.jhtml':2,  # 通知公告
            'http://ggzyjy.yantai.gov.cn/zwyw/index.jhtml':7,  # 工作动态
            'http://ggzyjy.yantai.gov.cn/zcfggcsh/index.jhtml':2,  # 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zcfggcsh' in url :
                xpath='//li/p[1]/a'
                xy="//ul[@class='pages-list']/li[4]/a"
            else:
                xpath = "//li/div/a"
                xy="//ul[@class='pages-list']/li[10]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+ 1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('li/', f'li[{i}]/')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()

                    if 'zcfggcsh' in url:
                        title1 = html_1.xpath(f"{xpath1}/text()")
                        title=''.join(title1).replace('\t','').replace('\n','').replace('                    ','')
                        publictime = html_1.xpath(f"//li[{i}]/p[2]/text()")[0].strip().replace('.', '-')
                    else:
                        title = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"//li[{i}]/div//div/text()")[0].strip().replace('.','-')

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://ggzyjy.yantai.gov.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                    driver.get(link)
                                    # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon = qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo += 1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo > 0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                                # if len(html_2.xpath(xy))>0:
                                #     driver.find_element_by_xpath(xy).click()
                            break
                    else:
                        po += 1
                        break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return yantai(name)

# todo  潍坊 公共资源中心
def weifang(name):
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
            'http://ggzy.weifang.gov.cn/wfggzy/zytz/048001/':2,  # 重要通知
            'http://ggzy.weifang.gov.cn/wfggzy/gzdt/045001/':3,  # 工作动态
            'http://ggzy.weifang.gov.cn/wfggzy/flfg/002001/':1,  # 法律法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath="//li/a[@class='info-list-name']"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages + 1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    href = html_1.xpath(f"{xpath}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"//li[{i}]/span/text()")[0].strip().replace('.','-')

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://ggzy.weifang.gov.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                    driver.get(link)
                                    # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon = qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo += 1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo > 0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')
                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return weifang(name)

# todo  泰安 公共资源中心
def taian(name):
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
            'http://www.taggzyjy.com.cn/Front/zytz/':2,  # 通知公告
            'http://www.taggzyjy.com.cn/Front/gzdt/':2,  # 工作动态
            'http://www.taggzyjy.com.cn/Front/zcfg/071002/071002003/':1,  # 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = '//*[@id="right_table"]/table/tbody/tr/td[2]/a'
            length = len(html_2.xpath(xpath))
            po = 0
            pp=7
            for page in range(1, pages+ 1):
                if po > 0:
                    break
                for i in range(1, 30,2):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    href = html_1.xpath(f'//*[@id="right_table"]/table/tbody/tr[{i}]/td[2]/a/@href')[0].strip()
                    title = html_1.xpath(f'//*[@id="right_table"]/table/tbody/tr[{i}]/td[2]/a/@title')[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"//tr[{i}]/td[3]/text()")[0].strip().replace('.','-')[1:-1]

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://www.taggzyjy.com.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    driver.get(link)
                                    # get_image(link,
                                    #           f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon = qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo += 1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo > 0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page!=pages:
                                    driver.find_element_by_xpath("//input[@id='GoToPagingNo']").send_keys(f'{page+1}')
                                    driver.find_element_by_xpath("//td[@class='goout']").click()

                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return taian(name)

# todo  日照 公共资源中心
def rizhao(name):
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
            'http://ggzyjy.rizhao.gov.cn/rzwz/zxdt/':6,  # 中心动态
            'http://ggzyjy.rizhao.gov.cn/rzwz/tzgg/':1,  # 通知公告
            'http://ggzyjy.rizhao.gov.cn/rzwz/hydt/':4,  # 行业动态
            'http://ggzyjy.rizhao.gov.cn/rzwz/zcfg/072002/':1,  # 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//li[@class='news-item']/a"
            length = len(html_2.xpath(xpath))
            po = 0
            pp=7
            for page in range(1, pages + 1):
                if po > 0:
                    break
                for i in range(1, 30,2):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/a', f'][{i}]/a')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/div[@class='news-txt l']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/div[@class='news-date r']/text()")[0].strip().replace('.','-')

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://ggzyjy.rizhao.gov.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    driver.get(link)
                                    # get_image(link,
                                    #           f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon = qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo += 1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo > 0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return rizhao(name)

# todo  德州 公共资源中心
def dezhou(name):
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
            'http://ggzyjy.dezhou.gov.cn/TPFront/zytz/':6,  # 通知公告
            'http://fgw.dezhou.gov.cn/n911465/index.html':9,  # 发改委 工作动态
            'http://fgw.dezhou.gov.cn/n911470/index.html':1,  # 发改委 法规规章
            'http://fgw.dezhou.gov.cn/n911460/index.html':4,  # 发改委 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//div[@class='you_con']/table//tr[1]/td[2]/a"
            else:
                xpath = "//li[@class='ewb-list-node clearfix']/a"
            length = len(html_2.xpath(xpath))+1
            po = 0
            for page in range(1, pages + 1):
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace("']/a", f"'][{i}]").replace("table//tr[1]/td[2]/a", f"table[{i}]//tr[1]/td[2]")
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'fgw' in url:
                        publictime = html_1.xpath(f"{xpath1.replace('/td[2]','/td[3]')}/text()")[0].strip()[1:-1]
                    else:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('.','-')

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        elif '../' in href:
                            link = 'http://fgw.dezhou.gov.cn/'+href[3:]
                        else:
                            link = 'http://ggzyjy.dezhou.gov.cn/' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')

                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('>'))
                            break

    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return dezhou(name)


# todo  滨州 公共资源中心
def binzhou(name):
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
            'http://ggzyjy.binzhou.gov.cn/bzweb/009/009001/MoreInfo.aspx?CategoryNum=009001':3,  # 综合新闻

            'http://ggzyjy.binzhou.gov.cn/bzweb/009/009003/MoreInfo.aspx?CategoryNum=009003':1,  # 行业动态

            'http://ggzyjy.binzhou.gov.cn/bzweb/dwgk/020001/MoreInfo.aspx?CategoryNum=020001':4,  # 中心动态
            'http://ggzyjy.binzhou.gov.cn/bzweb/dwgk/020003/MoreInfo.aspx?CategoryNum=020003':6,  # 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//tr[@class='tdstyle']/td[2]/a"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, pages+ 1):
                if po > 0:
                    break
                for i in range(1, 30,2):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/a', f'[{i}]/a')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"//tr[@class='tdstyle'][{i}]/td[3]/text()")[0].strip().replace('.','-')

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://ggzyjy.dezhou.gov.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    driver.get(link)
                                    # get_image(link,
                                    #           f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon = qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo += 1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo > 0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        return binzhou(name)

# todo  菏泽 公共资源中心
def heze(name):
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
            'http://www.hzsggzyjyzx.gov.cn/tblm/011001/about.html':2,  # 动态新闻
            'http://www.hzsggzyjyzx.gov.cn/tblm/011002/about.html':2,  # 通知公告
            'http://www.hzsggzyjyzx.gov.cn/tblm/011004/about.html':2,  # 图片轮播
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//li[@class='ewb-info-item clearfix']/a"
            length = len(html_2.xpath(xpath))
            po = 0
            for page in range(1, int(pages) + 1):
                if po > 0:
                    break
                for i in range(1, 30,2):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/a', f'[{i}]/')
                    href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()

                    publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        if 'http' in href:
                            link = href
                        else:
                            link = 'http://ggzyjy.dezhou.gov.cn' + href
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                        if select == None:
                            uid = uuid.uuid4()

                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    driver.get(link)
                                    # get_image(link,
                                    #           f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon = qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo += 1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break
                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo > 0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        if i == lengt:
                            if lengt < length-1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                    except:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>'))
                            break
                    else:
                        po += 1
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return heze(name)

# todo  济南 公共资源中心
def jinan(name):
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
        urls = {
            'http://jnggzy.jinan.gov.cn/col/col10765/index.html':3,  #  通知公告
            'http://jnggzy.jinan.gov.cn/col/col10766/index.html':3,  #  工作动态
            'http://jnggzy.jinan.gov.cn/col/col14195/index.html':1,  #  地方法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath="//ul[@id='listBox']/li/a"
            else:
                xpath = "//div[@class='default_pgContainer']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]/')
                    if 'www' in url:
                        href = html_1.xpath(f"{xpath1}a/@onclick")[0].strip().replace('goToInfo(','').replace("'","").split(',')
                    else:href = html_1.xpath(f"{xpath1}a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            elif 'www' in url:
                                link =f'http://www.sdcqjy.com/www/article/?infoId={href[0]}&categoryId={href[1]}'
                            else:
                                link = 'http://jnggzy.jinan.gov.cn' + href
                            uid = uuid.uuid4()
                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                    driver.get(link)
                                    # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon=qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo+=1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break

                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo>0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if 'www' in url:
                                if page<=8:
                                    xy=f"//div[@class='page']/a[{page}]"
                                else:
                                    xy=f"//div[@class='page']/a[8]"
                                driver.find_element_by_xpath(xy).click()
                            else:
                                xy=f"//a[@class='default_pgBtn default_pgNext']"
                                if len(html_2.xpath(xy)) > 0:
                                    driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return jinan(name)

# todo  青岛 公共资源中心
def qingdao(name):
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
            'https://ggzy.qingdao.gov.cn/PortalQDManage/PortalQD/NoticeList?category=%E9%80%9A%E7%9F%A5%E5%85%AC%E5%91%8A&noticetype=2':9,  #  通知公告
            'https://ggzy.qingdao.gov.cn/PortalQDManage/PortalQD/NoticeList?category=%E6%9C%8D%E5%8A%A1%E6%8C%87%E5%8D%97&noticetype=2':1,  #  服务指南
            'https://ggzy.qingdao.gov.cn/PortalQDManage/PortalQD/NoticeList?category=%E5%B7%A5%E4%BD%9C%E5%8A%A8%E6%80%81&noticetype=2':3,  #  工作动态
            'https://ggzy.qingdao.gov.cn/PortalQDManage/PortalQD/NoticeList?category=%E5%8C%BA%E5%B8%82%E9%A3%8E%E9%87%87&noticetype=2':2,  #  区市风采
            'http://www.qingdao.gov.cn/n172/n1530/n32936/index.html':1,  # 人民政府 政务要闻
            'http://www.qingdao.gov.cn/n172/n1530/n3177360/index.html':1,  # 人民政府 图片新闻
            'http://www.qingdao.gov.cn/n172/n1530/n2856332/index.html':1,  # 人民政府 区市动态
            'http://www.qingdao.gov.cn/n172/n1530/n32937/index.html':30,  # 人民政府 区市动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath="//div[@class='list03']/ul/li"
            else:
                xpath = "//tr/td[@class='box_td']"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('r/t', f'r[{i}]/t')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if 'www' in url:
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/','-')
                    else:
                        publictime = html_1.xpath(f"//tr[{i}]/td[2]/text()")[0].strip().replace('/','-')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'https://ggzy.qingdao.gov.cn' + href
                            uid = uuid.uuid4()
                            # go = 0
                            # fo=0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon=qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo+=1
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
                            # if fo>0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            xy=f"//a[@class='default_pgBtn default_pgNext']"
                            if len(html_2.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return qingdao(name)
# todo  济宁 公共资源中心
def jining(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzy.jining.gov.cn/JiNing/Posts?CategoryCode=370800001':2,  #  通知公告
            'http://ggzy.jining.gov.cn/JiNing/Posts/Index?CategoryCode=370800009':1,  #  法律法规
            'http://ggzy.jining.gov.cn/JiNing/Posts/Index?CategoryCode=37080000801':2,  #  工作动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//li[@class='list-group-item clearfix']/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/a', f'][{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/','-')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'http://ggzy.jining.gov.cn' + href
                            uid = uuid.uuid4()
                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                    driver.get(link)
                                    # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon=qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo+=1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break

                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo>0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            xy=f"//a[@class='default_pgBtn default_pgNext']"
                            if len(html_2.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return jining(name)
# todo  威海 公共资源中心
def weihai(name):
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
            'http://www.whggzyjy.cn/zxdt/index.jhtml':6,  #  中心动态
            'http://www.whggzyjy.cn/zytz/index.jhtml':8,  #  重要通知
            'http://www.whggzyjy.cn/zcfgzhsz/index.jhtml':1,  #  市级政策法规
            'http://zjj.weihai.gov.cn/col/col28581/index.html':4,  # 建设局  要闻动态
            'http://zjj.weihai.gov.cn/col/col28584/index.html':3,  # 建设局  通知公告
            'http://zjj.weihai.gov.cn/col/col28582/index.html':1,  # 建设局  文件发布
            'http://zjj.weihai.gov.cn/col/col28590/index.html':3,  # 建设局 建筑市场
            'http://zjj.weihai.gov.cn/col/col28583/index.html':2,  # 建设局 	政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if('col28590' or 'col28583') in url:
                xpath="//div[@class='default_pgContainer']//tr/td[3]"
            elif'zjj' in url:
                xpath="//div[@class='list_txt2']/table/tbody/tr/td[1]"
            else:
                xpath = "//li[@class='jygk-li']/div"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace(']/d', f'][{i}]/d').replace(']/t', f'][{i}]/t')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    if ('col28590'or 'col28583') in url:
                        publictime = html_1.xpath(xpath1.replace('td[3]','td[4]')+'/text()')[0].strip()[1:-1]
                    elif 'zjj' in url:
                        publictime = html_1.xpath(xpath1.replace('td[1]','td[2]')+'/text()')[0].strip()[1:-1]
                    else:
                        publictime = html_1.xpath(f"{xpath1}/div/text()")[0].strip().replace('/','-')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'http://www.whggzyjy.cn' + href
                            uid = uuid.uuid4()
                            # go = 0
                            # fo=0
                            # for gjz in gjzs:
                            #     if gjz in title:
                            #         print('含有关键字')
                            #         # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                            #         driver.get(link)
                            #         # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                            #         req_con = driver.page_source
                            #         reqcon=qc_js(req_con)
                            #
                            #         fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                            #         if fj > 0:
                            #             fo+=1
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
                            # if fo>0:
                            #     Mysql.update_xw_xz(biaoti=title, xz='1')
                            # else:
                            #     Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            xy=f"//a[@class='default_pgBtn default_pgNext']"
                            if len(html_2.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return weihai(name)

# todo  临沂 公共资源中心
def linyi(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.linyi.gov.cn/TPFront/zytz/':4,  #  重要通知
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//ul[@class='ewb-news-items ewb-build-items']/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                if po > 0:
                    break
                for i in range(1, length):
                    con = driver.page_source
                    html_1 = etree.HTML(con)
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('i/a', f'i[{i}]')
                    href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('/','-')
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'http://ggzyjy.linyi.gov.cn' + href
                            uid = uuid.uuid4()
                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                    driver.get(link)
                                    # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon=qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo+=1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break

                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo>0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            xy=f"//a[@class='page-next'][1]"
                            if len(html_2.xpath(xy)) > 0:
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return linyi(name)
# todo  聊城 公共资源中心
def liaocheng(name):
    try:
        city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions, executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.lcsggzyjy.cn/lcweb/tzgg/':4,  # 重要通知
            'http://www.lcsggzyjy.cn/lcweb/zhxw/':2,  # 综合新闻
            'http://www.lcsggzyjy.cn/lcweb/zwgk/069001/':2,  # 中心动态
            'http://www.lcsggzyjy.cn/lcweb/bszn/071003/':2,  # 办事指南 > 建设工程
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//tr/td[2]/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):

                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('r/t', f'r[{i}]/t')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                    publictime = html_1.xpath(f"//tr[{i}]/td[3]/font/text()")[0].strip()
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
                    insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            if 'http' in href:
                                link = href
                            else:
                                link = 'http://www.lcsggzyjy.cn' + href
                            uid = uuid.uuid4()
                            go = 0
                            fo=0
                            for gjz in gjzs:
                                if gjz in title:
                                    print('含有关键字')
                                    # mkdir(fr'D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}')
                                    driver.get(link)
                                    # get_image(link, f"D:\png\\{pro}\\{city}\\{publictime[:-3]}\\{publictime}\\{title}.png")
                                    req_con = driver.page_source
                                    reqcon=qc_js(req_con)

                                    fj = len(re.findall('\.pdf|\.doc|\.zip|\.hzb|\.xls', reqcon))
                                    if fj > 0:
                                        fo+=1
                                        print(f'有附件{fj}个')

                                    go += 1
                                    driver.back()
                                    break

                            Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                                               biaoti=title, tianjiatime=insertDBtime, zt='0')
                            print(f'--{city}-【{title}】写入成功')
                            # if go > 0:
                            #     Mysql.update_xw_nr(biaoti=title, zt='1')
                            if fo>0:
                                Mysql.update_xw_xz(biaoti=title, xz='1')
                            else:
                                Mysql.update_xw_xz(biaoti=title, xz='0')

                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                xy="//td[contains(string(),'下页')]"
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return liaocheng(name)

from threading import Thread

t0 = Thread(target=shandong, args=("山东",))
# t1 = Thread(target=zibo, args=("淄博",))
# t2 = Thread(target=zaozhuang, args=("枣庄",))
t3 = Thread(target=dongying, args=("东营",))
# t4 = Thread(target=yantai, args=("烟台",))
# t5 = Thread(target=weifang, args=("潍坊",))
# t6 = Thread(target=taian, args=("泰安",))
# t7 = Thread(target=rizhao, args=("日照",))
t8 = Thread(target=dezhou, args=("德州",))
# t9 = Thread(target=binzhou, args=("滨州",))
# t10 = Thread(target=heze, args=("菏泽",))
# t11 = Thread(target=jinan, args=("济南",))
t12 = Thread(target=qingdao, args=("青岛",))
# t13 = Thread(target=jining, args=("济宁",))
t14 = Thread(target=weihai, args=("威海",))
# t15 = Thread(target=linyi, args=("临沂",))
# t16 = Thread(target=liaocheng, args=("聊城",))

def ready():
    threadl = [
        t0, t12,t14, t3,t8
               ]
    for x in threadl:
        x.start()
ready()

# dezhou('德州')
