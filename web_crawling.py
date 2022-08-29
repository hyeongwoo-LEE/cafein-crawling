from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options)


browser.get("https://www.naver.com/")

time.sleep(500)
