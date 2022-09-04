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


query = '투썸 명동사거리점'

browser.get("https://m.search.naver.com/search.naver?query="+query)
time.sleep(0.5)

browser.find_element(By.XPATH, '//*[@id="place-main-section-root"]/div/div[3]/div/ul/li[2]/div/a/div/div').click()
a = browser.find_element(By.XPATH, '//*[@id="_title"]/a/span[1]').text

soup = BeautifulSoup(browser.page_source, 'html.parser')

span_tags = soup.find_all("span", {'class':'ob_be'})

#카페 빈 리스트 생성
store_list = []

store_name = browser.find_element(By.XPATH, '//*[@id="_title"]/a/span[1]').text

#카페별 딕셔너리 생성
store_dict = {"storeName" : store_name}

#영업시간 딕셔너리 생성
store_dict['businessHours'] = {}

for span_tag in span_tags:
    day_text = span_tag.find("span", {'class':'kGc0c'}).get_text()
    time_text = span_tag.find("div", {'class': 'qo7A2'}).get_text()
    
    split_time = time_text.replace(" ","").split("-")
    
    print(split_time)
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
    
    



