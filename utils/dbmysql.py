from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pymysql

DB_URI = "mysql+mysqlconnector://jscadmin01:Jsc190203@rm-2zeo7x35d2iqlqk71lo.mysql.rds.aliyuncs.com:3306/bh_gl?charset=utf8"
# DB_URI = "mysql+pymysql://root:password@127.0.0.1:3306/ceshi?charset=utf8mb4"
engine = create_engine(DB_URI, echo=False, pool_size=10, pool_recycle=60)

host = "rm-2zeo7x35d2iqlqk71lo.mysql.rds.aliyuncs.com"#ip地址
port = 3306#端口号
user = "jscadmin01"#数据库的用户名
passwd="Jsc190203"#数据库的密码
db='bh_gl'#你要连接的数据库名称

#
# host = "127.0.0.1"#ip地址
# port = 3306#端口号
# user = "root"#数据库的用户名
# passwd="password"#数据库的密码
# db='ceshi'#你要连接的数据库名称


def getConnection():
    try:
        #连接数据库
        conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, charset="utf8", db=db)
        #设置游标
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print('蚌埠\t', e)
        return None
def execute(sql):
    # 获取连接
    conn, cur = getConnection()
    try:
        #开启事物
        conn.begin()
        # 游标执行sql语句
        cur.execute(sql)
        # 连接进行事务提交
        conn.commit()
        # 如果程序执行无误，返回True
        return True
    except Exception as e:
        print('蚌埠\t', e)
        return False
    finally:
        cur.close()
        conn.close()

# 插入，修改，删除操作
def query(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句
        DB.execute(sql)
        DB.commit()
        return True
    except Exception as ex:
        print("exec sql got error:%s" % (ex))
        DB.rollback()
        return False
    finally:
        DB.close()


# 插入，修改，删除操作
def query_many(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句
        for item in sql:
            DB.execute(item)
        DB.commit()
        return True
    except Exception as ex:
        print("exec sql got error:%s" % (ex))
        DB.rollback()
        return False
    finally:
        DB.close()


# 查询第一条数据
def first(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句，.first  session对象返回第一条数据
        rs = DB.execute(sql).first()
        DB.commit()
        return rs
    except Exception as ex:
        print(ex)
        DB.rollback()
        return False
    finally:
        DB.close()


# 查询多条数据
def fetchall(sql):
    # 创建DBSession类型:
    DB_Session = sessionmaker(bind=engine)
    # 创建session对象:
    DB = DB_Session()
    try:
        # 执行sql语句,.fetchall  session对象返回全部数据
        rs = DB.execute(sql).fetchall()
        DB.commit()
        return rs
    except Exception as ex:
        print("exec sql got error:%s" % (ex))
        DB.rollback()
        return False
    finally:
        DB.close()


# # 插入，修改，删除操作
# def query1(sql):
#     # 创建DBSession类型:
#     DB_Session = sessionmaker(bind=engine1)
#     # 创建session对象:
#     DB = DB_Session()
#     try:
#         # 执行sql语句
#         DB.execute(sql)
#         DB.commit()
#         return True
#     except Exception as ex:
#         print("exec sql got error:%s" % (ex))
#         DB.rollback()
#         return False
#     finally:
#         DB.close()
#
#
# # 插入，修改，删除操作
# def query_many1(sql):
#     # 创建DBSession类型:
#     DB_Session = sessionmaker(bind=engine1)
#     # 创建session对象:
#     DB = DB_Session()
#     try:
#         # 执行sql语句
#         for item in sql:
#             DB.execute(item)
#         DB.commit()
#         return True
#     except Exception as ex:
#         print("exec sql got error:%s" % (ex))
#         DB.rollback()
#         return False
#     finally:
#         DB.close()
#
#
# # 查询第一条数据
# def first1(sql):
#     # 创建DBSession类型:
#     DB_Session = sessionmaker(bind=engine1)
#     # 创建session对象:
#     DB = DB_Session()
#     try:
#         # 执行sql语句，.first  session对象返回第一条数据
#         rs = DB.execute(sql).first()
#         DB.commit()
#         return rs
#     except Exception as  ex:
#         print("exec sql got error:%s" % (ex))
#         DB.rollback()
#         return False
#     finally:
#         DB.close()
#
#
# # 查询多条数据
# def fetchall1(sql):
#     # 创建DBSession类型:
#     DB_Session = sessionmaker(bind=engine1)
#     # 创建session对象:
#     DB = DB_Session()
#     try:
#         # 执行sql语句,.fetchall  session对象返回全部数据
#         rs = DB.execute(sql).fetchall()
#         DB.commit()
#         return rs
#     except Exception as ex:
#         print("exec sql got error:%s" % (ex))
#         DB.rollback()
#         return False
#     finally:
#         DB.close()
