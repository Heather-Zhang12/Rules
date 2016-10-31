# Rules

LoadData_day.py和LoadData_second.py分别用于将天线和秒线数据导入数据库。需要在代码中输入数据库名和原始数据位置

day_rules.py和second_rules.py分别用于进行天线和秒线的规则输出。可在代码中决定股票和时间长度，输出结果将存入指定文件夹

Apriori_support.py实现Apriori算法



操作步骤：

1.首先通过LoadData_day.py和LoadData_second.py将数据导入指定数据库

2.再通过day_rules.py和second_rules.py与相应数据库连接，进行规则分析

3.规则存入指定文件夹
