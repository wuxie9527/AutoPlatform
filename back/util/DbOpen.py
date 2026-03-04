# coding=utf-8
'''
@Time : 2019/9/2 下午10:52
@Author : HeXW
'''
import os
import time


class DbOpen:

    def __init__(self):
        self._db_conn_infos = {}
        self.conn = None

    def add_db_info(self, dbtype, host, port, user, password, dbname, conn_name="default"):
        self._db_conn_infos[conn_name] = dbtype, host, port, user, password, dbname

    def db_connect(self, conn_name='default'):
        if self._db_conn_infos:
            if conn_name in self._db_conn_infos:
                dbtype, host, port, user, password, dbname = self._db_conn_infos[conn_name]
                if dbtype.lower() == 'mysql':
                    import pymysql
                    try:
                        conn = pymysql.connect(host=host, user=user, password=password,
                                               db=dbname, port=port, charset='utf8')
                    except pymysql.err.OperationalError:
                        print('数据库连接超时重试一次：')
                        time.sleep(2)
                        conn = pymysql.connect(host=host, user=user, password=password,
                                               db=dbname, port=port, charset='utf8')
                elif dbtype.lower() == 'oracle':
                    # 设置字符集
                    os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.AL32UTF8'
                    import cx_Oracle
                    print('创建数据库连接，连接配置:' + ','.join([host, port, user, password, dbname]))
                    dns = cx_Oracle.makedsn(host, port, dbname)
                    conn = cx_Oracle.connect(user, password, dns)
                elif dbtype.lower() == 'sqlserver':
                    import pymssql
                    conn = pymssql.connect(host, user, password,
                                           dbname, charset='GBK')
                else:
                    raise DBError('数据库连接只支持mysql、oracle和sqlServer，请确认数据库类型配置是否正确')
                return conn
            else:
                raise DBError('请确认：' + conn_name + '数据库别名是否正确！')
        else:
            raise DBError('没有数据库配置，请确认当前配置下是否配置了数据库连接信息')

    def db_isconnect(self):
        if self.conn:
            return True
        else:
            return False

    def check_sql_vial(self, sql_commd):
        '''
        判断是否是sql语句
        '''
        if sql_commd.lower().startswith(('commit', 'select', 'insert', 'update', 'delete',)):
            return True
        else:
            return False

    def db_close(self, conn):
        if conn:
            conn.close()

    def db_execute(self, sql, sql_is_select=None, exist_conn=None):
        cur = None
        conn_name = "default"
        if not self.check_sql_vial(sql):
            if '#' in sql:
                conn_name = sql.split('#')[0]
                sql = sql.split('#')[1]
                if conn_name not in self._db_conn_infos:
                    raise DBError('{}数据库连接别名不在当前数据库配置中，请确认'.format(conn_name))
                if not self.check_sql_vial(sql):
                    raise DBError('执行SQL：' + sql + '不是正确的sql语句，请确认！')
            else:
                raise DBError('执行SQL：' + sql + '不是正确的sql语句，请确认！')
        if sql_is_select is None:
            sql_is_select = True if sql.lower().startswith('select') else False
        conn = exist_conn or self.db_connect(conn_name)
        try:
            cur = conn.cursor()
            sql = sql.strip("\n\r;")
            cur.execute(sql)
            if sql_is_select:
                sqlresult = list(cur.fetchone())
            else:
                sqlresult = [(cur.rowcount,)]
                if sqlresult:
                    conn.commit()
        except Exception as e:
            raise DBError('执行SQL：' + sql + '时，数据库操作出现异常:{0}，请确认'.format(e))
        finally:
            if cur:
                cur.close()
            # try:
            #     if conn:
            #         conn.close()
            # except Exception as e:
            #     raise DBError('关闭数据库连接出现异常，{}'.format(e))
        return sqlresult

    @property
    def db_conn_infos(self):
        return self._db_conn_infos


class DBError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


if __name__ == '__main__':
    DbOpen = DbOpen()
    # DbOpen.add_db_info("sqlserver", "172.16.8.174", 3306, "db_rw", "v0iI810H_0G5g18oRcJ", "egshop_waimao")
    DbOpen.add_db_info("mysql", "172.16.8.171", 3306, "db_rw", "s2DLBdS_J6tvAdeKwL", "nsy_crm")
    # DbOpen.add_db_info("mysql", "172.16.76.239", 3306, "nsy_readonly", "t6dD6hJSTbaI.", "nsy_crm")
    # sql = "SELECT status from dbo.EgSettlement_SyncBillQueue(NOLOCK) where QueueId = 21"
    sql = "select * from nsy_fms.bd_account where account_id = 303"
    print(DbOpen.db_execute(sql))
