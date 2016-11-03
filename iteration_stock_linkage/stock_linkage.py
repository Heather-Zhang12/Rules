#coding:utf-8
import apriori_support
import MySQLdb
import itertools
from connect_db import *
from datetime import date
from datetime import timedelta
import get_dataset


class StoreSupportData(object):
    def __init__(self):
        self.support_data = []

    def store_support(self, start_date, support_data): # store support_data
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

    def get_first_rules(self, start_date, data_set, min_support, min_conf):
        l, support_data = apriori_support.apriori(data_set, min_support)
        store_support_data = StoreSupportData()
        store_support_data.store_support(start_date, support_data)
        rules = apriori_support.generateRules(l, support_data, min_conf)
        if len(rules) != 0:
            store_rules = StoreRules()
            store_rules.store_rule(rules, start_date)
        return rules

    def get_iter_rules(self, start_date, l, support_data, min_conf):
        rules = apriori_support.generateRules(l, support_data, min_conf)
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

        sql = "select chCode from Stock where nDate = '" + date + "' and " + "nTrend = 1 " + " and (" + sql_part
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

    def get_old_support_data(self, start_date):
        support_data = {}
        with open_session() as s:
            result = s.query(SetSupport).\
                        filter(SetSupport.startdate == start_date).all()
            for trans in result:
                stock_list = eval(trans.transset)
                stock_set = frozenset(stock_list)
                support_data[stock_set] = trans.support
        return support_data

    def get_new_support_data(self, stock1, stock2, support_data):
        print stock1
        print stock2
        print support_data
        for i in range(1, len(stock1)+1):
            for _set in itertools.chain(itertools.combinations(stock1, i)):
                if support_data.has_key(frozenset(_set)):
                    support_data[frozenset(_set)] -= 1

        for i in range(1, len(stock2)+1):
            for _set in itertools.chain(itertools.combinations(stock2, i)):
                if support_data.has_key(frozenset(_set)):
                    support_data[frozenset(_set)] += 1

        return support_data


def genereterules(start_year, start_month, start_day, end_year, end_month, end_day, ulimatedate, stock_list, minsupport, minconf):

    start_date = str(start_year)+'-'+str(start_month)+'-'+str(start_day)
    end_date = str(end_year)+'-'+str(end_month)+'-'+str(end_day)

    data = get_dataset.stock_garbatrage(stock=stock_list,startdate=start_date,enddate=end_date)
    plate_linkage = PlateLinkage()
    rules = plate_linkage.get_first_rules(start_date,data,minsupport,minconf)

    if len(rules) == 0:
        print "这段时间没有强关联规则，无法继续"
        exit()

    iteration_rules = IterationRules()
    store_support_data = StoreSupportData()

    while end_date != ulimatedate:
        old_start_date = start_date
        start = date(start_year,start_month,start_day)
        next_start = start + timedelta(days=1)

        end = date(end_year, end_month, end_day)
        nex_tend = end + timedelta(days=1)

        start_date = str(next_start)
        print start_date
        end_date = str(nex_tend)
        print end_date

        start_year = int(start_date.split('-')[0]); start_month = int(start_date.split('-')[1]); start_day = int(start_date.split('-')[2])
        end_year = int(end_date.split('-')[0]); end_month = int(end_date.split('-')[1]); end_day = int(end_date.split('-')[2])

        old_startset = iteration_rules.get_oneday_set(old_start_date,stock_list)
        newendset = iteration_rules.get_oneday_set(end_date,stock_list)

        oldsupportdata = iteration_rules.get_old_support_data(old_start_date)
        newsupportdata = iteration_rules.get_new_support_data(old_startset,newendset,oldsupportdata)
        print newsupportdata

        store_support_data.store_support(start_date,newsupportdata)

        l = {}
        for key in newsupportdata:
           if newsupportdata[key] >= minsupport:
               if l.has_key(str(len(key))):
                    l[str(len(key))].insert(0, key)
               else:
                    l[str(len(key))] = [key]
        L = []
        for length in l:
            L.append(l[length])
        print L
        plate_linkage.get_iter_rules(start_date, L, newsupportdata, minconf)


if __name__ == '__main__':
    stock_list = ['600064', '600007', '600215', '600604', '600639', '600648', '600658', '600736', '600895']
    # stock_list = ['600064',  '600604', '600639', '600648',  '600736']
    genereterules(2015, 10, 8, 2015, 11, 8, '2016-04-27', stock_list, 10, 0.5)






