from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from config import url_test_seite, driver
import time
import random

def clickfunktion():
    quiz_frage_xpath = '/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/span/p'
    antworten_xpath_template = '/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{}]/td[1]/label'

    try:
        quiz_frage = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, quiz_frage_xpath))).text
        antworten = []

        for i in range(1, 6):
            xpath = antworten_xpath_template.format(i)
            try:
                antwort_element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.XPATH, xpath)))
                antworten.append(antwort_element.text)
            except TimeoutException:
                break

        if len(antworten) <= 3:
            ausgewaehlte_indices = random.sample(range(len(antworten)), 1)
        else:
            ausgewaehlte_indices = random.sample(range(len(antworten)), random.randint(2, 3))

        for index in ausgewaehlte_indices:
            xpath = antworten_xpath_template.format(index + 1)
            WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath))).click()


        
        button_weiter_xpath = '/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/div[3]/span/input'
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, button_weiter_xpath))).click()

    except Exception as e:
        print(f"Fehler beim Ausführen der clickfunktion: {e}")
