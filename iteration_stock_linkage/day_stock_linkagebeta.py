#coding:utf-8
import apriori_support
import MySQLdb
import itertools
from connect_db import *
from datetime import date
from datetime import timedelta
import time

class StoreSupportData(object):
    def __init__(self):
        self.support_data = []

    def store_support(self, start_date, old_start_date,support_data): # store support_data
        self.support_data = []
        for _set in support_data:
            data = {}
            list_str = list(_set)
            support = support_data[_set]
            data['startdate'] = start_date
            data['transset'] = str(list_str)
            data['support'] = support
            self.support_data.append(data)
        try:
            with open_session() as s:
                s.execute(
                    SetSupport.__table__.insert(), self.support_data
                )
                s.query(SetSupport).filter(SetSupport.startdate == old_start_date).delete()
                s.commit()
        except Exception as e:
            print e.args



class StoreRules(object):
    def __init__(self):
        self.rules = []

    def store_rule(self, rules, start_date):
        data = []
        for rule in rules:
            lhs = str(list(rule[0]))
            rhs = str(list(rule[1]))
            conf = rule[2]
            one_rule = {}
            one_rule['startdate'] = start_date
            one_rule['LHS'] = lhs
            one_rule['RHS'] = rhs
            one_rule['conf'] = conf
            data.append(one_rule)
        try:
            with open_session() as s:
                s.execute(
                    Rules.__table__.insert(),data
                )
                s.commit()
        except Exception as e:
            print e.args

        return self.rules


class PlateLinkage(object):
    def get_iter_rules(self, start_date, l, support_data, min_conf):
        rules = apriori_support.generateRules(l, support_data, min_conf)
        if len(rules) != 0:
            store_rules = StoreRules()
            store_rules.store_rule(rules, start_date)
        return rules


class IterationRules(object):

    def get_oneday_set(self, date, stocklist):
        stock = []
        sql_part = ''
        for i in range(0, len(stocklist)):
            if i != len(stocklist)-1:
                sql_part = sql_part + "chCode = '" + stocklist[i] + "' or "
            else:
                sql_part = sql_part + "chCode = '" + stocklist[i]+"');"

        sql = "select chCode from StockDay where nDate = '" + date + "' and " + "nTrend = 1 " + " and (" + sql_part
        try:
            conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='platelinkage')
            cursor = conn.cursor()
            result = cursor.execute(sql)
            stockid = cursor.fetchmany(result)
            for (stockid,) in stockid:
                stock.append(stockid)
        except Exception as e:
                print e.args
        return stock

    def get_new_support_data(self,stock1, stock2, support_data):
        for i in range(1, len(stock1)+1):
            for _set in itertools.chain(itertools.combinations(stock1, i)):
                if support_data.has_key(frozenset(_set)):
                    support_data[frozenset(_set)] -= 1

        for i in range(1, len(stock2)+1):
            for _set in itertools.chain(itertools.combinations(stock2, i)):
                    if support_data.has_key(frozenset(_set)):
                        support_data[frozenset(_set)] += 1
                    else:
                        print "23336666"
                        support_data[frozenset(_set)] = 1

        return support_data

def get_timewindow_dataset(start_date,end_date,stock_list):
        sql_part = ''
        _set = {}
        for i in range(0, len(stock_list)):
            if i != len(stock_list)-1:
                sql_part = sql_part + "chCode = '" + stock_list[i] + "' or "
            else:
                sql_part = sql_part + "chCode = '" + stock_list[i]+"');"

        sql = "select chCode,nDate from StockDay where nDate >= '" + str(start_date) + "' and " + " nDate <= '" + str(end_date) +"' and nTrend = 1 " + " and (" + sql_part
        try:
            conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='123456', port=3306, db='platelinkage')
            cursor = conn.cursor()
            result = cursor.execute(sql)
            stockid = cursor.fetchmany(result)
            for (chCode,nDate) in stockid:
                if(_set.has_key(nDate)):
                    _set[nDate].append(chCode)
                else:
                    _set[nDate] = [chCode]


            data_set = []
            for date in _set:
                data_set.append(_set[date])

            return data_set
        except Exception as e:
                print e.args

def get_L(support_data,minsupport):
        l = {}
        for key in support_data:
           if support_data[key] >= minsupport:
               if l.has_key(str(len(key))):
                    l[str(len(key))].insert(0, key)
               else:
                    l[str(len(key))] = [key]
        L = []
        for length in l:
            L.append(l[length])
        return L



def genereterules(start_year, start_month, start_day, end_year, end_month, end_day, ulimatedate, stock_list, minsupport, minconf):

    first_start = time.time()
    plate_linkage = PlateLinkage()
    iteration_rules = IterationRules()
    store_support_data = StoreSupportData()

    start = date(start_year,start_month,start_day)
    end = date(end_year,end_month,end_day)
    old_start = start + timedelta(days=-1)
    old_start_date = str(old_start)
    start_date = str(start)
    end_date = str(end)

    print "-----start_date  to endate:" + start_date + " " + end_date

    data_set = get_timewindow_dataset(start, end, stock_list)

    support_data = {}



    for data in data_set:
        for i in range(1, len(data)+1):
            for _set in itertools.chain(itertools.combinations(data, i)):
                    if support_data.has_key(frozenset(_set)):
                        support_data[frozenset(_set)] += 1
                    else:
                        support_data[frozenset(_set)] = 1

    # store_support_data.store_support(start_date,old_start_date,support_data)

    l = get_L(support_data,minsupport)
    print "length of l: ",len(l)
    if len(l) > 1:
        plate_linkage.get_iter_rules(start_date,l,support_data,minconf)

    first_end = time.time()
    print "------first runtime:",first_end - first_start

    while start_date != ulimatedate:
        start_time = time.time()
        old_start_date = str(start)
        start = start + timedelta(days=1)
        end = end + timedelta(days=1)
        start_date = str(start)
        end_date = str(end)
        print "------start_date to endate:" + start_date + " " + end_date

        new_last_day_data = iteration_rules.get_oneday_set(end_date, stock_list)
        old_first_day_data = iteration_rules.get_oneday_set(start_date, stock_list)
        support_data = iteration_rules.get_new_support_data(old_first_day_data, new_last_day_data, support_data)
        # store_support_data.store_support(start_date,old_start_date,support_data)
        l = get_L(support_data, minsupport)
        print "length of l: ",len(l)
        if len(l) > 1:
            plate_linkage.get_iter_rules(start_date,l,support_data,minconf)
        end_time = time.time()
        print "------run_time: ",end_time-start_time

if __name__ == '__main__':
    stock_list = ['000001', '000005', '000006', '000008', '000009', '000010', '000011', '000012', '000014', '000016','000019','000025','000035','000036','000039','000040','000042','000045','000048','000062']
    #stock_list = ['000001', '000005', '000006', '000008', '000009', '000010', '000011', '000012', '000014', '000016','000019','000025','000035','000036','000039']
    #stock_list = ['000001', '000005', '000006', '000008', '000009', '000010', '000011', '000012', '000014']
    genereterules(2016, 11, 14, 2015, 12, 14, '2016-04-27', stock_list, 13, 0.8)






