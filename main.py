from bing import * 
from baidu import *
 
if __name__ == '__main__':
    searchs = ["hello"]
    count = 30
    rk = int(input("请选择爬取哪个网站的图片?\n目前已经支持：\nbaidu:请输入1\nbing:请输入2\n"))
    if rk == 1:
        spiderOfBaiduImg(searchs,count)
    else:
        spiderOfBingImg(searchs,count)