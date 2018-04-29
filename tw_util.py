import re
import time
import datetime

import tw_util

import tweepy
from tweepy import OAuthHandler


# put your own token here
dict_token_xxx = {
    "consumer_key" : '',
    "consumer_secret" : '',
    "access_token" : '',
    "access_secret" : '',
}


def get_auth_api(user):

    dict_token = None

    if user == "xxx":
        dict_token = dict_token_xingye
    # ...

    else:
        print("Please check if the user name is correct")
        exit()

    consumer_key =  dict_token['consumer_key']
    consumer_secret = dict_token['consumer_secret']
    access_token = dict_token['access_token']
    access_secret = dict_token['access_secret']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    return tweepy.API(auth)


def process_tweet_text(tweet_text):

    '''
    cleansing raw tweets

    '''

    tweet_text = str(tweet_text).replace("\n", "") #转换成str， 并且清除所有换行符
    tweet_text = remove_emoji(tweet_text)  # 清除 emoj
    tweet_text = remove_weblink(tweet_text) # 清除 网址 e,g, https://mmmmmm
    tweet_text = remove_sign(tweet_text, "@") #清除 @
    tweet_text = remove_sign(tweet_text, "#") #清除 #
    tweet_text = tweet_text.replace("&amp;", "")  # 清除 &amp;
    tweet_text = tweet_text.strip()

    return tweet_text


def ts2str(ts, format='%Y-%m-%d %H:%M:%S'):

    '''
    时间戳格式化
    '''
    return datetime.datetime.fromtimestamp(ts).strftime(format)


def handle_TweepError(api):

    '''
    解决抓取历史数据时每15分钟超过180次后报错的问题
    计算reset的时间和cur当前时间，然后sleep相应的时间再继续抓取
    :param api:
    :return:
    '''

    limit = api.rate_limit_status()

    #remaining = limit['resources']['search']['/search/tweets']['remaining']
    reset_time_ts = limit['resources']['search']['/search/tweets']['reset']

    reset_time = ts2str(reset_time_ts)

    print("reset: " + reset_time)

    cur_time_ts = int(time.time())

    print("cur: " + ts2str(cur_time_ts))

    ms2wait = int(reset_time_ts) - cur_time_ts

    print("sleep {} secs".format(int(ms2wait)))

    time.sleep(ms2wait)


def remove_sign(text, sign):

    pattern = r"{}[\w\_]+".format(sign)

    filter = re.compile(pattern)

    return filter.sub(r'', text)


def remove_emoji(string):

    emoji_pattern = re.compile("["
                           "\U0001F600-\U0001F64F"  # emoticons
                           "\U0001F300-\U0001F5FF"  # symbols & pictographs
                           "\U0001F680-\U0001F6FF"  # transport & map symbols
                           "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "\U00002702-\U000027B0"
                           "\U000024C2-\U0001F251"
                           "\U0001F910-\U0001F9FF"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string)


def remove_weblink(text):

    pattern = r'[a-zA-z]+://[^\s]*'

    #(?: @[\w_]+)

    filter = re.compile(pattern)

    return filter.sub(r'', text)


if __name__ == "__main__":
    pass





