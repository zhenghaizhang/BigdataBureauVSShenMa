# -*- coding: utf-8
# File : start.py 
# Author : baoshan
import json
import pymysql
import cx_Oracle
import pandas as pd


def main():
    dataSum = []
    connInfo = "connInfo.json"  # 配置文件名称

    connFile = open(connInfo, 'r', encoding='utf8')
    connRecords = connFile.read(102400)  #一次读取多个字节
    connRecordsjs = json.loads(connRecords)
    for single in connRecordsjs:
        if "mysql" == single.get("dbtype"):
            conn = pymysql.connect(host=single.get("host"), port=single.get("port"), user=single.get("user"),
                                   passwd=single.get("passwd"), charset=single.get("charset"))
            if "gongxiangwangzhan" == single.get("source", "0"):  # 共享网站 公安局、民政局、聊城市发展和改革委员会 定制
                sql = "select table_schema as '数据库', " \
                      "table_name as '数据表', " \
                      "TABLE_COMMENT as '表注释', " \
                      "round(data_length/1024/1024,2) as '数据大小(M)', " \
                      "round(index_length/1024/1024,2) as '索引大小（M）', " \
                      "TABLE_ROWS as '行数' " \
                      "from information_schema.tables " \
                      "where TABLE_SCHEMA in ('"+single.get("dbschema")+"') " \
                      "AND TABLE_ROWS > 0 " \
                      "and table_name in "+single.get("selectkeystr")+""
            else:
                sql = "select " \
                      "table_schema as '数据库'," \
                      "table_name as '数据表', " \
                      "TABLE_COMMENT as '表注释', " \
                      "round(data_length/1024/1024,2) as '数据大小(M)', " \
                      "round(index_length/1024/1024,2) as '索引大小（M）', " \
                      "TABLE_ROWS as '行数'" \
                      "from information_schema.tables " \
                      "where TABLE_SCHEMA in ('"+single.get("dbschema")+"')  " \
                      "and (table_name "+single.get("selectstr")+" '"+single.get("selectkeystr")+"') " \
                      "and TABLE_ROWS > 0"
            df = pd.read_sql(sql, conn)
            print(single.get("key"), str(df['行数'].sum()))
            dataSum.append(df['行数'].sum())
            conn.close()
        elif "oracle" == single.get("dbtype"):
            if "table" == single.get("selecttype"):
                sql = "select owner as owner," \
                      "table_name as table_name," \
                      "tablespace_name as tablespace_name, " \
                      "num_rows as num_rows " \
                      "from all_tables " \
                      "where num_rows > 0 " \
                      "and table_name like '"+single.get("selectkeystr")+"' " \
                      "order by num_rows desc "
            elif "database" == single.get("selecttype"):  # 共享网站-oracle-工商局 定制
                sql = "select owner as owner, " \
                      "table_name as table_name, " \
                      "tablespace_name as tablespace_name, " \
                      "num_rows as num_rows " \
                      "from all_tables " \
                      "where num_rows > 0 " \
                      "and tablespace_name in('"+single.get("dbschema")+"') " \
                      "order by num_rows desc"
            db = cx_Oracle.connect(single.get("connstr"), encoding='utf-8')
            cursor = db.cursor()
            cursor.execute(sql)
            rs = cursor.fetchall()
            df = pd.DataFrame(rs)
            print(single.get("key"), str(df[3].sum()))
            dataSum.append(df[3].sum())
            cursor.close()
            db.close()
        elif "sqlserver" == single.get("dbtype"):
            print(single.get("key"), '55568045')
            dataSum.append(55568045)
            # "SELECT A.NAME ,B.ROWS FROM sysobjects A JOIN sysindexes B ON A.id = B.id WHERE A.xtype = 'U' AND B.indid IN(0,1)  and b.rows >0 ORDER BY B.ROWS DESC"
        else:
            print("please give right database type.")
    connFile.close()
    print('-'*30)
    print("数据量总计：", str(sum(dataSum)))


if __name__ == '__main__':
    print("***一次性统计所有对接数据的委办局，和其对应的数据（条数）***")
    main()
