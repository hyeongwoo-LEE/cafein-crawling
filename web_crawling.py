from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import json
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)


# 검색 keyword로 보낼 json 파일 로딩
# with open('file.json','r', encoding='utf-8-sig') as f:
#    data = json.load(f)
#    data = data['storeName']

# Json 파일
def toJson(store_list):
    with open('store_info_data.json', 'w', encoding='utf-8') as file :  
        json.dump(store_list, file, ensure_ascii=False, indent='\t')


query = '바람커피'
browser.get("https://m.place.naver.com/place/list?query="+ query + "&level=top")
#ser.get("https://m.search.naver.com/search.naver?query="+query)
time.sleep(10)

soup = BeautifulSoup(browser.page_source, 'html.parser')


#검색 결과 다중
store_list = soup.find_all('span', {'class':'place_bluelink YwYLL'})

for store in store_list:
    if(store.get_text() == query):
        print(store.get_text())
        print(store.parent.parent.parent.get_href())
        browser.find_element(By.CSS_SELECTOR, store).click()
        browser.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li[1]/div[2]/a[1]/div/div/span[1]').click()
        break
        
time.sleep(5)
browser.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div/div[1]/div/ul/li[2]/div/a/div[1]/div/span').click()

soup2 = BeautifulSoup(browser.page_source, 'html.parser')

span_tags = soup2.find_all('span', {'class':'ob_be'})

#카페 빈 리스트 생성
store_list = []

#카페별 딕셔너리 생성
store_dict = {"storeName" : query}

#영업시간 딕셔너리 생성
store_dict['businessHours'] = {'onMon':None, 'onTue':None, 'onWed':None, 'onThu':None, 'onFri':None, 'onSat':None, 'onSun':None}

cnt = 0
for span_tag in span_tags:
    
    if(span_tag.find("span", {'class':'kGc0c'}) == None): break
    
    day_text = span_tag.find("span", {'class':'kGc0c'}).get_text()
    time_text = span_tag.find("div", {'class': 'qo7A2'}).get_text()
    
    split_time = time_text.replace(" ","").split("-")
    
    if(len(split_time) < 2):continue
    
    if(day_text == '월'): 
        store_dict['businessHours']['onMon'] = {'open':split_time[0], 'closed':split_time[1]}
    elif(day_text == '화'): 
        store_dict['businessHours']['onTue'] = {'open':split_time[0], 'closed':split_time[1]}
    elif(day_text == '수'): 
        store_dict['businessHours']['onWed'] = {'open':split_time[0], 'closed':split_time[1]}
    elif(day_text == '목'): 
        store_dict['businessHours']['onThu'] = {'open':split_time[0], 'closed':split_time[1]}
    elif(day_text == '금'): 
        store_dict['businessHours']['onFri'] = {'open':split_time[0], 'closed':split_time[1]}
    elif(day_text == '토'): 
        store_dict['businessHours']['onSat'] = {'open':split_time[0], 'closed':split_time[1]}
    elif(day_text == '일'): 
        store_dict['businessHours']['onSun'] = {'open':split_time[0], 'closed':split_time[1]}
        
    
store_list.append(store_dict)
print(store_list)

toJson(store_list)
    
    



