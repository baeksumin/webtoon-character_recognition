import dload
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import os

# Webtoon Url : ex) 마음의 소리
url = "https://comic.naver.com/webtoon/list?titleId=20853" 

# 크롤링 우회
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'}
html = requests.get(url, headers = headers)
result = BeautifulSoup(html.content, "html.parser")

webtoonName = result.find("span", {"class", "wrt_nm"}).parent.get_text().strip().split('\n')
# webtoonName = ['마음의 소리', '\t\t\t\t\t\t\t조석']

cwd = os.getcwd()
files = os.listdir(cwd)
# 현재 directory 위치
print(cwd, end='\n\n')

# 크롤링한 이미지를 저장할 폴더를 만듦
if os.path.isdir(os.path.join(cwd,  webtoonName[0])) == False: 
    os.mkdir(webtoonName[0])
   
print(webtoonName[0] + " folder created successfully!")
os.chdir(os.path.join(cwd,  webtoonName[0])) 

title = result.findAll("td", {"class", "title"})

for t in title:
    
    # 회차별로 directory를 만든 후 해당 directory로 이동
    os.mkdir((t.text).strip()) 
    os.chdir(os.getcwd() + "//" + (t.text).strip()) 

    # 각 회차별 html 소스 가져오기
    url ="https://comic.naver.com" + t.a['href']
    html2 = requests.get(url, headers = headers) 
    result2 = BeautifulSoup(html2.content, "html.parser") 

    # webtoon image 가져오기
    webtoonImg = result2.find("div", {"class", "wt_viewer"}).findAll("img")
    num = 1 #image_name
    
    for i in webtoonImg:
        saveName = os.getcwd() + "//" + str(num) + ".jpg"
        with open(saveName, "wb") as file:
            src = requests.get(i['src'], headers = headers) 
            file.write(src.content) #
        num += 1

    os.chdir("..")

    # 한 회차 이미지 저장 완료!
    print((t.text).strip() + "   saved completely!") 