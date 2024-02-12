from test import clickfunktion
from config import url_test_seite, driver, find_by_xpath 
import time

def click_save_loop():
    counter = 0
    while counter < 50:  # Gesamtzahl der Durchläufe
        driver.get(url_test_seite)
        for _ in range(10):  # Führe clickfunktion() 10 Mal aus
            clickfunktion()
        
        # Nach 10 Durchläufen der clickfunktion(), führe zusätzliche Aktionen aus
        save_result = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/div[2]/table/tbody/tr/td[1]/a')
        save_result.click()
        print("Counter: click speichern", counter)
        
        counter += 1  # Zähler für die Gesamtanzahl der Durchläufe
