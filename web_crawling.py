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



def toJson(json_list):
    with open('store_info_data.json', 'w', encoding='utf-8') as file :  
        json.dump(json_list, file, ensure_ascii=False, indent='\t')


# 검색 keyword로 보낼 json 파일 로딩
with open('store_list_.json','r', encoding='utf-8-sig') as f:
    data = json.load(f)
    total_cnt = data['totalCnt']
    items = data['storeList']
    
    
# json 빈 리스트 생성
json_list = []

not_exist = []

for item in items:
    
    # 카페별 딕셔너리 생성
    store_dict = {"storeName" : item['storeName']}
    
    # 검색어 keyword
    query = item['storeName'].replace("메가커피","메가MGC커피")
    
    browser.get("https://m.place.naver.com/place/list?query="+ query + "&level=top")

    time.sleep(3)

    soup = BeautifulSoup(browser.page_source, 'html.parser')


    # 검색 다중 결과
    store_list = soup.find_all('span', {'class':'place_bluelink YwYLL'})

    loop_cnt = 1;
    
    for store in store_list:
        if(store.get_text() == query):
            print(store.get_text())

            try:
                browser.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li['+str(loop_cnt)+']/div[2]/a[1]/div/div/span[1]').click()
            except:
                browser.find_element(By.XPATH, '//*[@id="_list_scroll_container"]/div/div/div[2]/ul/li/div[1]').click() 
            break
        loop_cnt += 1
    else:
        print("검색 카페가 존재하지 않음 : ", query)
        not_exist.append(query)
        continue
    
    time.sleep(6)


    try:
        browser.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div/div[2]/div/ul/li[2]/div/a/div').click()
    except:
        try:
            browser.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div/div[1]/div/ul/li[2]/div/a/div').click()
        except:
            print("영업시간 데이터가 없음 : ", query)
            continue
        
          
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    
    # 전화번호 데이터
    try:
        phone = soup.find('span', {'class':'dry01'}).get_text()
        store_dict['phone'] = phone
    except:
        store_dict['phone'] = None

    # 영업시간 데이터
    span_tags = soup.find_all('span', {'class':'ob_be'})

    # 영업시간 딕셔너리 생성
    store_dict['businessHours'] = {'onMon':None, 'onTue':None, 'onWed':None, 'onThu':None, 'onFri':None, 'onSat':None, 'onSun':None}
   
    # 요일별 영업시간 데이터 수집
    for span_tag in span_tags:
        
        if(span_tag.find("span", {'class':'kGc0c'}) == None): 
            continue
        
        # 요일 데이터
        day_text = span_tag.find("span", {'class':'kGc0c'}).get_text()
        
        if(day_text != '매일'):
            day_text = day_text[0]
        
        # 영업시간 데이터
        time_text = span_tag.find("div", {'class': 'qo7A2'}).get_text()

        if "새벽" in time_text: 
            time_text = time_text.replace("새벽 ", "")
            
        if "개천절" in time_text:
            time_text = time_text.replace("개천절", "")
        
        split_time = time_text.replace(" ","").split("-")
        
        if(len(split_time) < 2): continue
         
        open_time = split_time[0][0:5]
        closed_time = split_time[1][0:5]

        #요일별 영업시간 딕셔너리 생성
        business_hour_dict = {'open':open_time, 'closed':closed_time}
        
        if(day_text == '월'): 
            store_dict['businessHours']['onMon'] = business_hour_dict
        elif(day_text == '화'): 
            store_dict['businessHours']['onTue'] = business_hour_dict
        elif(day_text == '수'): 
            store_dict['businessHours']['onWed'] = business_hour_dict
        elif(day_text == '목'): 
            store_dict['businessHours']['onThu'] = business_hour_dict
        elif(day_text == '금'): 
            store_dict['businessHours']['onFri'] = business_hour_dict
        elif(day_text == '토'): 
            store_dict['businessHours']['onSat'] = business_hour_dict
        elif(day_text == '일'): 
            store_dict['businessHours']['onSun'] = business_hour_dict
        elif(day_text == '매일'):
            store_dict['businessHours']['onMon'] = business_hour_dict
            store_dict['businessHours']['onTue'] = business_hour_dict
            store_dict['businessHours']['onWed'] = business_hour_dict
            store_dict['businessHours']['onThu'] = business_hour_dict
            store_dict['businessHours']['onFri'] = business_hour_dict
            store_dict['businessHours']['onSat'] = business_hour_dict
            store_dict['businessHours']['onSun'] = business_hour_dict
            break
            
            
        
    json_list.append(store_dict)
    print(store_dict)

# 검색 결과가 없는 카페 출력
for store_name in not_exist:
    print(store_name)
    
#수집한 데이터로 json 파일 생성
# Json 파일
toJson(json_list)

    
    



