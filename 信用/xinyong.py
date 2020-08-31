# -*- coding: utf-8 -*-
import time, uuid, requests, json
from dao import Mysql
from lxml import etree
from selenium import webdriver
from datetime import datetime
from openpyxl import load_workbook
import re, os, shutil
now = datetime.now()

def chuli(publictime,href,driver,url,title,city,xpath1,pro):
    try:

        if len(href)==0:
            link = href

        elif re.findall('http', href):
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
        insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        uid = uuid.uuid4()
        Mysql.insert_xw_nrxy(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link,
                           biaoti=title, tianjiatime=insertDBtime, zt='0')
        Mysql.update_xw_nrxy(xy=1,prid=uid)
        print(f'--{city}-【{title}】写入成功')

    except Exception as e:
        print('写入出错\t', e)

# jiezhi_time = int(time.mktime(time.strptime(now.strftime("%Y-%m-%d"), "%Y-%m-%d"))) - 86400 * 7
jiezhi_time = int(time.mktime(time.strptime(now.strftime("2019-01-01"), "%Y-%m-%d")))

# todo  安徽   公共资源中心
def anhui(name):
    try:
        pro='安徽'
        # city = name
        print(f"安徽程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            # 'http://ggzy.hefei.gov.cn/pgt/005001/badBehavior.html': 10,  # 合肥   曝光台>不良行为  公司
            # 'http://ggzy.hefei.gov.cn/pgt/005002/govPunish.html': 1,  # 合肥   曝光台>行政处罚   公司
            # 'http://whsggzy.wuhu.gov.cn/xyzl/subpagexyzl.html': 5,  # 芜湖   信用专栏 （下载、pdf、评审专家）
            # 'http://ggzy.bengbu.gov.cn/bbfwweb/xygk/025002/025002001/MoreInfo.aspx?CategoryNum=025002001': 1,  # 蚌埠    曝光台 >> 市区
            # 'http://ggzy.bengbu.gov.cn/bbfwweb/xygk/025002/025002002/MoreInfo.aspx?CategoryNum=025002002': 3,  # 蚌埠   曝光台 >> 怀远县
            # 'http://ggzy.bengbu.gov.cn/bbfwweb/xygk/025002/025002003/MoreInfo.aspx?CategoryNum=025002003': 3,  # 蚌埠    曝光台 >> 五河县
            # 'http://ggzy.bengbu.gov.cn/bbfwweb/xygk/025002/025002004/MoreInfo.aspx?CategoryNum=025002004': 3,  # 蚌埠    曝光台 >>  固镇县
            # 'http://ggj.huainan.gov.cn/xyxxgs/xzxkhxzcfsgssxml/index.html': 1,  # 淮南  行政许可和行政处罚双公示事项 目录
            # 'http://ggj.huainan.gov.cn/xyxxgs/xzcf/index.html': 6,  # 淮南  行政处罚
            # 'http://ggzy.huaibei.gov.cn/hbweb/xypt/006006/MoreInfo.aspx?CategoryNum=006006': 3,  # 淮北  信用平台 >> 信用信息
            # 'http://ggzyjyzx.tl.gov.cn/tlsggzy/xypt/002001/': 3,  # 铜陵  曝光台 >> 投诉处理
            # 'http://ggzyjyzx.tl.gov.cn/tlsggzy/xypt/002002/': 3,  # 铜陵  曝光台 >> 行政处罚
            # 'http://ggzyjyzx.tl.gov.cn/tlsggzy/xypt/002006/': 1,  # 铜陵  曝光台 >> 信用记录
            # 'http://ggzyjyzx.tl.gov.cn/tlsggzy/xypt/002005/': 1,  # 铜陵  曝光台 >> 其他
            # 'http://ggzy.huangshan.gov.cn/009/subpage.html': 3,  # 黄山  曝光台
            # 'http://jyzx.fy.gov.cn/FuYang/bgt/': 1,  # 阜阳  曝光台
            # 'http://jyzx.fy.gov.cn/FuYang/xypt/044001/': 1,  # 阜阳  违法违规
            # 'http://jyzx.fy.gov.cn/FuYang/xypt/044002/': 4,  # 阜阳  处罚
            # 'http://jyzx.fy.gov.cn/FuYang/xypt/044003/': 1,  # 阜阳  黑名单
            # 'http://jyzx.fy.gov.cn/FuYang/xypt/044004/': 1,  # 阜阳  撤销黑名单
            # 'http://ggzyjy.ahsz.gov.cn/szfront/xycx/018005/': 1,  # 宿州  信用监管 > 招标人
            # 'http://ggzyjy.ahsz.gov.cn/szfront/xycx/018006/': 2,  # 宿州  信用监管 > 投标人
            # 'http://ggzyjy.ahsz.gov.cn/szfront/xycx/018007/': 2,  # 宿州  信用监管 > 专家
            # 'http://ggzyjy.ahsz.gov.cn/szfront/xycx/018008/': 1,  # 宿州  信用监管 > 中介服务机构
            'https://ggzy.chuzhou.gov.cn/Front_jyzx/xycx/044001/': 9,  # 滁州 信用查询 > 违法违规
            'https://ggzy.chuzhou.gov.cn/Front_jyzx/xycx/044005/': 2,  # 滁州 信用查询 > 行政处罚
            'http://ggjfwpt.luan.gov.cn/laztb/xyxx/006001/': 6,  # 六安 曝光台
            'http://ggzyjy.xuancheng.gov.cn/xcspfront/xyxx/007001/moreinfo.html': 6,  # 宣城 曝光台
            'http://ggj.chizhou.gov.cn/chiztpfront/xypt/013005/': 1,  # 池州 曝光台 监管信息
            'http://ggj.chizhou.gov.cn/chiztpfront/xypt/013006/013006001/': 1,  # 池州 曝光台 不良行为
            'http://ggj.chizhou.gov.cn/chiztpfront/xypt/013006/013006002/': 1,  # 池州 曝光台 处罚
            'http://ggzy.bozhou.gov.cn/BZWZ/showinfo/xypt.aspx': 3,  # 毫州 信用平台(曝光台)


        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hefei' in url:
                city = '合肥'
                xpath = "//div[@class='ewb-right-bd']/ul/li"
            elif 'bozhou' in url:
                city = '毫州'
                xpath = "//table[@id='MoreInfoListxypt1_moreinfo']/tbody/tr/td/table/tbody/tr[17]/td/table/tbody/tr/td[2]/a"
            elif 'chizhou' in url:
                city = '池州'
                xpath = "//div[@id='categorypagingcontent']/ul/li/div/a"
            elif 'xuancheng' in url:
                city = '宣城'
                xpath = "//div[@class='ewb-project-info']/div[1]/ul/li"
            elif '.luan' in url:
                city = '六安'
                xpath = "//div[@class='ewb-sub']/ul/li"
            elif 'chuzhou' in url:
                city = '滁州'
                xpath = "//div[@class='right-wrap-ccontent-text']/div[1]/table/tbody/tr/td[2]/a"
            elif 'ahsz' in url:
                city = '宿州'
                xpath = "//div[@class='ewb-list-bd']/div[1]/ul/li"
            elif 'jyzx' in url:
                city = '阜阳'
                xpath = "//div[@class='categorypagingcontent']/div/ul/li/div/a"
            elif 'huangshan' in url:
                city = '黄山'
                xpath = "//div[@class='ewb-right-bd']/ul/li/div/a"
            elif 'bengbu' in url:
                city = '蚌埠'
                xpath = "//td[@class='rightbg']/table/tbody/tr/td[2]/a"
            elif 'huaibei' in url:
                city = '淮北'
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            elif 'ggzyjyzx' in url:
                city = '铜陵'
                xpath = "//table[@class='moreinfocon']/tbody/tr/td[2]/a"
            elif 'huainan' in url:
                city = '淮南'
                xpath = "//div[@class='lanmyList']/ul/li/a"
            else:
                city = '芜湖'
                xpath = "//div[@class='ewb-right']/ul/li/div/a"
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
                    # if 'www.hefei' in url and i%6==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                        if 'hefei' in url:
                            try:
                                href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            except:
                                href=''
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1}/span[3]/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        elif 'bengbu' in url or 'bozhou' in url or  'huaibei' in url or  'ggzyjyzx' in url or  'chuzhou' in url:

                            href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1.replace('2]/a','3]')}//text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        elif 'ahsz' in url or '.luan' in url or 'xuancheng' in url:

                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        elif 'huainan' in url:

                            href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1.replace('/a','/span')}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:

                            href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(xpath1.replace('div/a','')+"/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime.replace('[','').replace(']',''), "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1,pro)
                            else:
                                po += 1
                                break
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    if 'huangshan' in url:
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    elif 'xuancheng' in url :

                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    elif 'ggzyjyzx' in url or 'FuYang' in url or 'ahsz' in url or 'chuzhou' in url or 'bozhou' in url or '.luan' in url or 'chizhou' in url:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                        except:
                                            driver.find_element_by_xpath("//td[contains(string(),'下页')]").click()
                                    elif 'whsggzy' in url:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('>>'))
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))


                            break
    except Exception as e:
        print('安徽\t', e)
        driver.close()
        return anhui(name)

# todo  福建 公共资源中心 (厦门)
def fujian(name):
    try:
        pro = name
        print(f"福建程序已启动，稍等几秒")
        city='厦门'
        # fz_excel(pro, city)  # 复制同款excel表格


        urls = {
            51: 2,  # 公共资源中心 曝光专栏 省级及以上
            52: 2,  # 公共资源中心 曝光专栏 市级
            53: 1,  # 公共资源中心 曝光专栏 其他
        }
        for smallClassId, pages in zip(urls.keys(), urls.values()):
            url = "http://www.xmzyjy.cn/XmUiForWeb2.0/articleNews/getNewsPageList.do"
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Length': '83',
                'Content-Type': 'application/json;charset=UTF-8',
                'Cookie': 'Hm_lvt_b9b3de9840555ca877bfb52b9430f10b=1595386455,1595986747,1596186579,1596435407; Hm_lpvt_b9b3de9840555ca877bfb52b9430f10b=1596435407',
                'Host': 'www.xmzyjy.cn',
                'Origin': 'http://www.xmzyjy.cn',
                'Referer': 'http://www.xmzyjy.cn/XmUiForWeb2.0/xmebid/default.do',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'
            }
            data = {'pageIndex': 1, 'pageSize': 10, 'bigClassId': 12, 'middleClassId': 20, 'smallClassId':smallClassId , 'keyWord': ""}

            con = requests.post(url, headers=headers, json=data).content.decode('utf-8')
            for page in range(1, pages + 1):
                conts = json.loads(con)['data']['dataList']
                for cont in conts:
                    publictime = cont['pubDate']
                    href = cont['newsId']
                    link = f'http://www.xmzyjy.cn/XmUiForWeb2.0/articleNews/newsDetails.do?newsId={href}&bigClassId=12&middleClassId=20'
                    title = cont['newsTitle']
                    select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nrxy(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=link, biaoti=title, tianjiatime=insertDBtime, zt='0')
                            Mysql.update_xw_nrxy(xy=1, prid=uid)
                            print(f'--{city}-【{title}】写入成功')

                        break

    except Exception as e:
        print('福建\t', e)
        driver.close()
        return fujian(name)

# todo  福建   公共资源中心（莆田、龙岩）
def fujian1(name):
    try:
        pro=name
        # city = name
        print(f"安徽程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/bgt/013008/': 1,  # 莆田   交易诚信 > 黑名单
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/bgt/013001/': 1,  # 莆田   交易诚信 > 投标企业通报
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/bgt/013002/': 1,  # 莆田   交易诚信 > 代理机构通报
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/bgt/013003/': 1,  # 莆田   交易诚信 > 专家评委通报
            'http://ggzyjy.xzfwzx.putian.gov.cn/fwzx/bgt/013004/': 1,  # 莆田   交易诚信 > 其他通报
            'https://www.lyggzy.com.cn/lyztb/bgt/': 1,  # 龙岩   曝光台
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'xzfwzx' in url:
                city = '莆田'
                xpath = "//div[@id='right']/ul/li"
            else:
                city = '龙岩'
                xpath = "//div[@class='r-bd']/ul/li"
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
                    # if 'www.hefei' in url and i%6==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '').replace("'", "")
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1,pro)
                            else:
                                po += 1
                                break
                        if i == lengt:
                            if lengt < length - 1:
                                break
                            else:
                                if page != pages:
                                    if 'huangshan' in url:
                                        driver.find_element_by_xpath(f"//ul[@class='m-pagination-page']/li[{page+1}]/a").click()
                                    elif 'xzfwzx' in url:
                                        driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页 >'))
                                    else:
                                        try:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下页>'))
                                        except:
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))

                            break
    except Exception as e:
        print('福建1\t', e)
        driver.close()
        return fujian1(name)

# todo  广东   公共资源中心(阳江、东莞、中山)
def guangdong(name):
    try:
        pro=name
        # city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.yjggzy.cn/Query/ArticleQuery2/eda6cfcc738944fdab0a08e73abebc2d': 1,  # 阳江   诚信体系>企业诚信
            'http://ggzy.dg.gov.cn/ggzy/website/WebPagesManagement/CreditSystem/Exposure/list?KindIndex=-1': 1,  # 东莞   诚信体系>曝光台
            'http://ggzyjy.zs.gov.cn/Application/NewPage/PageSubItem.jsp?node=155': 1,  # 中山   征信体系》不良行为通报
            'http://ggzyjy.zs.gov.cn/Application/NewPage/PageSubItem.jsp?node=176': 4,  # 中山   征信体系》市场主体信用信息
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'yjggzy' in url:
                city = '阳江'
                xpath = "//div[@class='Rbox']/ul/li"

            elif 'zs.gov' in url:
                city = '中山'
                xpath = "//div[@class='nav_list']/ul/li"

            else:
                city = '东莞'
                xpath = "//table[@id='old_data']/tbody/tr/td[2]/a"
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
                    # if 'www.hefei' in url and i%6==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                        if 'dg.gov' in url :

                            href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1.replace('2]/a','4]/span')}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        elif '176' in url :
                            href = html_1.xpath(f"{xpath1}/span[4]/@onclick")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '').replace("window.open('","").replace("')","")
                            title = html_1.xpath(f"{xpath1}/span[1]/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1}/span[3]/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:

                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime.replace('/','-'), "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))

                            break
    except Exception as e:
        print('广东\t', e)
        driver.close()
        return guangdong(name)
# todo  广西   公共资源中心(贵港)
def guangxi(name):
    try:
        pro=name
        # city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggggjy.gxgg.gov.cn:9005/pgt/about.html': 1,  # 贵港  曝光台

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'gxgg' in url:
                city = '贵港'
                xpath = "//div[@class='ewb-con-bd']/ul/li/div/a"

            else:
                city = '东莞'
                xpath = "//table[@id='old_data']/tbody/tr/td[2]/a"
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
                    # if 'www.hefei' in url and i%6==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                        if 'gxgg' in url :

                            href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1.replace('div/a','span')}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:

                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))


                            break
    except Exception as e:
        print('广西\t', e)
        driver.close()
        return guangxi(name)

# todo  贵州   公共资源中心(遵义、安顺、黔东南、黔西南)
def guizhou(name):
    try:
        pro=name
        # city = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.zunyi.gov.cn/blxwjl/': 1,  # 遵义  不良行为记录
            'http://www.ggzy.anshun.gov.cn/cxpt/blxwjl/index.html': 1,  # 安顺  不良行为记录
            'http://ggzyjyzx.qdn.gov.cn/zxxx/cxpt/': 1,  # 黔东南  不良行为记录
            'http://ggzyjy.qxn.gov.cn/cxpt_500593/cxpj/zbcgr/index.html': 3,  # 黔西南  诚信评价 » 招标（采购）人
            'http://ggzyjy.qxn.gov.cn/cxpt_500593/cxpj/zbdljg/': 2,  # 黔西南  诚信评价 » 招标代理机构
            'http://ggzyjy.qxn.gov.cn/cxpt_500593/cxpj/tbr/': 2,  # 黔西南  诚信评价 » 投标人
            'http://ggzyjy.qxn.gov.cn/cxpt_500593/cxpj/pgt_500593/': 1,  # 黔西南  诚信评价 » 曝光台

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            time.sleep(1)
            driver.refresh()
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zunyi' in url:
                city = '遵义'
            elif 'qdn' in url:
                city = '黔东南'
            elif 'qxn' in url:
                city = '黔西南'
            else:
                city = '安顺'
            xpath = "//div[@class='NewsList']/ul/li"
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
                    # if 'www.hefei' in url and i%6==0:
                    #     pass
                    # else:
                        lengt = len(html_1.xpath(xpath))
                        xpath1 = xpath.replace('/li', f'/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                        if 'gxgg' in url :

                            href = html_1.xpath(f"{xpath1}/@href")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                            title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1.replace('div/a','span')}/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')
                        else:

                            href = html_1.xpath(f"{xpath1}/a/@href")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '')
                            title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                                '\r', '').replace("'", "")
                            publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n','').replace('\t','').replace('\r','')

                        select = Mysql.select_xw_nr(biaoti=title)  # 查询标题是否存在

                        if select == None:
                            publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                            # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                            if publictime_times >= jiezhi_time:
                                chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                            driver.execute_script("arguments[0].click();", driver.find_element_by_link_text('下一页'))


                            break
    except Exception as e:
        print('广西\t', e)
        driver.close()
        return guangxi(name)

# todo  黑龙江  公共资源中心(齐齐哈尔、大庆)
def heilongjiang(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzy.qqhr.gov.cn/cxtxpt/about.html': 1,  # 齐齐哈尔 奖惩记录
            'http://ggzyjyzx.daqing.gov.cn/supplier/index.htm': 1,  # 大庆 违约违规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'qqhr' in url:
                city='齐齐哈尔'
                xpath = "//div[@class='ewb-info-bd']/ul/li/div/a"
            else:
                city = '大庆'
                xpath = "//div[@class='con2']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'plaqqhr

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'qqhr' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a//text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('黑龙江\t', e)
        driver.close()
        return heilongjiang(name)


# todo  湖北  公共资源中心(十堰、咸宁、天门、潜江)
def hubei(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.hbcxpt.cn/illegalListZf.shtml?refresh=1&partiesName=': 4,  # 十堰 曝光台
            'http://www.hbcxpt.cn/jjmdList.shtml?refresh=1': 1,  # 十堰 黑名单
            'http://xnztb.xianning.gov.cn/xnweb/wfwgxx/016001/': 1,  # 咸宁  违法违规信息 >> 湖北省违法违规信息发布平台
            'http://xnztb.xianning.gov.cn/xnweb/wfwgxx/016002/': 1,  # 咸宁  违法违规信息 >> 咸宁市违法违规信息发布平台
            'http://ztb.tianmen.gov.cn/news/ztzx/bljl': 1,  # 天门  不良记录
            'http://www.qjggzy.cn/qjztb/gy_news_list.do?newCatid=6': 1,  # 潜江  违法违规
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'hbcxpt' in url:
                city='十堰'
                xpath = "//div[@class='list_info fl']/form/ul/li/a"
            elif 'tianmen' in url:
                city='天门'
                xpath = "//div[@class='newslist']/ul/li/a/span[1]"
            elif 'qjggzy' in url:
                city='潜江'
                xpath = "//div[@class='c1-bline']/div/a/span"
            else:
                city = '咸宁'
                xpath = "//div[@class='s-tt-bd']/div[1]/table/tbody/tr[1]/td[2]/a"
            if 'hbcxpt' in url:
                length = len(html_2.xpath(xpath)) + 3
                ii=3
            else:
                length = len(html_2.xpath(xpath)) + 1
                ii=1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(ii, length):
                  # if 'plaqqhr

                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hbcxpt' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a', "") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    elif 'tianmen' in url:
                        href = html_1.xpath(f"{xpath1.replace('span[1]','')}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('span[1]', "span[2]") + "/text()")[0].strip().replace('/', '-').replace('\n', '').replace('发布时间：', '')
                    elif 'qjggzy' in url:
                        href = html_1.xpath(f"{xpath1.replace('span','')}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a/span', "[2]") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('[2]/a','[3]/font')+f"/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('湖北\t', e)
        driver.close()
        return hubei(name)

# todo  湖南  公共资源中心
def hunan(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        # url = 'https://www.hnsggzy.com/queryContent-bgt.jspx?title=&origin=%E7%9C%81&channelPath=bgt'  # 行政处罚信息
        urls = {
             'https://www.hnsggzy.com/queryContent-bgt.jspx?title=&origin=%E7%9C%81&channelPath=bgt' : 4,  # 湖南省 行政处罚信息
            'https://www.hnsggzy.com/queryContent-bgt.jspx?title=&origin=%E7%9C%81&channelPath=lhcj': 4,  # 湖南省 联合惩戒

        }
        for url, io in zip(urls.keys(), urls.values()):  # 湖南省
          for uu in range(2,17):  # 省、长沙、株洲、湘潭、衡阳、邵阳、岳阳、常德、张家界、益阳、娄底、郴州、永州、怀化、湘西
            driver.get(url)
            driver.find_element_by_xpath(f"//div[@class='jyxxcontent']/ul[1]/li/ul[@id='zone']/li[{uu}]").click()
            driver.find_element_by_xpath(f"//div[@class='content-search']/div[@id='search_btn']").click()
            time.sleep(1)
            con = driver.page_source
            html_2 = etree.HTML(con)
            city=html_2.xpath(f"//div[@class='jyxxcontent']/ul[1]/li/ul[@id='zone']/li[{uu}]/text()")[0]
            xpath = "//div[@class='jyxxcontent']/ul/li/div[@class='article-list3-t']/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            if uu==16:pages=6
            else:pages=1
            for page in range(1, pages+1):
                time.sleep(1)
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title1 = html_1.xpath(f"{xpath1}/text()")
                    title=''.join(title1)
                    publictime = html_1.xpath(xpath1.replace(']/a',']/div')+f"/text()")[0].strip().replace('\n', '').replace('.', '-')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        cc=jiezhi_time
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('湖南\t', e)
        driver.close()
        return hunan(name)
# todo  湖南  公共资源中心(株洲、衡阳、邵阳、岳阳、常德、张家界、益阳、郴州)
def hunan1(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.zzzyjy.cn/006/006002/secondPage.html': 2,  # 株洲 曝光台
            'https://ggzy.hengyang.gov.cn/fwdh/pgt/index.html': 1,  # 衡阳 曝光台
            'https://ggzy.shaoyang.gov.cn/newsList.html?index=9&type=%E8%AF%9A%E4%BF%A1%E4%B8%93%E6%A0%8F&xtype=%E8%AF%9A%E4%BF%A1%E4%B8%93%E6%A0%8F': 1,  # 邵阳 曝光台
            'http://ggzy.yueyang.gov.cn/58094/index.htm': 1,  # 岳阳 曝光台
            'http://ggzy.changde.gov.cn/pgt': 2,  # 常德 曝光台
            'http://www.zjjsggzy.gov.cn/Home/NewsList?index=2&type=%E8%AF%9A%E4%BF%A1%E4%B8%93%E6%A0%8F&xtype=%E6%9B%9D%E5%85%89%E5%8F%B0': 2,  # 张家界 曝光台
            'http://jyzx.yiyang.gov.cn/ggzyjy/31066/31088/index.htm': 1,  # 益阳 曝光台
            'http://czggzy.czs.gov.cn/18360/18365/56569/index.htm': 1,  # 郴州 曝光台

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zzzyjy' in url:
                city='株洲'
                xpath = "//div[@class='ewb-right']/ul/li"
            elif 'czggzy' in url:
                city='郴州'
                xpath = "//div[@class='left_list col-md-9']/ul/li"
            elif 'shaoyang' in url:
                city='邵阳'
                xpath = "//div[@class='xxx-main']/ul/li"
            elif 'yiyang' in url:
                city='益阳'
                xpath = "//div[@class='tllb_rg_con']/ul[1]/li"
            elif 'zjjsggzy' in url:
                city='张家界'
                xpath = "//div[@class='xxx-main']/ul/li"
            elif 'yueyang' in url:
                city='岳阳'
                xpath = "//div[@class='list-right']/ul/li"
            elif 'changde' in url:
                city='常德'
                xpath = "//div[@class='mBd']/ul/li"
            else:
                city = '衡阳'
                xpath = "//div[@class='contentText']/ul/li"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'shaoyang' in url and i==1:
                      pass
                  else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('ul[1]/li', f'ul[1]/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if 'hbcxpt' in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('/a', "") + "/text()")[0].strip().replace('/', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/a/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/a/text()")[0].strip().replace('\n', '').replace('\t','').replace( '\r', '')
                        publictime = html_1.xpath(xpath1+f"/span/text()")[0].strip().replace('\n', '').replace('(', '').replace(')','').replace('[', '').replace(']','').replace('日', '').replace('/', '-')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('湖南\t', e)
        driver.close()
        return hunan1(name)

# todo  内蒙  公共资源中心(内蒙、呼和浩特、通辽、鄂尔多斯、呼伦贝尔)
def neimeng(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.nmg.gov.cn/cxxx/xyxx/wfwgxx': 2,  # 内蒙 违法违规信息
            'http://ggzyjy.nmg.gov.cn/cxxx/xyxx/hmd': 1,  # 内蒙 黑名单
            'http://ggzy.huhhot.gov.cn/hsweb/heimingdan/MoreInfo.aspx?CategoryNum=024': 2,  # 呼和浩特 黑名单
            'http://ggzy.tongliao.gov.cn/tlsggzy/xyxx/023001/about.html': 1,  # 通辽 违法违规信息
            'http://ggzyjy.ordos.gov.cn/TPFront/cxxx/': 1,  # 鄂尔多斯 诚信信息
            'http://www.hlbeggzyjy.org.cn/xypt/005006/subpage.html': 1,  # 呼伦贝尔 违法违规信息
            'http://www.hlbeggzyjy.org.cn/xypt/005003/subpage.html': 1,  # 呼伦贝尔 黑名单信息

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'nmg' in url:
                city='内蒙'
                xpath = "//form[@id='optionConditionForm']/table/tbody/tr/td[2]/a"
            elif 'hlbeggzyjy' in url:
                city='呼伦贝尔'
                xpath = "//div[@class='ewb-right-bd']/ul/li/div/a"
            elif 'tongliao' in url:
                city='通辽'
                xpath = "//div[@class='ewb-con-bd']/ul/li/div/a"
            elif 'ggzyjy' in url:
                city='鄂尔多斯'
                xpath = "//table/tbody/tr[3]/td/div/table/tbody/tr/td/table/tbody/tr/td[2]/a"
            else:
                city = '呼和浩特'
                xpath = "//div[@id='right']/table[2]/tbody/tr/td[2]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'nmg' in url and i==1:
                      pass
                  else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    if 'hmd' in url:
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[4]").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('\n', '')
                    else:
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('\n', '')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下页>'))
                                    except:
                                        driver.execute_script("arguments[0].click();",driver.find_element_by_link_text('下一页'))
                        break
    except Exception as e:
        print('内蒙\t', e)
        driver.close()
        return neimeng(name)

# todo  山东  公共资源中心(淄博、东营、烟台、滨州、济宁、聊城)
def shandong(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.zibo.gov.cn/TPFront/xygl/025002/MoreInfo.aspx?CategoryNum=10754': 1,  # 淄博 曝光台
            'http://ggzy.dongying.gov.cn/dyweb/015/MoreInfo.aspx?CategoryNum=015': 1,  # 东营 曝光台
            'http://ggzyjy.yantai.gov.cn/bgt/index.jhtml': 1,  # 烟台 曝光台
            'http://ggzyjy.yantai.gov.cn/bgthm/index.jhtml': 1,  # 烟台 黑名单
            'http://ggzyjy.binzhou.gov.cn/bzweb/xygl/021001/021001001/MoreInfo.aspx?CategoryNum=021001001': 1,  # 滨州 曝光台
            'http://ggzy.jining.gov.cn/JiNing/Posts?CategoryCode=370800010': 1,  # 济宁 曝光台
            'http://www.lcsggzyjy.cn/lcweb/bgt/': 9,  # 聊城 曝光台

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'zibo' in url:
                city='淄博'
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            elif 'lcsggzyjy' in url:
                city='聊城'
                xpath = "//div[@class='content']/div[1]/table/tbody/tr/td[2]/a"
            elif 'jining' in url:
                city='济宁'
                xpath = "//div[@class='panel-body']/ul/li/a"
            elif 'yantai' in url:
                city='烟台'
                xpath = "//div[@class='article-content']/ul/li/div/a"
            elif 'binzhou' in url:
                city='滨州'
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            else:
                city = '东营'
                xpath = "//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'shaoyang' in url and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    if 'jining' in url:
                        publictime = html_1.xpath(xpath1.replace(']/a', "]/span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')
                    else:
                        publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]").replace('div/a', "div/div") + "//text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
                        else:
                            po += 1
                            break
                    if i == lengt:
                        if lengt < length - 1:
                            break
                        else:
                            if page != pages:
                                xy = "//td[contains(string(),'下页')]"
                                driver.find_element_by_xpath(xy).click()
                        break
    except Exception as e:
        print('山东\t', e)
        driver.close()
        return shandong(name)


# todo  四川  公共资源中心(四川、攀枝花、泸州、眉山、宜宾、巴中、广安、资阳、成都)
def sichuan(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            # 'http://ggzyjy.sc.gov.cn/cxgl/006002/moreinfo.html': 1,  # 四川 曝光台
            # 'http://ggzy.panzhihua.gov.cn/badjilu/badjiluList': 1,  # 攀枝花 曝光台
            # 'https://www.lzsggzy.com/pgt/list.html': 1,  # 泸州 曝光台
            # 'http://www.msggzy.org.cn/front/bgt/': 1,  # 眉山 曝光台
            # 'https://ggzy.yibin.gov.cn/Jyweb/XinXiGongKaiList.aspx?type=%e4%bf%a1%e6%81%af%e5%af%bc%e8%88%aa&subtype=700': 1,  # 宜宾 曝光台
            # 'http://zwhjy.cnbz.gov.cn/pgt/index.html': 1,  # 巴中 曝光台
            # 'http://ggzy.guang-an.gov.cn/gasggzyjyw/bgt/list.shtml': 1,  # 广安 曝光台
            # 'http://ggzyjyzx.ziyang.gov.cn/fuwuzn/fwzn?zcfgType=22&city=': 1,  # 资阳  信用记录 > 不良记录
            'https://www.cdggzy.com/site/OpenGovernment/List.aspx?cid=0001000100020003': 3,  # 成都  信用信息

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy.sc' in url:
                city='四川'
                xpath = "//div[@class='container']/ul/li/a"
            elif 'cdggzy' in url:
                city='成都'
                xpath = "//table[@id='Result']/tbody/tr/td[1]/a"
            elif 'ziyang' in url:
                city='资阳'
                xpath = "//form[@id='zbggForm']/span/table/tbody/tr/td[2]/a"
            elif 'guang-an' in url:
                city='广安'
                xpath = "//div[@class='content']/ul/li/a"
            elif 'cnbz' in url:
                city='巴中'
                xpath = "//div[@class='listnews']/ul/li/a/span"
            elif 'yibin' in url:
                city='宜宾'
                xpath = '//*[@id="ctl00_Content_GridView1"]/tbody/tr/td[2]/a'
            elif 'msggzy' in url:
                city='眉山'
                xpath = "//div[@class='ewb-comp-bd']/div[1]/table/tbody/tr/td[1]/a"
            elif 'lzsggzy' in url:
                city='泸州'
                xpath = "//div[@id='main']/div[1]/ul/li/a"
            else:
                city = '攀枝花'
                xpath = "//table[@id='p2']/tbody/tr/td[2]/a"
            if 'zwhjy' in xpath:
                length = len(html_2.xpath(xpath)) + 2
            else:
                length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'd[2]/a' in xpath and i==1:
                      pass
                  elif 'cnbz' in url and i==6:
                      pass
                  else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                    if 'cnbz' in url:
                        href = html_1.xpath(f"{xpath1.replace('/span','')}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                            '\r', '')
                        publictime = html_1.xpath(xpath1.replace('a/span', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')
                    else:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        if 'lzsggzy' in url:
                            title = html_1.xpath(f"{xpath1}/text()")[1].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        else:
                            title = html_1.xpath(f"{xpath1}//text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if 'ggzyjy.sc' in url or 'lzsggzy' in url or 'guang-an' in url:
                            publictime = html_1.xpath( xpath1.replace( ']/a', "]/span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace( '.', '-').replace('\n', '')
                        else:
                            publictime = html_1.xpath( xpath1.replace('[2]/a', "[3]").replace('[1]/a', "[2]").replace('div/a', "div/div")+ "/text()")[0].strip().replace('[', '').replace(']', '').replace( '.', '-').replace('\n', '')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('四川\t', e)
        driver.close()
        return sichuan(name)

# todo  辽宁  公共资源中心(大连、锦州、葫芦岛)
def liaoning(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://ggzyjy.dl.gov.cn/TPFront/xyzl/096002/': 1,  # 大连 信用专栏> 代理机构
            'http://ggzyjy.dl.gov.cn/TPFront/xyzl/096006/': 1,  # 大连 信用专栏> 投标企业
            'http://ggzy.jz.gov.cn/jycx/006001/moreinfo.html': 1,  # 锦州 信用专栏> 投标企业
            'http://www.hldggzyjyzx.com.cn/pgt/thirdpage.html': 1,  # 葫芦岛 信用专栏> 投标企业

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy.dl' in url:
                city='辽宁'
                xpath = "//div[@class='categorypagingcontent']/ul/li/div/a"
            elif 'hldggzyjyzx' in url:
                city='葫芦岛'
                xpath = "//div[@class='ewb-info-bd']/ul/li/div/a"
            else:
                city = '锦州'
                xpath = "//div[@class='ewb-colu-bd ewb-container-min ']/ul/li/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'd[2]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')


                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    publictime = html_1.xpath(xpath1.replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace(
                        '.', '-').replace('\n', '')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('四川\t', e)
        driver.close()
        return sichuan(name)

# todo  吉林  公共资源中心(吉林、辽源、松原)
def jilin(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.ggzyzx.jl.gov.cn/pgt/': 1,  # 吉林 曝光台
            'http://ggzy.liaoyuan.gov.cn/cxxx/004001/secondPage.html': 1,  # 辽源 曝光台
            'http://syggzy.jlsy.gov.cn/pgt/list.html': 1,  # 松原 曝光台
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'ggzyjy.jl' in url:
                city='吉林'
                xpath = "//div[@class='list']/ul/li/a"
            elif 'syggzy' in url:
                city='松原'
                xpath = "//div[@class='ewb-right-info']/div[2]/ul/li/a"
            else:
                city = '辽源'
                xpath = "//div[@class='ewb-right ewb-box']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if 'd[2]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')


                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    if 'ggzyjy.jl' in url:
                        publictime = html_1.xpath(xpath1.replace('li/a', "li/div") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')
                    else:
                        publictime = html_1.xpath(xpath1.replace('li/a', "li/span").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace(
                        '.', '-').replace('\n', '')

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('四川\t', e)
        driver.close()
        return sichuan(name)

# todo  宁夏  公共资源中心(宁夏、银川、固原)
def ningxia(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.nxggzyjy.org/ningxiaweb/006/006002/about.html': 1,  # 宁夏 曝光台
            'http://www.ycsggzy.cn/morelink.html?type=95&index=2': 1,  # 银川 曝光台
            'http://www.gysggzyjy.cn/gysggzyjy/016/list.html': 2,  # 固原 曝光台
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'nxggzyjy' in url:
                city='宁夏'
                xpath = "//ul[@id='showList']/ul/li/div/a"
            elif 'ycsggzy' in url:
                city='银川'
                xpath = "//div[@id='showline_div']/ul/li/a"
            else:
                city = '固原'
                xpath = "//table[@id='GV1']/tbody/tr/td[1]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if '[1]/a' in xpath and i==1:
                      pass
                  else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                    if 'nxggzyjy' in url:
                        href = 'http://www.nxggzyjy.org/ningxiaweb/006/006002'+html_1.xpath(f"{xpath1}/@href")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    if 'ycsggzy' in url:
                        publictime = html_1.xpath(xpath1+ "/span/text()")[0].strip().replace('[', '').replace(']', '').replace('/', '-').replace('\n', '')
                    else:
                        publictime = html_1.xpath(xpath1.replace('[1]/a', "[2]").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace( '.', '-').replace('\n', '')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('宁夏 \t', e)
        driver.close()
        return ningxia(name)

# todo   江苏 公共资源中心(江苏、连云港、淮安、盐城、镇江、宿迁)
def jiangsu(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://jsggzy.jszwfw.gov.cn/xyxx/creditInfo.html': 1,  # 江苏 信用信息
            'http://spzx.lyg.gov.cn/lygweb/xyxxn/secondPage.html': 1,  # 连云港 信用信息
            'http://www.hasggzy.com/EpointWeb/ShowInfo/ShowSearchInfo.aspx?CategoryNum=035': 1,  # 淮安 信用信息
            'http://www.ycsggzy.com/026/026001/superviseInfo2.html': 1,  # 盐城 曝光台
            'http://ggzy.zhenjiang.gov.cn/050/second-page.html': 1,  # 镇江 曝光台
            'http://ggzy.sqzwfw.gov.cn/xyxx/secondPage.html': 3,  # 宿迁 信用信息
        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'jsggzy' in url:
                city='江苏'
                xpath = "//tbody[@class='wb-data-item']/tr/td[@class='ewb-trade-td'][1]/a"
            elif 'sqzwfw' in url:
                city='宿迁'
                xpath = "//tbody[@id='showList']/tr/td[@class='ewb-trade-td'][1]/a"
            elif 'ycsggzy' in url:
                city='盐城'
                xpath = "//tbody[@class='wb-data-item']/tr/td[@class='ewb-trade-td'][1]/a"
            elif 'zhenjiang' in url:
                city='镇江'
                xpath = "//tbody[@class='wb-data-item']/tr/td[@class='ewb-trade-td'][1]/a"
            elif 'lyg' in url:
                city='连云港'
                xpath = "//tbody[@id='showList']/tr/td[@class='ewb-trade-td'][1]/a"
            else:
                city = '淮安'
                xpath = "//tbody[@id='infolist']/tr/td[@class='ewb-trade-td'][1]/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if '[1]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')


                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    publictime = html_1.xpath(xpath1.replace('[1]/a', "[2]").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('江苏 \t', e)
        driver.close()
        return jiangsu(name)
# todo   江苏 公共资源中心(南京)
def jiangsu1(name):
    global driver
    try:
        pro = name
        city='南京'
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        url="http://njggzy.nanjing.gov.cn/njweb/pgt/expose.html#"
        driver.get(url)
        urls = {
            "//div[@class='ewb-comp-hd clearfix']/span[1]/a": 2,  # 南京 放弃中标行为
            "//div[@class='ewb-comp-hd clearfix']/span[2]/a": 10,  # 南京 违法违规红黄牌警示信息
            "//div[@class='ewb-comp-hd clearfix']/span[3]/a": 2,  # 南京 货物不良行为及处罚公示
        }
        for xx, pages in zip(urls.keys(), urls.values()):
            driver.find_element_by_xpath(xx).click()
            time.sleep(1)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'span[1]' in xx:
                xpath = "//div[@class='ewb-comp-bd']/div[3]/ul/li/div/h2"
            elif 'span[2]' in xx:
               xpath = "//div[@class='ewb-comp-bd']/div[4]/ul/li/div/h2"
            else:
               xpath = "//div[@class='ewb-comp-bd']/div[5]/ul/li/div/h2"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if '[1]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]')
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    if 'span[3]' in xx:
                        publictime = html_1.xpath(xpath1.replace('/h2', "/p/span") + "/text()")[1].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')[:10]
                    else:
                        publictime = html_1.xpath(xpath1.replace('/h2', "/p/span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace(
                        '.', '-').replace('\n', '')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            insertDBtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                            uid = uuid.uuid4()
                            Mysql.insert_xw_nrxy(prid=uid, shengfen=pro, dijishi=city, fabutime=publictime, url=url,
                                                 biaoti=title, tianjiatime=insertDBtime, zt='0')
                            Mysql.update_xw_nrxy(xy=1, prid=uid)
                            print(f'--{city}-【{title}】写入成功')
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
        print('江苏 \t', e)
        driver.close()
        return jiangsu(name)

# todo   青海 公共资源中心(青海、海东、西宁、海北州、海南州、黄南州、格尔木市)
def qinghai(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'https://www.qhggzyjy.gov.cn/ggzy/cxgk/002002/moreinfo.html': 10,  # 青海 信用信息
            'http://www.qhggzyjy.gov.cn/haid/xwzx/006003/moreinfo.html': 10,  # 海东 通报曝光
            'http://www.qhggzyjy.gov.cn/xin/xwzx/006003/moreinfo.html': 1,  # 西宁 通报曝光
            'http://www.qhggzyjy.gov.cn/haib/xwzx/006003/moreinfo.html': 1,  # 海北州 通报曝光
            'http://www.qhggzyjy.gov.cn/hain/xwzx/006003/moreinfo.html': 3,  # 海南州 通报曝光
            'http://www.qhggzyjy.gov.cn/huangn/xwzx/006003/moreinfo.html': 1,  # 黄南州 通报曝光
            'http://www.qhggzyjy.gov.cn/geem/xwzx/006003/moreinfo.html': 3,  # 格尔木市 通报曝光

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if '/ggzy/' in url:
                city='青海'
            elif '/geem/' in url:
                city='格尔木市'
            elif '/huangn/' in url:
                city='黄南州'
            elif '/hain/' in url:
                city='海南州'
            elif '/xin/' in url:
                city='西宁'
            elif '/haib/' in url:
                city='海北州'
            else:
                city = '海东'
            xpath = "//div[@class='ewb-sty-bd']/ul/li/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if '[1]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')


                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    publictime = html_1.xpath(xpath1.replace('[1]/a', "[2]").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('江苏 \t', e)
        driver.close()
        return jiangsu(name)

# todo   甘肃 公共资源中心(兰州、张掖)
def gansu(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://lzggzyjy.lanzhou.gov.cn/cxgk/004002/moreinfo.html': 1,  # 兰州 诚信公开
            'http://117.78.26.203:8080/xypt/004003/normalSecpage.html': 1,  # 张掖 诚信公开

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if 'xypt' in url:
                city='张掖'
                xpath = "//div[@id='main']/ul/li/div/a"
            else:
                city = '兰州'
                xpath = "//div[@id='jt']/ul/li/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if '[1]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')

                    if 'http://117.78.26.203:8080' in url:
                        href ='http://117.78.26.203:8080'+ html_1.xpath(f"{xpath1}/@href")[0].strip()
                    else:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace(
                        '\r', '')
                    publictime = html_1.xpath(xpath1.replace('[1]/a', "[2]").replace('div/a', "span") + "/text()")[0].strip().replace('[', '').replace(']', '').replace('.', '-').replace('\n', '')[:10]

                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('甘肃 \t', e)
        driver.close()
        return gansu(name)

# todo   河北 公共资源中心(石家庄)
def hebei(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            'http://www.sjzsggzyjyzx.org.cn/bgt/index.jhtml': 1,  # 石家庄 曝光台

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            city='石家庄'
            xpath = "//ul[@class='jcbg-ul']/ul/li/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  # if '[1]/a' in xpath and i==1:
                  #     pass
                  # else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')


                    href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                    title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                    publictime = html_1.xpath(xpath1.replace('i/a', "i/div") + "/text()")[0].strip().replace('.', '-').replace('\n', '')[:10]


                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime, "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('河北 \t', e)
        driver.close()
        return hebei(name)

# todo   河南 公共资源中心(河南 、济源、开封 、安阳、焦作 、濮阳、漯河、驻马店)
def henan(name):
    global driver
    try:
        pro = name
        print(f"{name}程序已启动，稍等几秒")
        # fz_excel(pro, city)  # 复制同款excel表格
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_experimental_option('w3c', False)
        chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
        chromeOptions.add_argument('--headless')  # 隐藏浏览器
        driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        driver.maximize_window()
        urls = {
            # 'http://www.hnggzy.com/hnsggzy/bgt/': 1,  # 河南 曝光台
            # 'http://ggzyjy.jiyuan.gov.cn/TPFront/lhjc/004004/': 1,  # 济源 联合奖惩 > 行政处罚决定
            # 'http://www.kfsggzyjyw.cn/xyptbgt/index.jhtml': 1,  # 开封 曝光台
            'http://www.ayggzy.cn/fuwuzn/fwzn?zcfgType=22': 1,  # 安阳 监督曝光
            'http://www.jzggzy.cn/TPFront/ztbzx/069011/MoreInfo.aspx?CategoryNum=69011': 1,  # 焦作 曝光台
            'http://www.pyggzy.com/list.asp?class=41': 1,  # 濮阳 曝光台
            'https://www.lhjs.cn/News/hmd': 1,  # 漯河 黑名单
            'http://www.zmdggzy.gov.cn/TPFront/bgt/': 1,  # 驻马店 黑名单

        }
        for url, pages in zip(urls.keys(), urls.values()):
            driver.get(url)
            con = driver.page_source
            html_2 = etree.HTML(con)
            if "kfsggzyjyw" in url:
                city='开封'
                xpath="//div[@class='infolist-main']/ul/li/a"
            elif "zmdggzy" in url:
                city='驻马店'
                xpath="//div[@class='categorypagingcontent']/div[1]/ul/li/div/a"
            elif "lhjs" in url:
                city='漯河'
                xpath="//div[@class='filter-content']/ul/li/a/span/span[1]"
            elif "pyggzy" in url:
                city='濮阳'
                xpath="//div[@class='lm_c']/table[1]/tbody/tr/td/table/tbody/tr/td[@class='aspFont1'][1]/a"
            elif "jzggzy" in url:
                city='焦作'
                xpath="//table[@id='MoreInfoList1_DataGrid1']/tbody/tr/td[2]/a"
            elif "ayggzy" in url:
                city='安阳'
                xpath="//table[@id='p2']/tbody/tr/td[2]/a"
            elif "hnggzy" in url:
                city='河南'
                xpath="//table[@class='divlxyz']/tbody/tr/td[2]/a"
            else:
                city='济源'
                xpath = "//div[@class='categorypagingcontent']/ul/li/div/a"
            length = len(html_2.xpath(xpath)) + 1
            po = 0
            for page in range(1, pages+1):
                con = driver.page_source
                html_1 = etree.HTML(con)
                if po > 0:
                    break
                for i in range(1, length):
                  if 'ayggzy' in url and i==1:
                      pass
                  else:
                    lengt = len(html_1.xpath(xpath))
                    xpath1 = xpath.replace('ul/li', f'ul/li[{i}]').replace('tr/td[', f'tr[{i}]/td[')
                    if "kfsggzyjyw" in url:
                        href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/span/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1 + "/em/text()")[ 0].strip().replace('.', '-').replace('[', '').replace(']', '').replace('\n', '')[:10]
                    elif "lhjs" in url:
                        href = html_1.xpath(f"{xpath1.replace('span/span[1]','')}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        publictime = html_1.xpath(xpath1.replace('span[1]','span[2]') + "/text()")[ 0].strip().replace('发布时间：', '').replace('.', '-').replace('[', '').replace(']', '').replace('\n', '')[:10]
                    else:
                        if 'pyggzy' in url:
                            href = 'http://www.pyggzy.com/'+html_1.xpath(f"{xpath1}/@href")[0].strip()
                        else:
                            href = html_1.xpath(f"{xpath1}/@href")[0].strip()
                        title = html_1.xpath(f"{xpath1}/text()")[0].strip().replace('\n', '').replace('\t', '').replace( '\r', '')
                        if "hnggzy" in url:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]/font") + "/text()")[0].strip().replace('.', '-').replace('[', '').replace(']', '').replace('\n', '')[:10]
                        elif "pyggzy" in url:
                            publictime = html_1.xpath(xpath1.replace("td[@class='aspFont1'][1]/a", "td[3]") + "/text()")[0].strip().replace('/', '-').replace('[  ', '').replace(']', '').replace('\n', '')[:10]
                        else:
                            publictime = html_1.xpath(xpath1.replace('[2]/a', "[3]").replace('div/a', "span") + "/text()")[0].strip().replace('.', '-').replace('[', '').replace(']', '').replace('\n', '')[:10]


                    select = Mysql.select_xw_nr1(biaoti=title, dijishi=city)  # 查询标题是否存在

                    if select == None:
                        publictime_times = int(time.mktime(time.strptime(publictime.replace('/', '-'), "%Y-%m-%d")))
                        # jiezhi_time = int(time.mktime(time.strptime('2018-01-01', "%Y-%m-%d")))
                        if publictime_times >= jiezhi_time:
                            chuli(publictime, href, driver, url, title, city,xpath1,pro)
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
        print('河南 \t', e)
        driver.close()
        return henan(name)


# anhui('安徽')
# fujian('福建')
# fujian1('福建')
# guangdong('广东')
# guangxi('广西')
# guizhou('贵州')
# heilongjiang('黑龙江')
# hubei('湖北')
hunan('湖南')
hunan1('湖南')
neimeng('内蒙')
shandong('山东')
sichuan('四川')
liaoning('辽宁')
jilin('吉林')
ningxia('宁夏')
jiangsu('江苏')
jiangsu1('江苏')
qinghai('青海')
gansu('甘肃')
hebei('河北')
henan('河南')