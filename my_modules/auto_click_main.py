from random_answer import clickfunktion
from selenium.common.exceptions import NoSuchElementException
from config import url_test_seite, find_by_xpath, driver
import time

def click_save_loop():
    counter = 0
    while counter < 150:  # Gesamtzahl der Durchläufe
        driver.get(url_test_seite)
        for _ in range(10):  # Führe clickfunktion() 10 Mal aus
            clickfunktion()
        
        try:
            save_result = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/div[2]/table/tbody/tr/td[1]/a')
            save_result.click()
            print("Counter: click speichern", counter)
            counter += 1  # Zähler für die Gesamtanzahl der Durchläufe nur erhöhen, wenn der Button gefunden wurde
        except NoSuchElementException:
            print("Button 'save_result' nicht gefunden, versuche erneut...")
            time.sleep(1)  # Kurze Pause, bevor der Versuch wiederholt wird, um eventuelle Ladezeiten zu berücksichtigen
            continue  # Startet die while-Schleife erneut ohne den Counter zu erhöhen

