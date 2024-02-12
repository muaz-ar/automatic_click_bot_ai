from selenium.common.exceptions import NoSuchElementException
from config import url_test_seite, find_by_xpath, driver, CahtGPT_API
import openai
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

    def question(*args):
        meine_frage = "Frage: " + quiz_frage + "\nAntwortmöglichkeiten:\n" + "\n".join(args) + "\nBitte antworte mit 'Ja' oder 'Nein' auf jede der obigen Optionen ausschließlich zeilenweise. Es ist immer eine Option richtig. Aus diesem Grund muss mindestens eine Option mit 'Ja' beantwortet werden. Keine weiteren Kommentare oder Erläuterungen hinzufügen."
        return meine_frage 

    openai.api_key = CahtGPT_API
    def chat(prompt):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[{"role": "user", "content": prompt}]
            )
            responses = response['choices'][0]['message']['content'].strip().split('\n')
            gefilterte_antworten = [antwort for antwort in responses if antwort.strip().lower() in ["ja", "nein"]]
            return gefilterte_antworten
        except Exception as e:
            print(f"Ein Fehler ist aufgetreten: {e}")
            return []

    frage = question(*antworten)
    ergebnisse = chat(frage)
    time.sleep(1)

    ergebnisse_zeilen = []  # Definiere ergebnisse_zeilen vor der if-Bedingung
    if not ergebnisse or ergebnisse[0] == '.':
        print("Keine Ergebnisse erhalten oder ungültiges Ergebnis. Führe zufällige Auswahl durch.")
        ausgewaehlte_indices = random.sample(range(len(antworten)), 1 if len(antworten) <= 3 else random.randint(2, 3))
        for index in ausgewaehlte_indices:
            ergebnisse_zeilen.append('ja')  # Füge 'ja' für jede zufällig ausgewählte Antwort hinzu
    else:
        ergebnisse_zeilen = ergebnisse

    for i, ergebnis in enumerate(ergebnisse_zeilen):
        if ergebnis.lower() == 'ja':
            xpath = f'/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{i+1}]/td[1]/label'
            find_by_xpath(xpath).click()
            time.sleep(1)

    time.sleep(2)
    button_weiter = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/div[3]/span/input')
    button_weiter.click()
