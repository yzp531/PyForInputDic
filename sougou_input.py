import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import unquote
from datetime import datetime
id = 31
dic_dir="sougou"
strid = input("请输入搜索id:")
if strid.strip() != "" and int(strid) > 0:
    id = int(strid)
now = datetime.now()
rooturl = "https://pinyin.sogou.com/dict/cate/index/"+str(id)+"/default/"
x = requests.get(rooturl)
bs = BeautifulSoup(x.text, 'html.parser')

# Pages 取总页数
all_a = bs.find_all("div", id='dict_page_list')[0].find("ul").find_all("a")
pages = int(all_a[-2].text)
print("总页面数："+str(pages))

# 创建词库保存的文件夹
rootpath = os.path.abspath(os.path.dirname(__file__))
folder = os.path.exists(rootpath+"/"+dic_dir)
if not folder:
    os.makedirs(rootpath+"/"+dic_dir)
dic_dir=rootpath+"/"+dic_dir;  
for i in range(1, pages+1):
    start = datetime.now()
    baseurl = rooturl
    print("=================<<"+str(i)+">> START=================")
    # print("开始下载：第"+str(i)+"页")
    baseurl += ("" if i <= 1 else str(i))
    print(baseurl)
    x = requests.get(baseurl)
    bs = BeautifulSoup(x.text, 'html.parser')
    divs = bs.find_all("div", class_='dict_dl_btn')
    index = 0
    for div in divs:
        # 读取下载地址
        a = div.find("a")
        downloadurl = a["href"]
        temp = unquote(downloadurl.split("name=")[-1]).split("/")
        dic_name = unquote(temp[-1], encoding="utf-8").strip()
        file =dic_dir+"/"+dic_name+".scel"
        # 已下载直接跳过
        if (os.path.exists(file) and os.stat(file).st_size > 0):
            index += 1
            print(dic_name + "===@>"+str(index)+"已存在，无需下载")
            continue
        r = requests.get(downloadurl, stream=True, allow_redirects=True)
        # 开始下载词库文件
        with open(file, "wb+") as f:
            f.write(r.content)
            f.close()
            index += 1
            print(dic_name+"===>"+str(index)+"下载成功")
    print("单页总耗时:"+str(datetime.now()-start))
    print("=================<<"+str(i)+">> End===================")
    # print(downloadurl)
print("总耗时:"+str(datetime.now()-now))
