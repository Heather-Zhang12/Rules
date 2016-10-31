#coding = utf8

import time
import MySQLdb


time_start = time.time()
file = open("E:\stock_list\sh.txt")
#file = open("E:\stock_list\sz.txt")
conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',port=3306,db='test_t')
cursor = conn.cursor()

while 1:
    line = file.readline()
    if not line:
        break
    code = line[:-1]
    codes = '`'+code+'`'
    print "code:"
    print code
    try:
        #create tables
        sql_create = "create table"+codes +"(" \
            "chWindCode varchar(255)," \
            "nDate varchar(255)," \
            "nTime varchar(255)," \
            "nPrice varchar(255)," \
            "iVolume varchar(255)," \
            "iTurover varchar(255)," \
            "nMatchItems varchar(255), " \
            "nInterest varchar(255)," \
            "chTradeFlag varchar(255)," \
            "chBSFlag varchar(255)," \
            "iAccVolume varchar(255),"\
            "iAccTurover varchar(255), " \
            "nHigh varchar(255)," \
            "nLow varchar(255)," \
            "nOpen varchar(255)," \
            "nPreClose varchar(255)," \
            "nTrend varchar(255))"

        cursor.execute(sql_create)
        #load csv table
        sql_load = "LOAD DATA INFILE 'C:\\\\Users\\\\Administrator\\\\Desktop\\\\20160810\\\\"+code+".SH20160810"+".csv"+"'"+\
              " REPLACE INTO TABLE "+ codes + \
              " CHARACTER SET gb2312 " \
              " FIELDS TERMINATED BY ',' ENCLOSED BY ''" \
              " LINES TERMINATED BY '\\r\\n';"
        cursor.execute(sql_load)
        #delete
        sql_delete = "delete from "+codes+" where chWindCode = 'chWindcode'"
        sql_alter = "ALTER TABLE "+codes+"MODIFY nTrend int(1);"
        cursor.execute(sql_delete)
        cursor.execute(sql_alter)

        # sql_id = "ALTER TABLE "+ codes + "ADD id INT NOT NULL PRIMARY KEY AUTO_INCREMENT FIRST"
        # sql_del = "DELETE FROM "+ codes + "WHERE id > 4380;"
        # cursor.execute(sql_id)
        # cursor.execute(sql_del)

        conn.commit()
    except MySQLdb.Error,e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])
cursor.close()
conn.close()
time_end = time.time()

print 'runtime:'
print time_end - time_start



