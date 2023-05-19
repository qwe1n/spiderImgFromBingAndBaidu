import os
from time import sleep
from io import BytesIO
import requests
from PIL import Image
import tqdm

header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
size = (224,224)

def getImg(url,idx,path,search):
    try:
        img=requests.get(url,headers=header,timeout=2)
    except:
        return
    try:
        search = "_".join(search.split(" "))
    except:
        pass
    img = Image.open(BytesIO(img.content))
    
    img = img.resize(size, Image.ANTIALIAS).convert('RGB')
    img.save(path+search+"_"+str(idx)+'.jpg')

def spiderOfBaiduImg(searchs:list,number):
    url = 'https://image.baidu.com/search/acjson'
    cnt = number
    for search in searchs:
        print(f"正在爬取{search}")
        path='baidu_images/'+search+'/'
        if not os.path.exists(path):
            os.makedirs(path)
        bar=tqdm.tqdm(total=number)
        page=0
        number = cnt
        while(True):
            if number==0:
                break
            params={
                    "tn": "resultjson_com",
                    "logid": "11555092689241190059",
                    "ipn": "rj",
                    "ct": "201326592",
                    "is": "",
                    "fp": "result",
                    "queryWord": search,
                    "cl": "2",
                    "lm": "-1",
                    "ie": "utf-8",
                    "oe": "utf-8",
                    "adpicid": "",
                    "st": "-1",
                    "z": "",
                    "ic": "0",
                    "hd": "",
                    "latest": "",
                    "copyright": "",
                    "word": search,
                    "s": "",
                    "se": "",
                    "tab": "",
                    "width": "",
                    "height": "",
                    "face": "0",
                    "istype": "2",
                    "qc": "",
                    "nc": "1",
                    "fr": "",
                    "expermode": "",
                    "force": "",
                    "pn": str(60*page),
                    "rn": number,
                    "gsm": "1e",
                    "1617626956685": ""
                }
            try:
                result = requests.get(url, headers=header,params=params).json()
            except:
                page+=1
                continue
            url_list=[]
            if 'data' not in result:
                sleep(2)
                continue
            for data in result['data'][:-1]:
                url_list.append(data['thumbURL'])
            for i in range(len(url_list)):
                getImg(url_list[i],60*page+i,path,search)
                bar.update(1)
                number-=1
                if number==0:
                    break
            page+=1