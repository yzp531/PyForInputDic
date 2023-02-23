import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
baseurl="https://mime.baidu.com/web/iw/c/null/download_number/page:"
dic_dir="baidu"
now = datetime.now()
# 创建词库保存的文件夹
rootpath = os.path.abspath(os.path.dirname(__file__))
folder = os.path.exists(rootpath+"/"+dic_dir)
if not folder:
    os.makedirs(rootpath+"/"+dic_dir)
dic_dir=rootpath+"/"+dic_dir;  
for i in range(1, 8):
    print("=================<<"+str(i)+">> START=================")
    start=datetime.now()
    x = requests.get(baseurl+str(i))
    bs = BeautifulSoup(x.text, 'html.parser')
    divs = bs.find_all("div", class_='wordsliblistdowload')
    base_downloadurl = "https://mime.baidu.com/"
    index=0
    for div in divs:
        a = div.find("a")
        downloadurl = base_downloadurl+a["href"]
        dic_name = downloadurl.split("/")[-1]
        file = dic_dir+"/"+dic_name
        if os.path.exists(file) and os.stat(file).st_size>0:
            index+=1
            print(dic_name + "===@>"+str(index)+"已存在，无需下载")
            continue;
        r = requests.get(downloadurl, stream=True, allow_redirects=True)
        with open(file, "wb") as f:
            f.write(r.content)
            f.close()
            index+=1
            print(dic_name+"===>"+str(index)+"下载成功")
    print("单页总耗时:"+str(datetime.now()-start))
    print("=================<<"+str(i)+">> End===================")
print("总耗时:"+str(datetime.now()-now))