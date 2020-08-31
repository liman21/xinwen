import time,html,uuid
from dao import Mysql
import requests,json,random,re
from lxml import etree

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

# 河北省新闻
def shengyw():
    url='http://www.hebei.gov.cn/hebei/13863674/13871225/index.html'
    tt = requests.get(url).content.decode('utf-8')
    pages = re.findall('totalpage="(\d+)"', tt)[0]
    for page in range(1, int(pages) + 1):
        url1=f'http://www.hebei.gov.cn/eportal/ui?pageId=13871225&currentPage={page}'
        tt = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
        contents = re.findall('<a href="(.*?)" onclick="void\(0\)" target="_blank" title="(.*?)" istitle="true">(.*?)</a> <span class="date" style="font-size: 12px;color: #898989;padding-left: 5px;">(.*?)</span> </li>', tt)
        for content in contents:
            linkurl = 'http://www.hebei.gov.cn' + content[0]
            detail_res = requests.get(linkurl).content.decode('utf-8')
            Html = etree.HTML(detail_res)
            div = Html.xpath('//*[@id="fadd83fc626241d9937b20353ca675eb"]/div[2]')[0]
            infocontent = html.unescape(etree.tostring(div, method='html').decode()).replace("'", " ").replace('"', ' ')
            title = content[1]
            publicTime = content[3]
            select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
            if len(select)==0:
                uid = uuid.uuid4()
                Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='050000-075000', regionName='河北省', areaRegion='河北省',
                                             publicTime=publicTime, linkurl=linkurl, title=title,
                                             dataResource='', yewuType='', infoType='', infoState='', isok='',
                                             isdeal='')
                Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
            else:
                print('标题存在')
def shijiazhuang():
    url1s=[
        # 'http://www.sjz.gov.cn/column.jsp?id=1490076462404',  # 市政要闻
        'http://www.sjz.gov.cn/column.jsp?id=1490076534390',    # 部门动态
        'http://www.sjz.gov.cn/column.jsp?id=1490076571666',    # 区县动态
    ]
    for url1 in url1s:
        tt=requests.get(url1).content.decode('gb2312')
        pages = re.findall("title='每页显示.*记录'>共.*条(\d+)页", tt)[0]
        for page in range(1,int(pages)+1):
            url=f'{url1}&current={page}'
            contents1 = requests.get(url1).content.decode('gb2312').replace('\n', '').replace('\r', '').replace('\t', '')
            contents2=re.findall('1 list_2"><ul>(.*?)/ul></div></div><div style="text-align:',contents1)
            contents=re.findall('href="(.*?)" target="_blank"  style="line-height:30px;" title="(.*?)">(.*?)</a>&nbsp;<span class="date" style="color:#898989">(.*?)</span>',contents2[0])
            for content in contents:
                linkurl='http://www.sjz.gov.cn'+content[0]
                detail_res=requests.get(linkurl).content.decode('gb2312')
                Html = etree.HTML(detail_res)
                div = Html.xpath("/html/body/div/div[2]")[0]
                infocontent = html.unescape(etree.tostring(div, method='html').decode()).replace("'", " ").replace('"', ' ')
                title=content[1]
                publicTime=content[3]
                select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                if select == None:
                    uid = uuid.uuid4()
                    Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='050000', regionName='河北省', areaRegion='石家庄市',
                                        publicTime=publicTime, linkurl=linkurl, title=title,
                                        dataResource='', yewuType='', infoType='', infoState='', isok='',
                                        isdeal='')
                    Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                else:
                    print('标题存在')
                print('gg')
def chengde():
    for page in range(1,374):
        url1s = [
            f'http://www.chengde.gov.cn/col/col360/index.html?uid=1412&pageNum={page}',  # 本市要闻  1361
            # 'http://www.chengde.gov.cn/col/col361/index.html?uid=1412&pageNum={page}',    # 外媒看承德  367
            # 'http://www.chengde.gov.cn/col/col362/index.html?uid=1412&pageNum={page}',    # 外媒看承德  374
            # 'http://www.chengde.gov.cn/col/col364/index.html?uid=1412&pageNum={page}',    # 公示公告    27
        ]
        for url1 in url1s:
            contents1 = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
            contents=re.findall('pan><a (.*?)</span>',contents1)
            for content in contents:
                co=re.findall("href=\\'(.*?)\\'title=\\'(.*?)\\'target",content)[0]
                co1=re.findall('target="_blank">(.*?)</a><span class="bt-data-time"style="font-size:14px;">\[(.*?)\]',content)[0]

                linkurl='http://www.chengde.gov.cn'+co[0]
                detail_res=requests.get(linkurl).content.decode('utf-8')
                Html = etree.HTML(detail_res)
                # div = Html.xpath("/html/body/div/div[2]")[0]
                infocontent = html.unescape(etree.tostring(Html, method='html').decode()).replace("'", " ").replace('"', ' ')
                title=co[1]
                publicTime=co1[1]
                select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                if select == None:
                    uid = uuid.uuid4()
                    Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='067000', regionName='河北省', areaRegion='承德市',
                                        publicTime=publicTime, linkurl=linkurl, title=title,
                                        dataResource='', yewuType='', infoType='', infoState='', isok='',
                                        isdeal='')
                    Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                else:
                    print('标题存在')
def zhangjiakou():
    try:
        for page in range(1,374):
            url1s = [
                 f'http://www.zjk.gov.cn/syscolumn/dt/zjkyw/index.html',  # 张家口要闻
                 f'http://www.zjk.gov.cn/syscolumn/dt/zjkyw/index_{page}.html',  # 张家口要闻
                 f'http://www.zjk.gov.cn/bmgz_frame1.jsp?pages={page}',    # 部门工作
            ]
            for url1 in url1s:
                contents1 = requests.get(url1,proxies=ipmax()).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
                contents=[
                    re.findall('"hg" href="(.*?)" target="_blank" title="(.*?)">(.*?)</a></td>                    <td width="80" class="cdate">\[(.*?)\]</td>',contents1),
                    re.findall('hg" href="(.*?)" title="(.*?)" target="_blank">(.*?)</a></td>              <td width="100" class="cdate">\[(.*?)\]</td>',contents1),
                ]
                for content in contents:
                    if len(content)>0:
                        content=content[0]
                        uu=re.findall('www.(.*?).gov',url1)[0]
                        linkurl=f'http://www.{uu}.gov.cn'+content[0].strip()
                        detail_res=requests.get(linkurl).content.decode('utf-8')
                        Html = etree.HTML(detail_res)
                        infocontent = html.unescape(etree.tostring(Html, method='html').decode()).replace("'", " ").replace('"', ' ')
                        title=content[1].strip()
                        publicTime=content[3].strip()
                        select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='067000', regionName='河北省', areaRegion='承德市',
                                                publicTime=publicTime, linkurl=linkurl, title=title,
                                                dataResource='', yewuType='', infoType='', infoState='', isok='',
                                                isdeal='')
                            Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                        else:
                            print('标题存在')
    except Exception as e:
        print('蚌埠\t', e)
        return zhangjiakou()
def qinhuangdao():
    try:
        url1s = [
             # f'http://www.qhd.gov.cn/front_pcsec.do?tid=A44A512C86E7FA51FEB2B9B098047A46&p=1',  # 本地动态
             # f'http://www.qhd.gov.cn/front_pcsec.do?tid=BE16A305B662511F9C82516BD16F3C24&p=1',  # 部门动态
             f'http://www.qhd.gov.cn/front_pcsec.do?tid=677638128C3E53D4C629F745917A4CD8&p=1',  # 县区动态
        ]
        for url1 in url1s:
            contents1 = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
            pages = int(re.findall('共(\d+)页',contents1)[0])
            for page in range(1, pages+1):
                url=url1.replace('p=1',f'p={page}')
                contents2 = requests.get(url).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')

                contents=[
                    re.findall('fl"><a href="(.*?)" target="_blank">(.*?)</a></div><div class="seclisttime fl">(.*?)</div></div>',contents2),
                    re.findall('</span>                        <a href="(.*?)" target="_blank">(.*?)</a></div><div class="seclisttime fl">(.*?)</div></div>',contents2),
                ]
                for content in contents:
                    if len(content)>0:
                        content=content[0]
                        linkurl=f'http://www.qhd.gov.cn/'+content[0].strip()
                        detail_res=requests.get(linkurl).content.decode('utf-8')
                        Html = etree.HTML(detail_res)
                        infocontent = html.unescape(etree.tostring(Html, method='html').decode()).replace("'", " ").replace('"', ' ')
                        title=content[1].strip()
                        publicTime=content[2].strip()
                        select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='067000', regionName='河北省', areaRegion='承德市',
                                                publicTime=publicTime, linkurl=linkurl, title=title,
                                                dataResource='', yewuType='', infoType='', infoState='', isok='',
                                                isdeal='')
                            Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                        else:
                            print('标题存在')
    except Exception as e:
        print('蚌埠\t', e)
        return qinhuangdao()
def tangshan():
    try:
        url1s = [
             f'http://www.tangshan.gov.cn/zhuzhan/zhengwuxinwen/index.html',  # 政务新闻
             # f'http://www.qhd.gov.cn/front_pcsec.do?tid=BE16A305B662511F9C82516BD16F3C24&p=1',  #  部门动态
             # f'http://www.qhd.gov.cn/front_pcsec.do?tid=677638128C3E53D4C629F745917A4CD8&p=1',  # 县区动态
        ]
        for url1 in url1s:
            contents1 = requests.get(url1).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')
            pages = int(re.findall('index_(\d+).html">尾页',contents1)[0])
            for page in range(2, pages+1):
                if page==1:
                    url=url1
                else:
                    url=url1.replace('index.html',f'index_{page}.html')
                contents2 = requests.get(url).content.decode('utf-8').replace('\n', '').replace('\r', '').replace('\t', '')

                contents=[
                    re.findall('<li><span class="title"><a href="(.*?)" target="_blank" >(.*?)</a></span><span class="date">(.*?)</span><span class="clear"></span></li>',contents2),
                    re.findall('</span>                        <a href="(.*?)" target="_blank">(.*?)</a></div><div class="seclisttime fl">(.*?)</div></div>',contents2),
                ]
                for content in contents:
                    if len(content)>0:
                        content=content[0]
                        linkurl=f'http://www.tangshan.gov.cn'+content[0].strip()
                        detail_res=requests.get(linkurl).content.decode('utf-8')
                        Html = etree.HTML(detail_res)
                        infocontent = html.unescape(etree.tostring(Html, method='html').decode()).replace("'", " ").replace('"', ' ')
                        title=content[1].strip()
                        publicTime=content[2].strip()
                        select = Mysql.select_xinwen(title=title)  # 查询标题是否存在
                        if select == None:
                            uid = uuid.uuid4()
                            Mysql.insert_xinwen_baseinfo(uid=uid, regionCode='063000', regionName='河北省', areaRegion='唐山市',
                                                publicTime=publicTime, linkurl=linkurl, title=title,
                                                dataResource='', yewuType='', infoType='', infoState='', isok='',
                                                isdeal='')
                            Mysql.insert_xinwen_detailinfo(uid=uid, infocontent=infocontent)
                        else:
                            print('标题存在')
    except Exception as e:
        print('蚌埠\t', e)
        return tangshan()


# shengyw()
# shijiazhuang()
# chengde()
# zhangjiakou()
# qinhuangdao()
tangshan()