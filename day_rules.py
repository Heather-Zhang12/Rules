#coding:utf-8
import  MySQLdb
import Apriori_support
import time


list = []
def get_dataset(StartTime,EndTime,stock):

    time_length = [] #用于存储每只股票存在数据的时间窗口长度
    dataset = [] #用来存储每天上涨的股票
    data = {} #用来存储每支股票每天上涨情况

    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',
                               port=3306,db='test')
        cursor = conn.cursor()

        for j in range(0,len(stock)):    #nTrend代表当天上涨或下跌，‘1’涨，‘0’跌
            sql = "select nTrend from" + "`" + stock[j] + "`" + \
                  "where nDate <= str_to_date('" + EndTime +"','%Y-%m-%d')"+\
                  " and " + "nDate >= str_to_date('" + StartTime +"','%Y-%m-%d');"
            rs = cursor.execute(sql) #rs为该支股票存在数据的时间窗口长度
            # print rs
            #将数据集转化成一个二维列表
            for i in range(0,rs):
                data[i] = 'NoRaise'#初始化股票每天上涨情况,'NoRaise'代表未上涨
                if(j == 0):
                    dataset.append([]) #初始化数据集，均为一个空列表

            time_length.append(rs)#存储查询结果窗口长度
            # print "time_length:"
            # print time_length
            info = cursor.fetchmany(rs)#得到查询结果集
            #print "info:"
            #print info

            i = 0
            for (nTrend,) in info:#遍历查询结果集，如果当天上涨，就加入字典data[i] = stock[j]
                if(nTrend == 1):
                    data[i] = stock[j]
                i = i+1

            #print data

            for i in data:
                if(data[i] != 'NoRaise'):#将上涨股票代码加入数据集
                    try:
                        dataset[i].append(data[i])
                    except IndexError as e:
                       print u"该时间窗口内股票数据不完全，请调整时间窗口后重新请求1"
                       exit()

        for i in range(0,len(time_length)):#检查所有股票存在数据的时间长度是否相等，
                                            # 如果不等则不能得到结果数据集，退出程序
            if(time_length[0] != time_length[i]):
                print u"该时间窗口内股票数据不完全，请调整时间窗口后重新请求2"
                print i  #说明第i只股票有停盘现象
                exit()

        cursor.close()
        conn.close()

    except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return dataset
def stock_garbatrage(stock,startdate,enddate,minSupport,minConf,filepath):

    dataset = []
    dataset_temp = get_dataset(startdate,enddate,stock)
    for i in dataset_temp:
        if (i != []):
             dataset.append(i)
#    print len(dataset)
    print dataset

    L,SupportData = Apriori_support.apriori(dataset,minSupport)
    print L
    rules = Apriori_support.generateRules(L,SupportData,minConf,filepath)
    print rules


if __name__ == "__main__":
    path = "D:/Program Files/python project/result/day1.txt"  #规则写入文件
    time_start = time.time()

    stock = ['600007', '600064', '600215', '600604', '600639', '600648', '600658', '600736', '600895']
    print len(stock)

    stock_garbatrage(stock=stock,startdate='2016-08-01',enddate='2016-08-31',
                     minSupport=0.7,minConf=0.8, filepath=path)


    time_end = time.time()

    print 'runtime:'
    print time_end - time_start


