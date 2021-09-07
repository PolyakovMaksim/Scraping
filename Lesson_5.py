from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time
from pymongo import MongoClient


client = MongoClient('127.0.0.1', 27017)
db = client['Mail']
mail = db.mail

chrome_options = Options()
chrome_options.add_argument("--window-size=760,1248")

driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=chrome_options)
driver.get('https://mail.ru/?from=logout')

login_input = driver.find_element_by_xpath("//input [@data-testid = 'login-input']")
login_input.send_keys('study.ai_172@mail.ru')
login_input.send_keys(Keys.ENTER)
time.sleep(0.5)

password_input = driver.find_element_by_xpath("//input [@data-testid = 'password-input']")
password_input.send_keys('NextPassword172???')
password_input.send_keys(Keys.ENTER)
time.sleep(5)

link_list = []
link_mess_list = []
link_heading_list = []
sender_list = []
date_list = []
links = driver.find_elements_by_xpath("//div[@class = 'dataset__items']/a[contains(@href, '/inbox/')]")

for link in links:
    new_element = link.get_attribute('href')
    link_list.append(new_element)

actions = ActionChains(driver)
actions.move_to_element(links[-1])
actions.perform()

while True:

    wait = WebDriverWait(driver, 5)
    links = driver.find_elements_by_xpath("//div[@class = 'dataset__items']/a[contains(@href, '/inbox/')]")

    new_list = []
    for link in links:
        new_element = link.get_attribute('href')
        new_list.append(new_element)

    if new_list[-1] == link_list[-1]:
        break
    else:
        for el in new_list:
            link_list += new_list

    actions = ActionChains(driver)
    actions.move_to_element(links[-1])
    actions.perform()

final_list = list(set(link_list))

for mess in final_list:
    driver.get(mess)
    time.sleep(1.5)
    heading = driver.find_element_by_class_name('thread__subject').text
    sender = driver.find_element_by_class_name('letter-contact').text
    date = driver.find_element_by_class_name('letter__date').text

    mail.insert_one({'Heading' : heading, 'Sender' : sender, 'Date' : date, 'Link' : mess})

driver.quit()
