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


def qc_js(url):
    mio = []
    soup = BeautifulSoup(urlopen(url).read(), "html.parser")
    titles = soup.select("script")  # CSS 选择器
    for title in titles:
        mio.append(str(title))
    qc_cg = deleteData(str(soup), mio)
    return qc_cg


if __name__ == '__main__':
    qc_js(url='http://ggzyjy.zibo.gov.cn/TPFront/InfoDetail/Default.aspx?InfoID=16207a39-7032-47d3-a5fc-cd0b9cb998f6&CategoryNum=024001')
