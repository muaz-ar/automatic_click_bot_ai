from selenium.common.exceptions import NoSuchElementException
from config import url_test_seite, find_by_xpath, driver, CahtGPT_API
import openai
import time
import random
from datetime import datetime, timedelta

letzter_gueltiger_versuch = datetime.now() - timedelta(seconds=20)  # Erlaubt sofortige Anfrage

def clickfunktion():
    global letzter_gueltiger_versuch
    jetzt = datetime.now()

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

    def question(*args):
        return f"Frage: {quiz_frage}\nAntwortmöglichkeiten:\n" + "\n".join(args)

    if jetzt - letzter_gueltiger_versuch >= timedelta(seconds=20):
        print("Stelle eine neue GPT-Anfrage...")
        openai.api_key = CahtGPT_API
        frage = question(*antworten)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": frage}]
            )
            responses = response['choices'][0]['message']['content'].strip().split('\n')
            ergebnisse = [antwort for antwort in responses if antwort.strip().lower() in ["ja", "nein"]]
            if not ergebnisse:  # Keine gültigen Antworten
                raise Exception("Keine gültigen Antworten erhalten.")
            letzter_gueltiger_versuch = jetzt  # Erfolgreiche Anfrage
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten oder keine gültigen Antworten: {e}")
            ergebnisse = []
    else:
        print("Wartezeit noch nicht abgelaufen, verwende zufällige Auswahl...")
        ergebnisse = []

    if not ergebnisse:
        print("Führe zufällige Auswahl durch...")
        ausgewaehlte_indices = random.sample(range(len(antworten)), 1 if len(antworten) <= 3 else random.randint(2, 3))
        for index in ausgewaehlte_indices:
            xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{index+1}]/td[1]/label'
            find_by_xpath(xpath).click()
    else:
        print("Verarbeite GPT-3 Ergebnisse...")
        for i, ergebnis in enumerate(ergebnisse):
            if ergebnis.lower() == 'ja':
                xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{i+1}]/td[1]/label'
                find_by_xpath(xpath).click()

    time.sleep(1)  # Kurze Pause, um das Klicken zu simulieren
    button_weiter = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/div[3]/span/input')
    button_weiter.click()

