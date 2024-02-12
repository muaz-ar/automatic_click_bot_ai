from selenium.common.exceptions import NoSuchElementException
from config import url_test_seite, find_by_xpath, driver
import time
import random

def clickfunktion():
    quiz_frage = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/span/p').text
    antworten = []

    for i in range(1, 6):
        xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{i}]/td[1]/label'
        try:
            antwort_element = find_by_xpath(xpath)
            antwort = antwort_element.text
            antworten.append(antwort)
        except NoSuchElementException:
            break



    # Bestimme die Anzahl der Antworten zufällig, basierend auf der Anzahl der verfügbaren Optionen
    if len(antworten) <= 3:
        ausgewaehlte_indices = random.sample(range(len(antworten)), 1, 2)
    else:
        ausgewaehlte_indices = random.sample(range(len(antworten)), random.randint(2, 3))

    for index in ausgewaehlte_indices:
        xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{index+1}]/td[1]/label'
        find_by_xpath(xpath).click()
        

    time.sleep(1)  # Kurze Pause, um das Klicken zu simulieren
    button_weiter = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/div[3]/span/input')
    button_weiter.click()
    print("Weiter zum nächsten Schritt...")


