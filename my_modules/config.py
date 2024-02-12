# setup.py
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

load_dotenv()

USER = os.getenv('USER')
KEY = os.getenv('KEY')
CahtGPT_API = os.getenv('CahtGPT_API')

options = Options()
options.add_argument('-no-remote')
options.add_argument('-foreground')
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'

driver = webdriver.Firefox(service=Service(r'C:\Users\md-ar\OneDrive\Desktop\python_projekts\ai_click_bot\driver\geckodriver.exe'), options=options)
url_test_seite = "https://internet.partnerportal-deutschepost.de/verkaufsunterstuetzung/lernen/check-starten/kompetenzcheck.html?tx_ptcertification_questionnaire%5Baction%5D=init&tx_ptcertification_questionnaire%5Bcategory%5D=12&tx_ptcertification_questionnaire%5Bcontroller%5D=Questionnaire&tx_ptcertification_questionnaire%5BcsrfToken%5D=cf12f16d608b4232d37aaf6e7c9b987374fffee7&tx_ptcertification_questionnaire%5BmainPid%5D=124&cHash=e490131c452aacba80a0802658db67b4"

def find_by_xpath(xpath):
    return driver.find_element(By.XPATH, xpath)