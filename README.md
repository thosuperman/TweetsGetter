# TweetsGetter
Get historical &amp; stream tweets using tweepy. 基于Tweepy的推特历史和实时数据抓取


## Usage

```
$ python3 get_tweets.py [user] [datatype] [nums_line] [nums_file]
```
Ps. 
- `get_tweets.py` is the main entry of this tool.
- [user] -> using which user's token. You can set up your own token in `tw_util.py`
- [datatype] -> whether collecting historical data (hist) or stream data (stream). 
- [nums_line] -> how many lines you'd like to have in a single file.
- [nums_file] -> how many files you'd like to have

e.g. 
```
python3 get_tweets.py xingye hist 5000 5
```
   
