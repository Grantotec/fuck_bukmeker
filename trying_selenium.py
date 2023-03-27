import requests
import selenium
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC


def create_cond(by, name):
    return EC.element_to_be_clickable((by, name))

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://1xstavka.ru/line/football/")
wait = WebDriverWait(driver, 30)

menu = driver.find_element(By.CSS_SELECTOR, '#sports_left > div > div > div > div.assideCon > div:nth-child(1) > div > ul > li:nth-child(1) > div > ul:nth-child(6) > li > a > span.link__arrow.link-arrow > i')
hidden_submenu = driver.find_element(By.CSS_SELECTOR, '#sports_left > div > div > div > div.assideCon > div:nth-child(1) > div > ul > li:nth-child(1) > div > ul:nth-child(6) > li > ul > li:nth-child(1) > a > span.link__arrow.link-arrow > i')

actions = ActionChains(driver)
actions.move_to_element(menu)
actions.click(hidden_submenu)
actions.perform()
# wait.until(create_cond(By.XPATH,
#                        '//*[@id="sports_left"]/div/div/div/div[6]/div[1]/div/ul/li[1]/div/ul[6]/li/a/span[2]/i')
#            ).click()
time.sleep(200)
