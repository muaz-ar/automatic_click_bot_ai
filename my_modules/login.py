# login.py
from selenium.webdriver.common.by import By
from config import driver, USER, KEY
from selenium.common.exceptions import NoSuchElementException

url_login = 'https://internet.partnerportal-deutschepost.de/login.html'
url_test_seite = "https://internet.partnerportal-deutschepost.de/verkaufsunterstuetzung/lernen/check-starten/kompetenzcheck.html?tx_ptcertification_questionnaire%5Baction%5D=init&tx_ptcertification_questionnaire%5Bcategory%5D=12&tx_ptcertification_questionnaire%5Bcontroller%5D=Questionnaire&tx_ptcertification_questionnaire%5BcsrfToken%5D=cf12f16d608b4232d37aaf6e7c9b987374fffee7&tx_ptcertification_questionnaire%5BmainPid%5D=124&cHash=e490131c452aacba80a0802658db67b4"


def login():
    driver.get(url_login)
    user_bar = driver.find_element(By.XPATH, '//*[@id="loginUser"]')
    user_bar.send_keys(USER)
    key_bar = driver.find_element(By.XPATH, '//*[@id="loginPlaintextPassword"]')
    key_bar.send_keys(KEY)
    button_login = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/main/div[4]/div/form/fieldset/div[3]/input')
    button_login.click()
    def click_button_if_exists(xpath):
        try:
            button = driver.find_element(By.XPATH, xpath)
            button.click()
        except NoSuchElementException:
            pass
    click_button_if_exists('/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/form/div[2]/span[2]/input')
    click_button_if_exists('/html/body/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/form/div[2]/span[2]/input')
    

    

