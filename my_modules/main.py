from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os 
from dotenv import load_dotenv
load_dotenv()

USER = os.getenv('USER')
KEY = os.getenv('KEY')

options = Options()
options.add_argument('-no-remote')
options.add_argument('-foreground')
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(service=Service(r'C:\Users\md-ar\OneDrive\Desktop\python_projekts\ai_click_bot\driver\geckodriver.exe'), options=options)
url_login = 'https://internet.partnerportal-deutschepost.de/login.html'
url_test_seite = "https://internet.partnerportal-deutschepost.de/verkaufsunterstuetzung/lernen/check-starten/kompetenzcheck.html?tx_ptcertification_questionnaire%5Baction%5D=init&tx_ptcertification_questionnaire%5Bcategory%5D=12&tx_ptcertification_questionnaire%5Bcontroller%5D=Questionnaire&tx_ptcertification_questionnaire%5BcsrfToken%5D=cf12f16d608b4232d37aaf6e7c9b987374fffee7&tx_ptcertification_questionnaire%5BmainPid%5D=124&cHash=e490131c452aacba80a0802658db67b4"

def get_driver(x):
    return driver.get(x)

get_driver(url_login)

def find_by_xpath(xpath):
    return driver.find_element(By.XPATH, xpath)

user_bar = find_by_xpath('//*[@id="loginUser"]')

user_bar.send_keys(USER)

key_bar = find_by_xpath('//*[@id="loginPlaintextPassword"]')
key_bar.send_keys(KEY)


button_login = find_by_xpath('/html/body/div[1]/div/div/main/div[4]/div/form/fieldset/div[3]/input')
button_login.click()

def click_button_if_exists(xpath):
    try:
        button = driver.find_element(By.XPATH, xpath)
        button.click()
    except NoSuchElementException:
        pass


click_button_if_exists('/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/form/div[2]/span[2]/input')
click_button_if_exists('/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/form/div[2]/span[2]/input')

driver.get(url_test_seite)

#frage = find_by_xpath()