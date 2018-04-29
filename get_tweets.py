import sys
import tw_util
import tw_class
import tweepy
import time
import os

import daemon


def run_hist(api, nums_line, nums_file, until):
    myHistGetter = tw_class.MyHistGetter(api, nums_line, nums_file, until)

    myHistGetter.get_hist_tweet()

def run_stream(api, nums_line, nums_file):
    myStreamListener = tw_class.MyStreamListener(nums_line, nums_file)
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

    myStream.filter(track=["Trump"], languages=['en'])

def get_until(user):

    '''
    根据用户token的不同，自动划定时间范围
    :param user:
    :return: YY-MM-DD
    '''

    '''
    这里利用了3个用户的auth key, 每个用户实现抓取两天的数据
    '''

    cur_ts = time.time()
    two_days_sec = 2*24*3600

    if user == "xxx":
        return tw_util.ts2str(cur_ts - 2*two_days_sec, '%Y-%m-%d')
    elif user == "xxx":
        return tw_util.ts2str(cur_ts - two_days_sec, '%Y-%m-%d')
    elif user == "xxx":
        #return tw_util.ts2str(cur_ts, '%Y-%m-%d')
        return ""
    else:
        print("Please check if the user name is correct")
        exit()


if __name__ == "__main__":

    '''
    执行方式： python3 get_tweets.py [user] [datatype] [nums_line] [nums_file]
        e.g. python3 get_tweets.py xingye hist 5000 5
    共四个参数
        1. [user] -> xingye, huanyu, pengyuxia #即要用哪一个人的token
        2. [datatype] -> hist, stream          #历史数据还是实时数据
        3. [nums_line] -> int  # 一个文件里写多少行
        4. [nums_file] -> int #分多少个文件存储
    '''

    # user = "huanyu"
    # datatype = "hist"
    # nums_line = "1250000"
    # nums_file = "3"

    user = sys.argv[1]
    datatype = sys.argv[2]
    nums_line = sys.argv[3]
    nums_file = sys.argv[4]

    try:
        nums_line = int(nums_line)
        nums_file = int(nums_file)
    except Exception as e:
        print("Please check if nums_file is correct")
        exit()


    # 每次启动后把自己的pid写入run.pid
    # 如果启动了监控进程daemon.py, 监控进程会自动去run.pid中读取进程号并进行监控
    # 一旦意外退出，就重新启动该进程
    pid = os.getpid()

    with open("run.pid", "w") as f_pid:
        f_pid.write(str(pid))


    api = tw_util.get_auth_api(user)

    if datatype == "hist":
        until = get_until(user)
        run_hist(api, nums_line, nums_file, until)
    elif datatype == "stream":
        run_stream(api, nums_line, nums_file)
    else:
        print("please check if datatype is correct")
        exit()



