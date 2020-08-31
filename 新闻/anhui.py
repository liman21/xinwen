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

gjzs = [ '保函', '中标贷', '电子一体化', '放管服', '履约贷', '金融', '公共资源',
        '保证金', '政采贷', '平台', '电子', '保险', '工程建设', '系统', '营商环境', '中标', '履约政采']
pro = '安徽'
jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 7
def chuli(publictime,href,driver,url,title,city,xpath1):
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
            link = 'http' + re.findall(r'http(.*?)\.cn', url)[0] + '.cn/'+href
        uid = uuid.uuid4()
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

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

# todo  安徽  公共资源中心(无响应) | 发改委 |人民政府 | 住建局
def anhui(name):
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
            'http://fzggw.ah.gov.cn/ywdt/fgyw/index.html': 29,  # 发改委 发改要闻
            'http://fzggw.ah.gov.cn/ywdt/tzgg/index.html': 11,  # 发改委 通知公告
            'http://fzggw.ah.gov.cn/ywdt/gzdt/index.html': 40,  # 发改委 工作动态
            'http://fzggw.ah.gov.cn/ywdt/sxcz/index.html': 23,  # 发改委 市县传真
            'http://www.ah.gov.cn/zwyw/jryw/index.html': 26,  # 人民政府 安徽要闻  264
            'http://www.ah.gov.cn/zwyw/tzgg/index.html': 4,  # 人民政府 通知公告
            'http://dohurd.ah.gov.cn/zx/tjgz/index.html': 3,  # 住建局 推荐关注
            'http://dohurd.ah.gov.cn/zx/gsgg/index.html': 12,  # 住建局 公示公告
            'http://dohurd.ah.gov.cn/zx/jsfc/index.html': 1,  # 住建局 建设风采
            'http://dohurd.ah.gov.cn/zx/tpxw/index.html': 2,  # 住建局 图片新闻
            'http://dohurd.ah.gov.cn/zx/sxdt/index.html': 20,  # 住建局 市县动态
            'http://dohurd.ah.gov.cn/zx/jsyw/index.html': 9,  # 住建局 建设要闻
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fzggw' in url:
                xpath="//div[@class='listnews']/ul/li"
                length = len(html_2.xpath(xpath))
            elif 'dohurd' in url:
                xpath="//div[@class='listnews']/ul/li"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@class='navjz clearfix']/ul/li"
                length = len(html_2.xpath(xpath))
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'fzggw' in url and i%7==0:
                        pass
                    elif 'www.ah' in url and i%6==0:
                        pass
                    else:
                        if 'dohurd' in url:
                            lengt = len(html_1.xpath(xpath))
                        else:
                            lengt = len(html_1.xpath(xpath))-1
                        xpath1 = xpath.replace('/li', f'/li[{i}]/')
                        href = html_1.xpath(f"{xpath1}a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('安徽\t', e)
        driver.close()
        return anhui(name)

# todo  合肥   发改委|人民政府 | 住建局
def hefei(name):
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
            'http://ggzy.hefei.gov.cn/ptdt/001003/about.html': 7,  # 公共资源中心  重要通知
            'http://ggzy.hefei.gov.cn/ptdt/001001/about2.html': 23,  # 公共资源中心  中心动态
            'http://ggzy.hefei.gov.cn/ptdt/001012/about.html': 32,  # 公共资源中心  县区资讯
            'http://www.hfss.gov.cn/zqdh/zfjg/fzhggwyh/gzdt/index.html': 5,  # 发改委 工作动态
            'http://www.hfss.gov.cn/zqdh/zfjg/fzhggwyh/tzgg/index.html': 2,  # 发改委 通知公告
            'http://www.hfss.gov.cn/zqdh/zfjg/fzhggwyh/zcfg/index.html': 1,  # 发改委 政策法规

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzy' in url:
                xpath="//div[@class='ewb-right-bd']/ul/li/a/div/span[1]"
            elif 'www.hfss' in url:
                xpath="//div[@class='navjz']/ul/li/a"
            elif 'szfwj' in url:
                xpath="//div[@class='listnews xxgk_listnews']/ul/li/div"
            elif 'cxjsj' in url:
                xpath="//div[@class='navjz clearfix']/ul/li/a"
            else:
                xpath = "//div[@class='listnews']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www.hefei' in url and i%6==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]/').replace('li/div', f'li[{i}]/div/')

                        if 'ggzy' in url:
                            href = html_1.xpath(xpath1.replace('/div/span[1]','')+f"/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                    '\r', '').replace("'", "")
                            publictime = html_1.xpath(xpath1.replace('/span[1]','/span[2]')+f"/text()")[0].strip().replace('\n', '').replace('\t', '').replace('\r', '')[:10]

                        else:
                            href = html_1.xpath(f"{xpath1}a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            try:
                                title = html_1.xpath(f"{xpath1}a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace("'","")
                            except:
                                title = html_1.xpath(f"{xpath1}a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace("'","")
                            if 'szfwj' in url:
                                publictime = html_1.xpath(f"{xpath1.replace('div/','')}span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            else:
                                publictime = html_1.xpath(f"{xpath1}span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime[:10], "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime[:10], href, driver, url, title, city,xpath1)
                            else:
                                po += 1
                                break
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('合肥\t', e)
        driver.close()
        return hefei(name)
# todo 合肥 人民政府
def hefei1():
    urls={
        'http://www.hefei.gov.cn/content/column/6790181?pageIndex=1':25, # 人民政府 城事播报
        'http://www.hefei.gov.cn/content/column/6790171?pageIndex=1': 25,  # 人民政府 政务要闻
        'http://www.hefei.gov.cn/content/column/6790201?pageIndex=1': 25,  # 人民政府 微观合肥
        'http://www.hefei.gov.cn/content/column/6790211?pageIndex=1': 25,  # 人民政府 信息快递
        'http://www.hefei.gov.cn/content/column/6794811?pageIndex=1': 6,  # 人民政府 公示公告
        'http://www.hefei.gov.cn/content/column/6791771?pageIndex=1': 3,  # 人民政府 市政府文件
        'http://cxjsj.hefei.gov.cn/content/column/6802371?pageIndex=1':  34,  # 住建局 县区动态
        'http://cxjsj.hefei.gov.cn/content/column/6802381?pageIndex=1': 18,  # 住建局 行业动态
        'http://cxjsj.hefei.gov.cn/content/column/6802391?pageIndex=1': 15,  # 住建局 建设局要闻
    }
    for url1, pages in zip(urls.keys(), urls.values()):
        for page in range(1,pages+1):
            url=url1.replace('pageIndex=1',f'pageIndex={page}')
            if 'www' in url:
                headers={
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate',
                    # 'Accept-Language': 'zh-CN,zh;q=0.9',
                    # 'Connection': 'keep-alive',
                    'Cookie': 'yfx_c_g_u_id_10006944=_ck20061015535319102737672832727; __jsluid_h=17dd9c910b3c86c92fbf7858b9430352; __jsl_clearance=1596608545.288|0|NCGDlByX5m71wOvzkUpbEJ3xy80%3D; yfx_f_l_v_t_10006944=f_t_1591775633884__r_t_1596608546282__v_t_1596608546282__r_c_2; hefei_gova_SHIROJSESSIONID=5993e6b8-6ddb-44d6-b5de-19819e29b7e9',
                    'Host': 'www.hefei.gov.cn',
                    # 'Referer': 'http://www.hefei.gov.cn/ssxw/zwyw/index.html',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
                }
            else:
                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    # 'Accept-Encoding': 'gzip, deflate',
                    # 'Accept-Language': 'zh-CN,zh;q=0.9',
                    # 'Connection': 'keep-alive',
                    'Cookie': 'yfx_c_g_u_id_10006944=_ck20061015535319102737672832727; yfx_f_l_v_t_10006944=f_t_1591775633884__r_t_1596608546282__v_t_1596608546282__r_c_2; __jsluid_h=4b41abb3b6ff56e8b433a8b3fd6dbb42; __jsl_clearance=1596610865.099|0|6KQN%2FU%2FsDzAVfNQ%2B4jxeMVgD3v0%3D; hefei_gove_SHIROJSESSIONID=394a2435-f34a-4c0c-a61e-b81761cfe699',
                    'Host': 'cxjsj.hefei.gov.cn',
                    # 'Referer': 'http://www.hefei.gov.cn/ssxw/zwyw/index.html',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
                }
            data={
                'pageIndex': f'{page}'
            }

            con=requests.get(url,headers=headers,params=data).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
            conts=re.findall('<span class="right date">(.*?)</span>            <a href="(.*?)" target="_blank" title="(.*?)" class="left">',con)
            for cont in conts:
                publictime=cont[0]
                href=cont[1]
                title=cont[2]
                city='合肥'
                select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                if select == None:
                    publictime_times = int(time.mktime(time.strptime(publictime[:10], "%Y-%m-%d")))
                    # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                    if publictime_times >= jiezhi_time:
                        uid = uuid.uuid4()
                        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

                        Mysql.insert_xw_nr(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=href,
                                           biaoti=title, tianjiatime=insertDBtime, zt='0')
                        print(f'--{city}-【{title}】写入成功')


# todo  芜湖   发改委 |人民政府 | 住建局
def wuhu(name):
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
            'http://whfgw.wuhu.gov.cn/fgyw/fgyw/index.html': 47,  # 发改委 发改要闻
            'http://whfgw.wuhu.gov.cn/fgyw/tzgg/index.html': 6,  # 发改委 通知公告
            'http://www.wuhu.gov.cn/xwzx/zwyw/index.html': 205,  # 人民政府 政务要闻
            'http://www.wuhu.gov.cn/xwzx/bmdt/index.html': 76,  # 人民政府 部门动态
            'http://www.wuhu.gov.cn/xwzx/xqkx/index.html': 76,  # 人民政府 区县快讯
            'http://www.wuhu.gov.cn/xwzx/tzgg/index.html': 6,  # 人民政府 通知公告
            'http://www.wuhu.gov.cn/public/column/6596211?type=4&catId=6716031&action=list': 25,  # 人民政府 政策解读
            'http://zjw.wuhu.gov.cn/xwzx/zjyw/index.html': 13,  # 住建局 住建要闻
            'http://zjw.wuhu.gov.cn/xwzx/jsdt/index.html': 39,  # 住建局 局属动态
            'http://zjw.wuhu.gov.cn/xwzx/xqdt/index.html': 12,  # 住建局 县区动态
            'http://zjw.wuhu.gov.cn/xwzx/tzgg/index.html': 53,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'whfgw' in url:
                xpath="//div[@class='navjz clearfix']/ul/li"
            elif 'public' in url:
                xpath="//div[@class='xxgk_navli']/ul/li/div"
            elif 'zjw' in url:
                xpath="//div[@class='navjz clearfix']/ul/li"
            else:
                xpath = "//div[@class='navjz clearfix']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i%7==0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]').replace("li']/ul", f"li'][{i}]/ul")
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a[@class='title']/text()")[1].strip().replace('\n','').replace('            ','')
                        if 'public' in url:
                            pp=f"{xpath1.replace('i/div','i')}"+"[@class='rq']"+'/text()'
                            publictime = html_1.xpath(pp)[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('芜湖\t', e)
        driver.close()
        return wuhu(name)

# todo  蚌埠   发改委 |人民政府 | 住建局
def bengbu(name):
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
            'http://dpc.bengbu.gov.cn/xwdt/gzdt/index.html': 26,  # 发改委 工作动态
            'http://dpc.bengbu.gov.cn/xwdt/tzgg/index.html': 8,  # 发改委 通知公告
            'http://dpc.bengbu.gov.cn/xwdt/tpxw/index.html': 5,  # 发改委 图片新闻
            'http://www.bengbu.gov.cn/ywdt/bbxw/index.html': 152,  # 人民政府 蚌埠新闻
            'http://www.bengbu.gov.cn/ywdt/xqdt/index.html': 157,  # 人民政府 县区动态
            'http://www.bengbu.gov.cn/ywdt/bmdt/index.html': 75,  # 人民政府 部门动态
            'http://www.bengbu.gov.cn/ywdt/gsgg/index.html': 7,  # 人民政府 公示公告
            'http://www.bengbu.gov.cn/zwgk/zcfg/szfwj/index.html': 3,  # 人民政府 市政府文件
            'http://zjj.bengbu.gov.cn/xwdt/tzgg/index.html': 8,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zcfg' in url:
                xpath="//div[@class='listnews gklist']/ul/li/div"
            else:
                xpath = "//div[@class='listnews']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i % 6 == 0:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]').replace("i/d", f"i[{i}]/d")
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a[@class='title']/text()")[1].strip().replace('\n','').replace('\t','').replace('\r','').replace('            ','')
                        if 'zcfg' in url:
                            pp=f"{xpath1.replace(']/div',']/')}"+'span/text()'
                            publictime = html_1.xpath(pp)[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('蚌埠\t', e)
        driver.close()
        return bengbu(name)

# todo  淮南   发改委 |人民政府 | 住建局
def huainan(name):
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
            'http://fgw.huainan.gov.cn/tzgg/index.html': 6,  # 发改委 通知公告
            'http://fgw.huainan.gov.cn/xqdt/index.html': 7,  # 发改委 区县动态
            'http://fgw.huainan.gov.cn/gzdt/index.html': 30,  # 发改委 工作动态
            'http://fgw.huainan.gov.cn/ywgz/zcfg/zcjd/index.html': 2,  # 发改委 政策解读
            'http://www.huainan.gov.cn/zwgk/jrhn/index.html': 192,  # 人民政府 今日淮南
            'http://www.huainan.gov.cn/zwgk/bmdt/index.html': 33,  # 人民政府 部门动态
            'http://www.huainan.gov.cn/zwgk/xqdt/index.html': 54,  # 人民政府 区县动态
            'http://www.huainan.gov.cn/zwgk/tzgg/index.html': 5,  # 人民政府 通知公告
            'http://cjj.huainan.gov.cn/tzgg/index.html': 5,  # 住建局 通知公告
            'http://cjj.huainan.gov.cn/cxjs/index.html': 8,  # 住建局 城乡建设
            'http://cjj.huainan.gov.cn/xqzx/index.html': 4,  # 住建局 县区资讯
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//div[@class='navjz clearfix']/ul/li"
                length = len(html_2.xpath(xpath))+ 1
            else:
                xpath="//div[@class='navjz']/ul/li"
                length = len(html_2.xpath(xpath))
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i%7==0:
                        pass
                    else:
                        if 'fgw' in url:
                         lengt = len(html_1.xpath(xpath))
                        else:
                         lengt = len(html_1.xpath(xpath))-1
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('淮南\t', e)
        driver.close()
        return huainan(name)

# todo  马鞍山   发改委 |人民政府 | 住建局
def maanshan(name):
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
            'http://fgw.mas.gov.cn/xxfb/gzdt/index.html': 29,  # 发改委 工作动态
            'http://fgw.mas.gov.cn/xxfb/tzgg/index.html': 5,  # 发改委 通知公告
            'http://fgw.mas.gov.cn/xxfb/fgzc/index.html': 3,  # 发改委 发改政策
            'http://www.mas.gov.cn/zxzx/zwyw/index.html': 231,  # 人民政府 政务要闻
            'http://www.mas.gov.cn/zxzx/bmdt/index.html': 272,  # 人民政府 部门动态
            'http://www.mas.gov.cn/zxzx/qxdt/index.html': 975,  # 人民政府 区县动态
            'http://www.mas.gov.cn/zxzx/tzgg/index.html': 11,  # 人民政府 通知公告
            'http://www.mas.gov.cn/zxzx/mtjj/index.html': 16,  # 人民政府 媒体聚焦
            'http://zjj.mas.gov.cn/xxfb/gzdt/index.html': 87,  # 住建局 工作动态
            'http://zjj.mas.gov.cn/xxfb/tzgg/index.html': 12,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='listnews ztlmpic']/ul/li/p[@class='p2']"
            else:
                xpath = "//div[@class='navjz']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i==1:
                        pass
                    else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]').replace('i/p', f'i[{i}]/p')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'www' in url:
                            pp=f"{xpath1[:-13]}"+"[@class='p3']/text()"
                            publictime = html_1.xpath(pp)[0].strip().replace('年','-').replace('月','-').replace('日','')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip()
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('马鞍山\t', e)
        driver.close()
        return maanshan(name)


# todo  淮北   发改委 |人民政府 | 住建局
def huaibei(name):
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
            'http://fgw.huaibei.gov.cn/fgdt/fgdt/index.html': 28,  # 发改委 发改动态
            'http://fgw.huaibei.gov.cn/fgdt/zcfg/index.html': 2,  # 发改委 政策法规
            'http://fgw.huaibei.gov.cn/fgdt/tzgg/index.html': 5,  # 发改委 通知公告
            'http://fgw.huaibei.gov.cn/fgdt/tpxw/index.html': 14,  # 发改委 图片新闻
            'http://www.huaibei.gov.cn/xwzx/zwyw/index.html': 57,  # 人民政府 政务要闻
            'http://www.huaibei.gov.cn/xwzx/xqkx/index.html': 181,  # 人民政府 区县快讯
            'http://www.huaibei.gov.cn/xwzx/gsgg/zw/index.html': 11,  # 人民政府  新闻中心 > 公示公告 > 政务
            'http://hbxxgk.huaibei.gov.cn/public/column/15?type=4&catId=4743391&action=list': 1,  # 人民政府 政策法规
            'http://hbxxgk.huaibei.gov.cn/public/column/15?type=4&action=list': 184,  # 人民政府 政府信息公开目录
            'http://hbzjj.huaibei.gov.cn/xwzx/zxzx/index.html': 50,  # 住建局 住建新闻
            'http://hbzjj.huaibei.gov.cn/xwzx/tzgg/index.html': 14,  # 住建局 通知公告
            'http://hbzjj.huaibei.gov.cn/xwzx/bsyw/index.html': 4,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@id='mm2']/ul/li"
                length = len(html_2.xpath(xpath))
            elif 'hbxxgk' in url:
                xpath = "//div[@class='xxgk_navli']/ul/li/div"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@class='navjz']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i==1:
                        pass
                    else:
                        if 'www' in url:
                            lengt = len(html_1.xpath(xpath))-1
                        else:
                            lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]').replace('i/p', f'i[{i}]/p')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'hbxxgk' in url:
                            publictime = html_1.xpath(f"{xpath1[:-4]}"+"[@class='rq']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('淮北\t', e)
        driver.close()
        return huaibei(name)

# todo  铜陵   发改委 |人民政府
def tongling(name):
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
            'http://fzggw.tl.gov.cn/xxzx/3849/': 21,  # 发改委 工作动态
            'http://fzggw.tl.gov.cn/xxzx/3851/': 28,  # 发改委 通知公告
            'http://www.tl.gov.cn/zxzx/xwzx/135/': 36,  # 人民政府 政务要闻
            'http://www.tl.gov.cn/zxzx/xwzx/136/': 36,  # 人民政府 部门信息
            'http://www.tl.gov.cn/zxzx/gsgg/140/': 36,  # 人民政府 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@id='mm2']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath = "//div[@class='o_rg_down']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i==1:
                        pass
                    else:
                        if 'www' in url:
                            lengt = len(html_1.xpath(xpath))-1
                        else:
                            lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]').replace('i/p', f'i[{i}]/p')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'fzggw' in url:
                            publictime = html_1.xpath(f"{xpath1}/text()")[1].strip().replace('\n','').replace('\t','').replace('\r','').replace('                            ','')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('铜陵\t', e)
        driver.close()
        return tongling(name)
# todo   铜陵(ij)  住建局
def tongling1(name):
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
            'http://zfcxjsj.tl.gov.cn/jsxw/':25,  # 住建局 建设新闻
            'http://zfcxjsj.tl.gov.cn/zwgk/wjgk_1/zcfg/':1,  # 住建局 政策法规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con1 = driver.page_source
            html_2 = etree.HTML(con1)
            xpath = "//div[@class='bd_content']/ul/li/ul/li"
            jj = 5
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
                        xpath1 = xpath.replace('ul/li/ul/li', f'ul/li[{j}]/ul/li[{i}]/a')
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('·  ','').replace('\n','').replace('\t','').replace('\r','')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
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
                                        driver.find_element_by_xpath(  "//a[@class='default_pgBtn default_pgNext']").click()
    except Exception as e:
        print('铜陵1\t',e)
        driver.close()
        return tongling1(name)

# todo  安庆   发改委 |人民政府 | 住建局
def anqing(name):
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
            'http://fgw.anqing.gov.cn/zxzx/fgyw/index.html': 12,  # 发改委 发改要闻
            'http://fgw.anqing.gov.cn/zxzx/xqdt/index.html': 6,  # 发改委 县区动态
            'http://fgw.anqing.gov.cn/zxzx/zhjj/index.html': 8,  # 发改委 综合经济
            'http://fgw.anqing.gov.cn/zxzx/tzgg/index.html': 2,  # 发改委 通知公告
            'http://www.anqing.gov.cn/xwxx/zwyw/index.html': 183,  # 人民政府 政务要闻
            'http://www.anqing.gov.cn/xwxx/qxdt/index.html': 259,  # 人民政府 区县动态
            'http://www.anqing.gov.cn/xwxx/bmdt/index.html': 214,  # 人民政府  部门动态
            'http://www.anqing.gov.cn/xwxx/zcdt/index.html': 7,  # 人民政府 政策动态
            'http://aqzjj.anqing.gov.cn/xwzx/zjyw/index.html': 33,  # 住建局 住建要闻
            'http://aqzjj.anqing.gov.cn/xwzx/tzgg/index.html': 28,  # 住建局 通知公告
            'http://aqzjj.anqing.gov.cn/xwzx/bmdt/index.html': 17,  # 住建局 部门动态
            'http://aqzjj.anqing.gov.cn/xwzx/xqdt/index.html': 25,  # 住建局 县区动态
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//div[@class='o_rg_down']/ul/li/a"
                length = len(html_2.xpath(xpath)) + 1
            else:
                xpath = "//div[@class='navjz']/ul/li"
                if 'www' in url:
                    length = len(html_2.xpath(xpath))
                else:
                    length = len(html_2.xpath(xpath))+1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'www' in url and i%6==0:
                        pass
                    else:
                        if 'www' in url:
                            lengt = len(html_1.xpath(xpath))-1
                        else:
                            lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('i/a', f'i[{i}]').replace('i/p', f'i[{i}]/p')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        if 'fzggw' in url:
                            publictime = html_1.xpath(f"{xpath1}/text()")[1].strip().replace('\n','').replace('\t','').replace('\r','').replace('                            ','')
                        else:
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('安庆',e)
        driver.close()
        return anqing(name)

# todo  黄山   发改委 |人民政府 | 住建局
def huangshan(name):
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
            # 'http://fgw.huangshan.gov.cn/BranchOpennessContent/showList/10374/300100/page_1.html': 35,  # 发改委 工作动态
            # 'http://fgw.huangshan.gov.cn/BranchOpennessContent/showList/10374/0/page_1.html': 79,  # 发改委 最新公开
            # 'http://fgw.huangshan.gov.cn/BranchOpennessContent/showList/10374/40400/page_1.html': 79,  # 发改委 政策解读
            # 'http://fgw.huangshan.gov.cn/Content/showList/JA002/30900/1/page_1.html': 15,  # 发改委 区县信息
            # 'http://fgw.huangshan.gov.cn/Content/showList/JA002/30904/1/page_1.html': 4,  # 发改委 通知公告
            'http://zw.huangshan.gov.cn/OpennessContent/showList/10373/280000/page_1.html': 79,  # 人民政府 政策解读
            'http://www.huangshan.gov.cn/News/showList/9/page_1.html': 233,  # 人民政府 政务要闻
            'http://www.huangshan.gov.cn/News/showList/10/page_1.html': 180,  # 人民政府 部门动态
            'http://www.huangshan.gov.cn/News/showList/11/page_1.html': 219,  # 人民政府 区县动态
            'http://www.huangshan.gov.cn/News/showList/14/page_1.html': 8,  # 人民政府 通知公告
            'http://zjj.huangshan.gov.cn/BranchOpennessContent/showList/10387/300100/page_1.html': 40,  # 住建局 工作动态
            'http://zjj.huangshan.gov.cn/Content/showList/JA015/15771/1/page_1.html': 36,  # 住建局 区县动态
            'http://zjj.huangshan.gov.cn/Content/showList/JA015/32104/1/page_1.html': 15,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'BranchOpennessContent' in url:
                xpath = "//dl[@class='content-list']/dt/div/div/a"
                length = len(html_2.xpath(xpath))+1
            elif 'zw' in url:
                xpath = "//dl[@class='content-list']/dt/div/div/a"
                length = 16
            elif 'fgw' in url:
                xpath = "//dl[@class='key-list']/dt"
                length = len(html_2.xpath(xpath))+1
            else:
                xpath = "//div[@class='l-cont']/dl/dt"
                length = len(html_2.xpath(xpath))
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        if 'www' in url or 'zw' in url:
                             lengt = len(html_1.xpath(xpath))-1
                        else:lengt = len(html_1.xpath(xpath))
                        if ('www' in url or 'zw' in url) and i%6==0:
                            pass
                        else:
                            xpath1 = xpath.replace('/dt', f'/dt[{i}]').replace('div/a', f'div')
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            try:
                                title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            if 'zw' in url or '10387' in url or 'BranchOpennessContent' in url:
                                publictime = html_1.xpath(xpath1.replace(f'/div/div','')+f"/span[@class='cont-time']/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('                            ','')
                            elif 'www'  in url:
                                publictime = html_1.xpath(xpath1+'/span[1]/text()')[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('                            ','')
                            else:
                                publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                        try:
                                            driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('黄山',e)
        driver.close()
        return huangshan(name)


# todo  滁州   发改委 |人民政府 | 住建局
def chuzhou(name):
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
            'http://fgw.chuzhou.gov.cn/xwdt/fgyw/index.html': 11,  # 发改委 发改要闻
            'http://fgw.chuzhou.gov.cn/xwdt/xtdt/index.html': 35,  # 发改委 系统动态
            'http://fgw.chuzhou.gov.cn/xwdt/tzgg/index.html': 6,  # 发改委 通知公告
            'http://www.chuzhou.gov.cn/zxzx/jryw/index.html': 19,  # 人民政府 今日要闻
            'http://www.chuzhou.gov.cn/zxzx/bmdt/index.html': 36,  # 人民政府 部门动态
            'http://www.chuzhou.gov.cn/zxzx/gsgg/index.html': 23,  # 人民政府 公告公示
            'http://zfcxjsj.chuzhou.gov.cn/xxfb/bjdt/index.html': 16,  # 住建局 本局动态
            'http://zfcxjsj.chuzhou.gov.cn/xxfb/xqdt/index.html': 7,  # 住建局 县区动态
            'http://zfcxjsj.chuzhou.gov.cn/xxfb/tzgg/tzgg/index.html': 4,  # 住建局 通知公告

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'fgw' in url:
                xpath = "//div[@class='listnews']/ul/li"
                length = len(html_2.xpath(xpath)) + 1
            elif 'zfcxjsj' in url:
                xpath = "//div[@class='navjz']/ul/li"
                length = len(html_2.xpath(xpath))
            else:
                xpath = "//div[@class='listnews']/ul/li"
                length = len(html_2.xpath(xpath))

            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        if ('www' in url or'zfcxjsj' in url) and i%6==0:
                            pass
                        else:
                            if 'fgw' in url:
                                 lengt = len(html_1.xpath(xpath))
                            else:lengt = len(html_1.xpath(xpath))-1
                            xpath1 = xpath.replace('/li', f'/li[{i}]')
                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            try:
                                title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                            except:
                                title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                            select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                        try:
                                            driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                                break
    except Exception as e:
        print('滁州',e)
        driver.close()
        return chuzhou(name)

# todo  阜阳   发改委 |人民政府(响应慢) | 住建局
def fuyang(name):
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
            'http://fgw.fy.gov.cn/content/channel/5705d9d1ceab06394fbcc502/': 11,  # 发改委 工作动态
            'http://fgw.fy.gov.cn/content/channel/5704a894ceab060a66bcc503/': 10,  # 发改委 区县动态
            'http://fgw.fy.gov.cn/content/channel/5704a894ceab060a66bcc505/': 8,  # 发改委 通知公告
            'http://www.fy.gov.cn/content/channel/54509804dfdd2e8475a9dad2/': 19,  # 人民政府 阜阳要闻
            'http://www.fy.gov.cn/content/channel/54509804dfdd2e8475a9dad3/': 21,  # 人民政府 区县动态
            'http://www.fy.gov.cn/content/channel/54509804dfdd2e8475a9dad4/': 25,  # 人民政府 部门动态
            'http://www.fy.gov.cn/content/channel/54509807dfdd2e8475a9e38b/': 45,  # 人民政府 公告公示
            'http://cxjsj.fy.gov.cn/content/channel/5acabc767f8b9ade4c304a2a/': 3,  # 住建局 县区动态
            'http://cxjsj.fy.gov.cn/content/channel/5acabc697f8b9ad34c435e3e/': 30,  # 住建局 建设要闻
            'http://cxjsj.fy.gov.cn/content/channel/5acabc937f8b9aed4caa3474/': 9,  # 住建局 本级文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='listright-box']/ul/li"
            length = len(html_2.xpath(xpath))+1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        # if 'fgw' in url:
                        #      lengt = len(html_1.xpath(xpath))
                        # else:lengt = len(html_1.xpath(xpath))-1
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('阜阳',e)
        driver.close()
        return fuyang(name)


# todo  宿州   发改委 |人民政府(响应慢) | 住建局
def suzhou(name):
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
            'http://fagaiwei.ahsz.gov.cn/fgzx/zhzx/fgyw/index.html': 24,  # 发改委 发改要闻
            'http://fagaiwei.ahsz.gov.cn/fgzx/zhzx/xqdt/index.html': 5,  # 发改委 县区动态
            'http://fagaiwei.ahsz.gov.cn/fgzx/zhzx/tzgg/index.html': 6,  # 发改委 通知公告
            'http://www.ahsz.gov.cn/zwzx/zwyw/index.html': 80,  # 人民政府 政务要闻
            'http://www.ahsz.gov.cn/zwzx/bmdt/index.html': 167,  # 人民政府 部门动态
            'http://www.ahsz.gov.cn/zwzx/xqyq/index.html': 87,  # 人民政府 部门动态
            'http://zjj.ahsz.gov.cn/zwzx/gsgg/index.html': 12,  # 人民政府 公示公告
            'http://zjj.ahsz.gov.cn/zwzx/wjtz/index.html': 4,  # 人民政府 文件通知
            'http://zjj.ahsz.gov.cn/zwzx/xqxx/index.html': 2,  # 人民政府 县区信息
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='navjz']/ul/li"
            if 'zjj' in url:
                length = len(html_2.xpath(xpath))+1
            else:length = len(html_2.xpath(xpath))
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    if 'zjj' in url:
                        lengt = len(html_1.xpath(xpath))
                    else:
                        lengt = len(html_1.xpath(xpath))-1
                    if 'www' in url and i%7==0:
                        pass
                    elif 'fagaiwei' in url and i%6==0:
                        pass
                    else:
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('宿州',e)
        driver.close()
        return suzhou(name)

# todo  六安   发改委 |人民政府| 住建局
def liuan(name):
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
            'http://fgw.luan.gov.cn/zwzx/gsgg/index.html': 7,  # 发改委 公示公告
            'http://fgw.luan.gov.cn/zwzx/xqcz/index.html': 6,  # 发改委 区县传真
            'http://fgw.luan.gov.cn/zwzx/fgyw/index.html': 16,  # 发改委 发改要闻
            'http://www.luan.gov.cn/zwzx/jrla/zxyw/index.html': 19,  # 人民政府 最新要闻
            'http://www.luan.gov.cn/zwzx/jrla/dtxx/index.html': 19,  # 人民政府 动态信息
            'http://www.luan.gov.cn/zwzx/gsgg/index.html': 8,  # 人民政府 公示公告
            'http://zjj.luan.gov.cn/zwzx/gzdt/index.html': 30,  # 住建局 工作动态
            'http://zjj.luan.gov.cn/zwzx/xqdt/index.html': 11,  # 住建局 县区动态
            'http://zjj.luan.gov.cn/zwzx/gsgg/hytz/index.html': 1,  # 住建局 会议通知
            'http://zjj.luan.gov.cn/zwzx/jfwj/index.html': 9,  # 住建局 局发文件
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            xpath = "//div[@class='navjz clearfix']/ul/li"
            length = len(html_2.xpath(xpath))+1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('六安',e)
        driver.close()
        return liuan(name)


# todo  毫州   发改委 |人民政府 | 住建局
def haozhou(name):
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
            'http://fgw.bozhou.gov.cn/News/showList/3065/page_1.html': 9,  # 发改委 发改动态
            'http://fgw.bozhou.gov.cn/News/showList/3066/page_1.html': 6,  # 发改委 综合信息
            'http://fgw.bozhou.gov.cn/News/showList/3067/page_1.html': 3,  # 发改委 通知公告
            'http://fgw.bozhou.gov.cn/News/showList/3083/page_1.html': 12,  # 发改委 县区动态
            'http://www.bozhou.gov.cn/News/showList/1359/page_1.html': 333,  # 人民政府 政务要闻
            'http://www.bozhou.gov.cn/News/showList/1364/page_1.html': 290,  # 人民政府 县区动态
            'http://www.bozhou.gov.cn/News/showList/1363/page_1.html': 236,  # 人民政府 部门动态
            'http://zjj.bozhou.gov.cn/News/showList/4795/page_1.html': 14,  # 住建局 建设要闻
            'http://zjj.bozhou.gov.cn/News/showList/4797/page_1.html': 44,  # 住建局 通知公告
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='m-listcg m-liststyle1 f-md-mb15']/ul/li"
            else:
                xpath = "//div[@class='news-container']/ul/li"
            length = len(html_2.xpath(xpath))+1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('毫州\t', e)
        driver.close()
        return haozhou(name)

# todo  池州   发改委 |人民政府| 住建局(有时无响应)
def chizhou(name):
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
            'http://fgw.chizhou.gov.cn/News/showList/1450/page_1.html': 1,  # 发改委 工作动态
            'http://fgw.chizhou.gov.cn/News/showList/1451/page_1.html': 3,  # 发改委 通知公告
            'http://www.chizhou.gov.cn/News/showList/8/page_1.html': 132,  # 人民政府 政务要闻
            'http://www.chizhou.gov.cn/News/showList/9/page_1.html': 77,  # 人民政府 县区动态
            'http://www.chizhou.gov.cn/News/showList/10/page_1.html': 68,  # 人民政府 部门传真
            'http://zjw.chizhou.gov.cn/News/showList/3496/page_1.html': 9,  # 住建局 建设要闻
            'http://zjw.chizhou.gov.cn/News/showList/3501/page_1.html': 3,  # 住建局 县区动态
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='m-cglists m-liststyle1']/ul/li"
            else:
                xpath = "//td[@class='rightnr']/ul/li"
            length = len(html_2.xpath(xpath))+1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()

                                    except:
                                        try:
                                            driver.find_element_by_xpath("//ul[@id='paging']/li[8]/a").click()
                                        except:
                                            try:
                                                driver.execute_script("arguments[0].click();",  driver.find_element_by_link_text('下页'))
                                            except:
                                                driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('池州',e)
        driver.close()
        return chizhou(name)

# todo  宣城   发改委 |人民政府| 住建局(有时无响应)
def xuancheng(name):
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
            'http://fgw.xuancheng.gov.cn/News/showList/1556/page_1.html': 11,  # 发改委 发改要闻
            'http://fgw.xuancheng.gov.cn/News/showList/1548/page_1.html': 6,  # 发改委 通知公告
            'http://fgw.xuancheng.gov.cn/News/showList/1549/page_1.html': 20,  # 发改委 上级动态
            'http://www.xuancheng.gov.cn/News/showList/6218/page_1.html': 10,  # 人民政府 宣城要闻  74
            'http://www.xuancheng.gov.cn/News/showList/6219/page_1.html': 13,  # 人民政府 县区动态  73
            'http://www.xuancheng.gov.cn/News/showList/6220/page_1.html': 11,  # 人民政府 部门动态  118
            'http://zjj.xuancheng.gov.cn/News/showList/3080/page_1.html': 17,  # 住建局 公告发布
            'http://zjj.xuancheng.gov.cn/News/showList/3095/page_1.html': 10,  # 住建局 工作动态
            }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'www' in url:
                xpath = "//div[@class='m-cglists m-liststyle1']/ul/li"
            else:
                xpath = "//div[@class='listright-box']/ul/li"
            length = len(html_2.xpath(xpath))+1
            pages = int(pages)
            po = 0
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]')
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        try:
                            title = html_1.xpath(f"{xpath1}/a/@title")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        except:
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','').replace('[','').replace(']','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在
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
                                    try:
                                        driver.find_element_by_xpath("//a[@class='default_pgBtn default_pgNext']").click()
                                    except:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))
                            break
    except Exception as e:
        print('宣城',e)
        driver.close()
        return xuancheng(name)


from threading import Thread
t0 = Thread(target=anhui, args=("安徽",))
t1 = Thread(target=hefei, args=("合肥",))
t2 = Thread(target=wuhu, args=("合肥",))
t3 = Thread(target=bengbu, args=("蚌埠",))
t4 = Thread(target=huainan, args=("淮南",))
t5 = Thread(target=maanshan, args=("马鞍山",))
t6 = Thread(target=huaibei, args=("淮北",))
t7 = Thread(target=tongling, args=("铜陵",))
t77 = Thread(target=tongling1, args=("铜陵",))
t8 = Thread(target=anqing, args=("安庆",))
t9 = Thread(target=huangshan, args=("黄山",))
t10 = Thread(target=chuzhou, args=("滁州",))
t11= Thread(target=fuyang, args=("阜阳",))
t12= Thread(target=suzhou, args=("宿州",))
t13 = Thread(target=liuan, args=("六安",))
t14 = Thread(target=haozhou, args=("毫州",))
t15 = Thread(target=chizhou, args=("池州",))
t16 = Thread(target=xuancheng, args=("宣城",))

def ready4():
    anhui('安徽')
    hefei('合肥')
    hefei1()
    wuhu('芜湖')
    bengbu('蚌埠')
    huainan('淮南')
    maanshan('马鞍山')  # 已爬完
    huaibei('淮北')
    tongling('铜陵')
    tongling1('铜陵')
    anqing('安庆')
    huangshan('黄山')  # list out of range  有问题
    chuzhou('滁州')
    fuyang('阜阳')
    suzhou('宿州')
    liuan('六安')
    haozhou('毫州')
    chizhou('池州')
    xuancheng('宣城')
#
# threadl = [
#            t8,t9,t10,t11,t12,t13,t14,t15,t16
# ]
# tt = Thread(target=start)
# threadl.append(tt)
#
# def ready4():
#     for x in threadl:
#         x.start()
#
#
ready4()
# bengbu('蚌埠')


