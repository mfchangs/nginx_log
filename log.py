#_*_coding:utf-8_*_
import re
import time
import sys
from collections import OrderedDict

#nginx access.log中的格式例子
#url='106.120.173.123 - - [22/May/2017:23:59:48 +0800] "GET /list/5100101.html HTTP/1.1" 200 1367 "-" "Sogou web spider/4.0(+http://www.sogou.com/docs/help/webmasters.htm#07)" - '

class Statistics:
    def __init__(self,log_type,ip_address,number,flag,log_path):
        self.log_type = log_type
        self.ip_address = ip_address
        self.number = number
        self.flag = flag
        self.log_path = log_path
        self.log_dict = {}

    #nginx access方法        
    def nginx_access(self):
        log_file = open(self.log_path,'r')
        for i in log_file:
            pattern_math = re.match(pattern,i)
            if self.ip_address:     #如果输入IP地址
                if pattern_math.group("remote") == self.ip_address:
                    if pattern_math.group("remote") not in self.log_dict:   #判断IP地址是否在字典self.log_dict
                        self.log_dict.setdefault(self.ip_address, {})["number"] = 1 #统计此IP地址出现的次数
                    else:
                        self.log_dict[self.ip_address]["number"] = self.log_dict[self.ip_address]["number"] + 1
            else:   #不输入IP地址
                if pattern_math.group("remote") not in self.log_dict:
                    self.log_dict.setdefault(pattern_math.group("remote"),{})["number"] = 1
                else:
                    self.log_dict[pattern_math.group("remote")]["number"] = self.log_dict[pattern_math.group("remote")]["number"] + 1
        log_file.close()
        return self.log_dict

    #nginx error方法
    def nginx_error(self):
        pass

    #正序显示方法
    def sort(self,log_dict):
        sort_log = sorted(log_dict.items(),key = lambda d:d[1]['number'],reverse=True)  #根据字典中的number的值进行排序
        limit_sort_log = []
        if self.number != 0:    #输入显示指定个数的IP地址时，即number不等于0时
            for i in range(self.number):
                limit_sort_log.append(sort_log[i])
            sort_log = limit_sort_log
        return sort_log

    #倒序显示方法
    def resverse(self,log_dict):
        resverse_log = sorted(log_dict.items(),key = lambda d: d[1]['number'],reverse=False)
        limit_resverse_log = []
        if self.number != 0:
            for i in range(self.number):
                limit_resverse_log.append(resverse_log[i])
            resverse_log = limit_resverse_log
        return resverse_log

    def nginx_error(self):
        pass

    #执行方法
    def run(self):
        if self.log_type == 'access' and self.ip_address:   #分析access.log且指定IP地址时
            self.nginx_access()
            return sorted(self.log_dict.items())

        elif self.log_type == 'error' and self.ip_address:  #分析error.log且指定IP地址时
            self.nginx_error()
            return  sorted(self.log_dict.items())

        elif self.log_type == 'access':     
            if self.flag != False:      #access.log的正序
                self.nginx_access()
                resverse_log =self.sort(self.log_dict)
                return resverse_log
            else:
                self.nginx_access()     #access.log的倒序
                sort_log = self.resverse(self.log_dict)
                return sort_log

        elif self.log_type == 'error':  
            if self.flag != False:      #error.log的正序
                self.nginx_error()
                resverse_log = self.sort(self.log_dict)
                return resverse_log
            else:
                self.nginx_error()      #error.log的倒序
                sort_log = self.resverse(self.log_dict)
                return sort_log
#用户输入函数
def User_input():
	
    #运行此脚本时的第一个位置参数是日志文件
    log_path = sys.argv[1]
    log_path = log_path.strip()

    
    log_type = input("请输入日志文件类型access或error,默认是access: ").strip()
    if log_type != 'access' or log_type != 'error':
        log_type = 'access'

    #进行循环，判断用户输入的IP是否被ip_pattern匹配；匹配则有效，否则为无效
    while True:
        ip_address = input('请输入IP地址，留空则为所有，默认为空: ').strip()
        if ip_address:
            if re.match(ip_pattern,ip_address):
                break
            else:
                print('错误！！输入IP地址错误，须重新输入')
                continue
        else:
            break

    number = input("请输入显示IP地址的个数，默认显示所有: ").strip()
    if number.isdigit():
        number = int(number)
    else:
        number = 0

    flag = input("输入False或false时，将倒序显示；其他则正序显示: ").strip()
    if flag == 'false':
        flag = False
    elif flag != True or flag != False:
        flag = True

    #当number与ip_address同时输入时，number赋值为0
    if ip_address and number:
        number = 0

    return log_path,log_type,ip_address,number,flag

#预先编译正则表达式，用于匹配nginx access.log日志
pattern=re.compile(r'(?P<remote>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<time>.*)\] "(?P<request>.*)" (?P<status>\d+) (?P<length>\d+) ".*" "(?P<agent>.*)"')

#用于匹配用户输入的IP地址是否有效
ip_pattern=re.compile(r'(?P<remote>\d+\.\d+\.\d+\.\d+)')


if __name__ == "__main__":
    log_path,log_type,ip_address,number,flag = User_input()

    statistics = Statistics(log_type,ip_address,number,flag,log_path)
    print_log = statistics.run()
    print()
    for key in print_log:
        print("{}\t{}".format(key[0],key[1]['number']))

