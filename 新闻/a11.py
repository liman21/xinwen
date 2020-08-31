import requests

# 南宁
# 厦门

for page in range(3,6):
    url = 'http://www.xmzyjy.cn/XmUiForWeb2.0/articleNews/getNewsPageList.do'
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8',
        'Cookie': 'Hm_lvt_b9b3de9840555ca877bfb52b9430f10b=1598679800; Hm_lpvt_b9b3de9840555ca877bfb52b9430f10b=1598680386',
        'Host': 'www.xmzyjy.cn',
        'Origin': 'http://www.xmzyjy.cn',
        'Referer': 'http://www.xmzyjy.cn/XmUiForWeb2.0/xmebid/default.do',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36',
        'X-Requested-With ': 'XMLHttpRequest'
    }
    data = {
        'pageIndex':f'{page}','pageSize':'10','bigClassId':'13','keyWord':""
    }
    content=requests.post(url,headers=headers,data=data).content.decode('utf-8').replace('\n','').replace('\t','').replace('\r','')
    import re
    contts=re.findall('<td align="left" valign="middle" style="border-style:None;"><a href="(.*?)" target="_blank" title="(.*?)">(.*?)</a></td><td align="center" valign="middle" style="border-style:None;width:70px;">(.*?)</td></tr>',content)
    for cont in contts:
        href=cont[0]
        title=cont[1]
        publictime=cont[3]
        link='https://www.nnggzy.org.cn'+href
        print('dd')
