#
# def start0():
#     from 新闻.shandong import ready
# def start1():
#     from 新闻.fujian import ready1
# def start2():
#     from 新闻.jiangxi import ready2
# def start3():
#     from 新闻.guizhou import ready3
# def start4():
#     from 新闻.anhui import ready4
# def start5():
#     from 新闻.hunan import ready5

import os,time
from time import sleep
from threading import Thread

# def run1():
#     from .anhui import ready4
#     from .shandong import ready
#
#     t0 = Thread(target=ready4, )
#     t1 = Thread(target=ready, )

def run():
    while 1:
        from gevent import monkey
        # 遇到阻塞自动切换协程，程序启动时执行monkey.patch_all()解决
        monkey.patch_all()

        import gevent
        time_begin = time.time()
        gevent.joinall([
            os.system("python anhui.py"),os.system("python fujian.py"),os.system("python guangdong.py"),
            os.system("python guangxi.py"),os.system("python guizhou.py"), os.system("python hainan.py"),
            os.system("python heilongjiang.py"),os.system("python hubei.py"),os.system("python hunan.py"),
            os.system("python jiangxi.py"), os.system("python neimeng.py"),os.system("python shandong.py"),
            os.system("python sichuan.py"),  os.system("python xinjiang.py"),
        ])
        print(time.time() - time_begin)



run()
# os.system("python anhui.py")
# # 定时 1小时 后执行
# sleep(1800)
# # 定时 1小时 后执行
# os.system("python shandong.py")
# sleep(900)
# os.system("python fujian.py")
# sleep(1800)
# os.system("python jiangxi.py")
# sleep(1800)
# os.system("python guizhou.py")
# sleep(1800)
# os.system("python hunan.py")
# os.system("python hubei.py")
