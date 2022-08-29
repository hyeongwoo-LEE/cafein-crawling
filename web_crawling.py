from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import json

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

browser.get("https://map.naver.com/")

time.sleep(5)

# css를 찾을때 까지 10초 대기
time_wait(10, 'div.input_box > input.input_search')

keyword = "투썸 명동사거리점"

browser.find_element('xpath','//*[@id="search-input"]').clear()
browser.find_element('xpath','//*[@id="search-input"]').send_keys(keyword)
browser.find_element('xpath','//*[@id="header"]/div[1]/fieldset/button').click()

# 검색창 찾기
search = browser.find_element_by_css_selector('div.input_box > input.input_search')
search.send_keys(keyword)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

res = browser.page_source  # 페이지 소스 가져오기
soup = BeautifulSoup(res, 'html.parser')  # html 파싱하여  가져온다