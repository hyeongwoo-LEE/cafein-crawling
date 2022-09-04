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
    
# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(browser, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        browser.quit()
    return wait

query = '투썸 명동사거리점'

browser.get("https://m.search.naver.com/search.naver?query="+query)
time.sleep(0.5)

browser.find_element(By.XPATH, '//*[@id="place-main-section-root"]/div/div[3]/div/ul/li[2]/div/a/div/div').click()
a = browser.find_element(By.XPATH, '//*[@id="_title"]/a/span[1]').text

soup = BeautifulSoup(browser.page_source, 'html.parser')

span_tags = soup.find_all("span", {'class':'ob_be'})

print(browser.find_element(By.XPATH, '//*[@id="_title"]/a/span[1]').text)
for span_tag in span_tags:
    
    day_text = span_tag.find("span", {'class':'kGc0c'})
    time_text = span_tag.find("div", {'class': 'qo7A2'})
    print(day_text.get_text(),": ", time_text.get_text())
    
    



