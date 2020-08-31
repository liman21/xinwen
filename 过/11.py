import time,html,uuid
from dao import Mysql
import requests,json,random,re
from lxml import etree
from selenium import webdriver
from datetime import datetime

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

def ganzhou():
    try:
        url1s=[
            # 'http://www.ganzhou.gov.cn/c100022/list.shtml',  # 政务动态
            # 'http://www.ganzhou.gov.cn/c100023/list.shtml',  # 通知公告
            # 'http://www.ganzhou.gov.cn/c100024/list_bmqx.shtml',  # 部门动态
            # 'http://www.ganzhou.gov.cn/c100025/list_bmqx.shtml',  # 区县动态
            'http://www.ganzhou.gov.cn/c100026/list.shtml',  # 便民提示
            'http://www.ganzhou.gov.cn/c100027/list.shtml',  # 央网推荐
            'http://www.ganzhou.gov.cn/c100028/list.shtml',  # 省网推荐
            'http://www.ganzhou.gov.cn/c100029/list.shtml',  # 市外媒体
            'http://www.ganzhou.gov.cn/c100030/list.shtml',  # 新闻发布会
            'http://www.ganzhou.gov.cn/c100032/list.shtml',  # 专题专栏
        ]
        for url1 in url1s:
            print("程序已启动，稍等几秒")
            for page in range(1,37):
                if page==1:
                    tt = requests.get(url1,proxies=ipmax()).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
                else:
                    url2=url1.replace('list.shtml',f'list_{page}.shtml').replace('bmqx.shtml',f'bmqx_{page}.shtml')
                    tt = requests.get(url2).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t',
                                                                                                            '')
                contents1 = re.findall('<div class="bd">(.*?)text/javascript', tt)
                contents = [
                    re.findall('<li><a href="(.*?)" target="_blank" title=\'(.*?)\'  >(.*?)</a><span>(.*?)</span>',contents1[0]),
                    re.findall('<li><a href="(.*?)">(.*?)</a><span>(.*?)</span>',contents1[0]),
                ]
                for content11 in contents:
                    if len(content11)>0:
                        for con in range(len(content11)):
                            content=content11[con]
                            if re.findall('mp.weixin',content[0]):
                                linkurl=content[0]
                                # detail_res = requests.get(linkurl).content.decode('utf-8')
                                # Html = etree.HTML(detail_res)
                                # div = Html.xpath("//div[@id='page-content']")[0]
                                # infocontent = html.unescape(etree.tostring(div, method='html').decode()).replace("'", " ").replace( '"', ' ')
                            else:
                                linkurl = 'http://www.ganzhou.gov.cn' + content[0]
                                # detail_res = requests.get(linkurl).content.decode('utf-8')
                                # Html = etree.HTML(detail_res)
                                # div = Html.xpath('/html/body/div[4]')[0]
                                # infocontent = html.unescape(etree.tostring(div, method='html').decode()).replace("'", " ").replace('"',
                                #                                                                                                ' ')
                            title = content[1]
                            try:
                                publicTime = content[3]
                            except:
                                publicTime = content[2]
                            s = publicTime.replace('/', '-')
                            t = int(datetime.strptime(s, '%Y-%m-%d').timestamp())
                            if t >= 1570896000:
                                select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                                if len(select) == 0:
                                    uid = uuid.uuid4()
                                    Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='360000', regionName='江西省', areaRegion='赣州市',
                                                                publicTime=publicTime, linkurl=linkurl, title=title,
                                                                dataResource='', yewuType='人民政府', infoType='', infoState='', isok='',
                                                                isdeal='')
                                    Mysql.insert_xinwen_detailinfo(uid=uid, infocontent='')
                                    print(f'标题【{title}】写入成功')

                                else:
                                    print(f'标题【{title}】存在')
                print('-' * 50 + f'赣州市第{page}页已完成' + '-' * 50)

    #         chromeOptions = webdriver.ChromeOptions()
    #         chromeOptions.add_experimental_option('w3c', False)
    #         chromeOptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    #         chromeOptions.add_argument('--headless')  # 隐藏浏览器
    #         # chromeOptions.add_argument(f'--proxy-server={ipmax()}')
    #         driver = webdriver.Chrome(options=chromeOptions,  executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    #         driver.get(url=url1)
    #         aoo_11 = driver.page_source  # html
    #         pages=re.findall('总共(\d+)页',aoo_11)
    #         print(f'共{pages[0]}页')
    #         for aa in range(1, int(pages[0])):
    #             if driver.find_element_by_xpath("//td[@class='font_hei12']/input[@id='CP']"):
    #                 driver.find_element_by_xpath("//td[@class='font_hei12']/input[@id='CP']").clear()  # 清除文本框内容
    #             else:
    #                 driver.find_element_by_xpath("//input[@id='ctl00$ContentPlaceHolder1$AspNetPager1_input']").clear()  # 清除文本框内容
    #             driver.find_element_by_xpath("//tr[3]/td[@class='font_hei12']/input[@id='CP']").send_keys(aa)  # 搜索框输入内容
    #             driver.find_element_by_xpath("//tr[3]/td[@class='font_hei12']/input[2]").click()  # 点击一下按钮
    #
    #             aoo_1 = driver.page_source  # html
    #             html_1 = etree.HTML(aoo_1)
    #             list_num = html_1.xpath(f"//table/tbody/tr[1]/td[@class='font_hei14']/a")  # 详情url
    #             for i in range(1, len(list_num)+1):  # 一页20条数据
    #                 qufen ='人民政府'+html_1.xpath(f"/html/body/table[3]/tbody/tr/td[3]/table/tbody/tr[1]/td/a[4]/text()")[0].strip()  # 区分
    #                 link = html_1.xpath(f"//table[{i}]/tbody/tr[1]/td[@class='font_hei14']/a/@href")[0].strip()  # 详情url
    #                 title = html_1.xpath(f"//table[{i}]/tbody/tr[1]/td[@class='font_hei14']/a/text()")[0].strip()  # 标题
    #                 publicTime = html_1.xpath(f"//tr[2]/td[@class='borderhui']/table[{i}]/tbody/tr[1]/td[@class='font_hui12']/text()")[0].strip().replace('\n','') .replace('[','') .replace(']','') .replace('                ','')  # 时间
    #                 s = publicTime.replace('/', '-')
    #                 t = int(datetime.strptime(s, '%Y-%m-%d').timestamp())
    #                 if t >= 1570896000:
    #
    #                     if re.findall('xinhuan',link):
    #                         linkurl=link
    #                     else:
    #                         linkurl = url1 + link[1:]  # url
    #                     driver.find_element_by_xpath(f"//table[{i}]/tbody/tr[1]/td[@class='font_hei14']/a").click()
    #                     driver.switch_to.window(driver.window_handles[-1])
    #                     detail_res=driver.page_source
    #                     Html = etree.HTML(detail_res)
    #                     if Html.xpath("//table[3]/tbody/tr/td[@class='font_hui12']"):
    #                         div1 = Html.xpath("//table[3]/tbody/tr/td[@class='font_hui12']")[0]  # 当前栏目
    #                         div2 = Html.xpath("//table[@class='borderhui']/tbody/tr/td")[0]       # text
    #                     elif Html.xpath("//div/div/div[@class='news-position']"):
    #                         div1 = Html.xpath("//div/div/div[@class='news-position']")[0]  # 当前栏目
    #                         div2 = Html.xpath("//div/div/div[@id='p-detail']")[0]  # text
    #                     elif Html.xpath("//div[@class='padd']/div[@class='BreadcrumbNav']"):
    #                         div1 = Html.xpath("//div[@class='padd']/div[@class='BreadcrumbNav']")[0]  # 当前栏目
    #                         div2 = Html.xpath("//div[@class='article oneColumn pub_border']")[0]  # text
    #                     else:
    #                         div1 = Html.xpath("//div[@class='xl-main']/div[@class='container']")[0]  # 当前栏目
    #                         div2 = '' # text
    #                     try:
    #                         infocontent1 = html.unescape(etree.tostring(div1, method='html').decode()).replace("'", " ").replace(
    #                             '"', ' ')  # html
    #                         infocontent2 = html.unescape(etree.tostring(div2, method='html').decode()).replace("'", " ").replace(
    #                                             '"', ' ')  # html
    #                         infocontent=infocontent1+infocontent2
    #                     except:
    #                         infocontent1 = html.unescape(etree.tostring(div1, method='html').decode()).replace("'",  " ").replace( '"', ' ')  # html
    #                         infocontent=infocontent1
    #                     if re.findall('src="(.*?)" oldsrc=',infocontent):
    #                         infocontent=infocontent.replace('src=.\./',url1+link[1:7]+'/')
    #                     else:infocontent=infocontent
    #                     select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
    #                     if len(select)==0:
    #                         uid = uuid.uuid4()
    #                         Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='360000', regionName='江西省', areaRegion='萍乡市',
    #                                             publicTime=publicTime, linkurl=linkurl, title=title,
    #                                             dataResource='', yewuType='人民政府', infoType='', infoState='', isok='',
    #                                             isdeal='')
    #                         Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
    #                         print(f'标题【{title}】写入成功')
    #
    #                     else:
    #                         print(f'标题【{title}】存在')
    #                     driver.back()  # 返回上一页
    #                     time.sleep(1)
    #             print('-' * 50 + f'萍乡第{aa}页已完成' + '-' * 50)
    except Exception as e:
        print('蚌埠\t', e)
        return ganzhou()
ganzhou()