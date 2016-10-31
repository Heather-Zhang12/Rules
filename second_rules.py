#coding:utf-8
import  MySQLdb
import datetime
import Apriori_support
import time


#日期时间格式转化
def shift_time(date_time):
    split=datetime.datetime.strptime(date_time,'%Y%m%d%H%M%S')
    result=split.strftime('%Y-%m-%d %H:%M:%S')
    return result

def get_dataset(StartTime,EndTime,stock):

    time_length = [] #用于存储每只股票存在数据的时间窗口长度
    dataset = [] #用来存储每天上涨的股票
    data = {} #用来存储每支股票每天上涨情况
    try:
        conn = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',
                               port=3306,db='test_t')
        cursor = conn.cursor()
        for j in range(0,len(stock)):  #nTrend代表当天上涨或下跌，‘1’涨，‘0’跌

            sql = "select nTrend from" + "`" + stock[j] + "`" + "where nTime <="+"'"+EndTime +"'"+\
                  " and " + "nTime >=" +"'"+ StartTime +"'"+";"

            rs = cursor.execute(sql) #rs为该支股票存在数据的时间窗口长度
            # print rs
            #将数据集转化成一个二维列表
            for i in range(0,rs):
                data[i] = 'NoRise'#初始化股票每天上涨情况,'NoRaise'代表未上涨
                if(j == 0):
                    dataset.append([]) #初始化数据集，均为一个空列表

            time_length.append(rs)#存储查询结果窗口长度
            # print "time_length:"
            # print time_length
            info = cursor.fetchmany(rs)#得到查询结果集
            # print "info:"
            # print info
            i = 0
            for (nTrend,) in info:#遍历查询结果集，如果当天上涨，就加入字典data[i] = stock[j]
                if(nTrend == 1):
                    data[i] = stock[j]
                i = i+1

            #print data

            for i in data:
                if(data[i] != 'NoRise'):#将上涨股票代码加入数据集
                    try:
                        dataset[i].append(data[i])
                    except IndexError as e:
                       print u"该时间窗口内股票数据不完全，请调整时间时间窗口后重新请求1"
                       exit()

         #for i in range(0,len(time_length)):#检查所有股票存在数据的时间长度是否相等，
                                             # 如果不等则不能得到结果数据集，退出程序
         #    if(time_length[0] != time_length[i]):
         #        print u"该时间窗口内股票数据不完全，请调整时间时间窗口后重新请求2"
         #        print i   #说明第i只股票有停盘现象
         #        exit()

        cursor.close()
        conn.close()

    except MySQLdb.Error,e:
      print "Mysql Error %d: %s" % (e.args[0], e.args[1])

    return dataset
def stock_garbatrage(stock,starttime,endtime,minSupport,minConf,filepath):

    dataset = []
    dataset_temp = get_dataset(starttime,endtime,stock)
    for i in dataset_temp:
        if (i != []):
             dataset.append(i)
    print len(dataset)

    L,SupportData = Apriori_support.apriori(dataset,minSupport)
    print L
    rules = Apriori_support.generateRules(L,SupportData,minConf,filepath)
    print rules

if __name__ == "__main__":
    path = "D:/Program Files/python project/result/second.txt"  #规则写入文件
    start_time = time.time()

    stock = ['600007', '600064', '600215', '600604', '600639', '600648', '600658', '600736', '600895']


    #如果starttime和endtime的位数不一致则手动在前面添加0使位数对齐。
    stock_garbatrage(stock=stock,starttime='0930000000',endtime='1130000000',
                     minSupport=0.1,minConf=0.1,filepath=path)

    end_time = time.time()
    print end_time - start_time
