import os
import time
import urllib
import requests
import re
import tqdm
from bs4 import BeautifulSoup
import time
from PIL import Image
from PIL.Image import LANCZOS
from io import BytesIO
 
header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
size = (224,224)
def getImg(imgurl,count,path,role):
    #print(imgurl)
    try:
        response = requests.get(imgurl,timeout=2)
        img = Image.open(BytesIO(response.content))
        img = img.resize(size, resample=LANCZOS).convert('RGB')
        img.save(os.path.join(path,f"{role}_{count}.png"))
        return 1
    except Exception as e:
        #print(e)
        return 0
        
def crawlBing(url, key, first, loadNum, sfx, cnt, path,bar,role):
    time.sleep(1)
    while True:
        try:
            html = requests.get(url.format(key, first, loadNum, sfx),
									headers=header).text
            break
        except:
            time.sleep(1.5)
            continue
    soup = BeautifulSoup(html, "lxml")

    link_list = soup.find_all("a", class_="iusc")
    rule = re.compile(r"\"murl\"\:\"http\S[^\"]+")
    for link in link_list:
        result = re.search(rule, str(link))
        try:
            imgurl = result.group(0)
        except:
            continue
        imgurl = imgurl[8:len(imgurl)]
        dd = getImg(imgurl, cnt, path,role)
        bar.update(dd)
        cnt += dd

    return cnt
 

def spiderOfBingImg(searchs:list,number:int):
    url = "https://cn.bing.com/images/async?q={0}&first={1}&count={2}&scenario=ImageBasicHover&datsrc=N_I&layout=ColumnBased&mmasync=1&dgState=c*9_y*2226s2180s2072s2043s2292s2295s2079s2203s2094_i*71_w*198&IG=0D6AD6CBAF43430EA716510A4754C951&SFX={3}&iid=images.5599"
    for search in searchs:
        print(f"正在爬取{search}")
        try:
            role = "_".join(search.split(" "))
        except:
            role = search
        cnt = 0
        bar = tqdm.tqdm(total=number)
        bar.update(cnt)
        path = f'bing_images/{role}/'
        if not os.path.exists(path):
            os.makedirs(path)
        key = urllib.parse.quote(search)
        first = 1
        loadNum = 30
        sfx = 1
        while cnt < number:
            cnt = crawlBing(url,key,first,loadNum,sfx,cnt, path,bar,role)
            first = cnt+1
            sfx += 1