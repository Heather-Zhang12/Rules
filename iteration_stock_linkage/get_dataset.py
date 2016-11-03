#coding:utf-8
import  MySQLdb
import time


code = 'stock'    #表2中是天线数据
codes = '`'+str(code)+'`'


def get_dataset(StartTime,EndTime,stock):

    time_length = []    #用于存储每只股票存在数据的时间窗口长度
    dataset = []     #用来存储每天上涨的股票，二维列表
    collection = {}     #初始化最大时间长度内的所有股票nTrend为0，key值表示日期，value值表示涨跌
    data = {}     #用来存储每支股票每天上涨情况，key值为日期
    up =  {}     #存储每只股票每天涨跌情况

    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',
                               port=3306,db='platelinkage')
        cursor = conn.cursor()


        ########################找出最大时间长度并初始化collection########################################
        number = 0
        for j in range(0,len(stock)):    #nTrend代表当天上涨或下跌，‘1’涨，‘0’跌
            sql_ = "select nTrend, nDate from " + codes + \
                  " where nDate >= str_to_date('" + StartTime +"','%Y-%m-%d')"+\
                  " and " + "nDate <= str_to_date('" + EndTime +"','%Y-%m-%d')"+\
                "and " + "chCode = '" + stock[j] + "';"

            rs_ = cursor.execute(sql_) #rs为该支股票存在数据的时间窗口长度
            res_ = cursor.fetchall()
            if len(res_) > number:
                number = len(res_)
                for i in range(0, number):
                    date_time_ = res_[i][1]
                    #print "data_time:"
                    #print date_time
                    collection[date_time_] = 0

        #print "collection:"
        #print len(collection)
        #print collection
        ####################################################################################


        for j in range(0,len(stock)):    #nTrend代表当天上涨或下跌，‘1’涨，‘0’跌
            sql = "select nTrend, nDate from" + codes + \
                  "where nDate >= str_to_date('" + StartTime +"','%Y-%m-%d')"+\
                  " and " + "nDate <= str_to_date('" + EndTime +"','%Y-%m-%d')"+\
                "and " + "chCode = '" + stock[j] + "';"
            #print "sql:"
            #print sql
            rs = cursor.execute(sql)
            #print rs
            res = cursor.fetchall()


            up = {}

            #print res[0][1]
            #print res[1][0]

            data = collection.copy()


            for num in range(len(data)):          #初始化up
                up[num] = 'null'
                if(j == 0):
                    dataset.append([])          #初始化数据集，均为一个空列表
            #print up

            for i in range(len(res)):           #将股票涨跌情况加入data字典
                date_time = res[i][1]
                trend = res[i][0]
                data[date_time] = trend
                #print "data[date_time]:"
                #print data[date_time]

            time_length.append(len(res))     #存储查询结果窗口长度
            # print "time_length:"
            # print time_length         #检查各个股票时间长度

            num = 0
            #print "data.values():"
            #print data.values()
            for each in data.values():         #更新相应up字典
                if(each == 1):
                    up[num] = stock[j]
                num = num+1



            for i in range(len(up)):
                #print "up::"
                #print up[i]
                if(up[i] != 'null'):              #将上涨股票代码加入数据集
                    dataset[i].append(up[i])

            del up    #清空up、data，继续处理下一只股票
            del data


        cursor.close()
        conn.close()

    except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return dataset


def stock_garbatrage(stock,startdate,enddate):

    dataset = []
    dataset_temp = get_dataset(startdate,enddate,stock)
    for i in dataset_temp:
        if (i != []):
             dataset.append(i)

    return dataset


if __name__ == "__main__":
    time_start = time.time()

    stock = ['600064','600007', '600215', '600604', '600639', '600648', '600658', '600736', '600895']
    #stock = ['600007', '600008', '600009', '600010', '600011']
    #print len(stock)

    stock_garbatrage(stock=stock,startdate='2015-10-08',enddate='2016-1-30')


    time_end = time.time()

    print 'runtime:'
    print time_end - time_start


