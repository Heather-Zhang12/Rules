使用方法：

在数据库platelinkage下导入stock表

调用方法stock_linkage中的genereterules函数:
genereterules(2015, 10, 8, 2015,  11, 8, '2016-04-27', stock_list, 10, 0.5)
             (起始年,月,日,终止年,月,日 ,最终日期   ,  股票列表,minsupport,minconf)

历史支持度存储在表setsupport，历史强关联规则存储在表rules