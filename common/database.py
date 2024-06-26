# -*- coding: utf-8 -*-

"""
@author: gaojie
@File: database.py
@IDE: PyCharm
@time: 2023-06-12 16:06
@description: 数据库操作
"""
import jsonpath, redis
import pymysql
import pymysql.cursors
from warnings import filterwarnings
# 忽略 Mysql 告警信息
filterwarnings("ignore", category=pymysql.Warning)
from confluent_kafka import Consumer, TopicPartition, admin

from common.basefunc import config_dict

class MysqlConn:
    """
    封装MySQL常用方法。
    """

    def __init__(self):
        try:
            # 建立数据库连接
            mysql_db = config_dict['mysql_db']
            self.conn = pymysql.connect(host=mysql_db['host'],
                                        port=mysql_db['port'],
                                        user=mysql_db['user'],
                                        passwd=mysql_db['password'])
            # 创建游标
            self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            raise Exception("Mysql数据库连接失败：" + str(e))

    def __del__(self):
        try:
            # 关闭游标
            self.cur.close()
            # 关闭连接
            self.conn.close()
        except Exception as e:
            raise Exception("关闭数据库连接失败：" + str(e))

    # 增加、修改、删除命令语句
    def mysql_execute(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 提交事务
            self.conn.commit()
        except Exception as e:
            # 出错时回滚
            self.conn.rollback()
            raise Exception('执行数据库操作失败：' + str(e))

    # 查询所有数据,多个值
    def mysql_query(self, sql):
        try:
            # 执行sql语句
            self.cur.execute(sql)
            # 查询结果
            # data = self.cur.fetchall()
            # 查询单条数据
            data = self.cur.fetchone()
            return data
        except Exception as e:
            raise Exception('执行数据库查询失败：' + str(e))


class RedisConn:
    """
    封装Redis常用方法。
    """

    def __init__(self, db=0, decode_responses=True):
        redis_config = config_dict['redis']
        redis_config['db'] = db
        redis_config['decode_responses'] = decode_responses
        self.conn = redis.StrictRedis(**redis_config)

    def __del__(self):
        self.conn.close()


class KafkaConn:
    """
    封装Kafka常用方法。
    """

    def __init__(self):
        try:
            # 初始化consumer
            kafka_conf = config_dict['kafka']
            # kafka_conf = {"bootstrap-servers": "192.168.148.174:9094"}
            try:
                kafka_client = admin.AdminClient({'bootstrap.servers': kafka_conf['bootstrap-servers']})
                kafka_client.list_topics(timeout=10)
            except Exception as e:
                raise Exception("Kafka连接失败：" + str(e))
            self.consumer = Consumer({
                'bootstrap.servers': kafka_conf['bootstrap-servers'],  # kafka服务器地址
                'group.id': 'mygroup',
                'auto.offset.reset': 'latest',
            })
        except Exception as e:
            raise Exception("Kafka初始化consumer失败：" + str(e))

    def kafka_get_msg(self, topic):
        """
        获取kafka消息
        :param topic: topic
        :return:
        """
        try:
            # 获取topic的分区
            partitions = self.consumer.list_topics('user-password-update').topics['user-password-update'].partitions.keys()
            last_offset = 0
            msg = None
            for p in partitions:
                tp = TopicPartition(topic, p)  # 获取topic的分区
                # 获取当前分区最新的offset
                last_par_offset = self.consumer.get_watermark_offsets(tp)[1]
                if last_par_offset > last_offset:   # 获取最新的offset
                    last_offset = last_par_offset
                    tp.offset = last_offset - 1
                    self.consumer.assign([tp])
                    msg = self.consumer.consume(1)[0].value().decode('utf-8')
            return msg
        except Exception as e:
            raise Exception("kafka获取消息失败：" + str(e))

    def __del__(self):
        try:
            # 关闭consumer
            self.consumer.close()
        except Exception as e:
            raise Exception("kafka关闭consumer失败：" + str(e))


class HandleDB(MysqlConn):
    """
    处理数据库操作
    """

    def handle_dbdata(self, dbdata_list):
        """
        数据库操作
        :param dbdata_list: 数据库操作数据
        :return:
        """
        db_dict = {}
        try:
            if isinstance(dbdata_list, list):
                for dbdata in dbdata_list:
                    db_type = dbdata['type']   #数据库类型
                    db_sql = dbdata['sql']     #数据库操作语句
                    if db_type == 'mysql':     #mysql数据库
                        sql_list = db_sql.split(';')    #分割sql语句
                        for sql in sql_list:
                            if sql:
                                if sql[0:6].upper() == 'SELECT':   #查询语句
                                    sql_data = self.mysql_query(sql)
                                    for param in dbdata['sqldata']:
                                        value = jsonpath.jsonpath(sql_data, param['jsonpath'])
                                        name = param['name']
                                        if value:
                                            db_dict[name] = value[0]
                                        else:
                                            raise Exception("数据库参数：" + name + "获取失败，请检查用例！")
                                else:
                                    self.mysql_execute(sql)    #增删改语句
                    else:
                        raise Exception("当前暂不支持此种数据库类型：" + str(db_type))
            else:
                raise Exception("数据库操作数据格式错误，非列表格式，请检查！")
        except Exception as e:
            raise Exception("数据库操作失败：" + str(e))
        return db_dict



