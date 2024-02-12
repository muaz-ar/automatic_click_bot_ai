from selenium.common.exceptions import NoSuchElementException
from config import url_test_seite, find_by_xpath, driver, CahtGPT_API
import openai
import time
import random
from datetime import datetime, timedelta

letzter_gueltiger_versuch = datetime.now() - timedelta(seconds=20)  # Startwert setzen, um die erste Anfrage sofort zu ermöglichen

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
        try:
            frage = question(*antworten)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": frage}]
            )
            responses = response['choices'][0]['message']['content'].strip().split('\n')
            ergebnisse = [antwort for antwort in responses if antwort.strip().lower() in ["ja", "nein"]]
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            ergebnisse = []
    else:
        ergebnisse = []
        print("Verwende zufällige Auswahl aufgrund von Rate-Limit...")

    if not ergebnisse:
        print("Keine Ergebnisse erhalten oder Rate-Limit erreicht. Führe zufällige Auswahl durch.")
        letzter_gueltiger_versuch = jetzt  # Aktualisiere den Zeitpunkt des letzten gültigen Versuchs
        ausgewaehlte_indices = random.sample(range(len(antworten)), 1 if len(antworten) <= 3 else random.randint(2, 3))
        for index in ausgewaehlte_indices:
            xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{index+1}]/td[1]/label'
            find_by_xpath(xpath).click()
    else:
        print("Verarbeite GPT-3 Ergebnisse...")
        letzter_gueltiger_versuch = jetzt  # Aktualisiere den Zeitpunkt des letzten gültigen Versuchs
        for i, ergebnis in enumerate(ergebnisse):
            if ergebnis.lower() == 'ja':
                xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{i+1}]/td[1]/label'
                find_by_xpath(xpath).click()

    # Kurze Pause vor dem Weiterklicken, um das menschliche Verhalten zu simulieren und der Seite Zeit zum Laden zu geben
    time.sleep(1)  
    button_weiter = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/div[3]/span/input')
    button_weiter.click()

# Denke daran, die Funktion clickfunktion() irgendwo in deinem Code aufzurufen, wo es passt.
 