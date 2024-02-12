from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os 
from dotenv import load_dotenv
import openai 
import time 
load_dotenv()

USER = os.getenv('USER')
KEY = os.getenv('KEY')
CahtGPT_API = os.getenv('CahtGPT_API')
openai.api_key = CahtGPT_API

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

counter = 0

def clickfunktion():
    global counter
    while True:
        
        quiz_frage = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/span/p').text

        antworten = []

        for i in range(1, 6):
            xpath = '/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{}]/td[1]/label'.format(i)
            try:
                antwort_element = find_by_xpath(xpath)
                antwort = antwort_element.text
                antworten.append(antwort)
            except NoSuchElementException:
                break

        # Die einzelnen Zeilen in Variablen speichern 
            antwort_1 = antworten[0] if len(antworten) >= 1 else ""
            antwort_2 = antworten[1] if len(antworten) >= 2 else ""
            antwort_3 = antworten[2] if len(antworten) >= 3 else ""
            antwort_4 = antworten[3] if len(antworten) >= 4 else ""
            antwort_5 = antworten[4] if len(antworten) >= 5 else ""

        

        def question(quiz_frage, antwort_1, antwort_2, antwort_3, antwort_4, antwort_5):
            meine_frage = "Frage : " + quiz_frage + "\n"
            meine_frage += "\nAntwortmöglichkeiten:\n" + "\n".join(antworten)
            meine_frage += "\nBitte antworte mit 'Ja' oder 'Nein' auf jede der obigen Optionen ausschlieslich zeilenweise." 
            meine_frage += "Es ist immer eine Option richtig. ausdemgrund muss mindestens eine Option mit 'Ja' beantwortet werden. "
            meine_frage += "Keine weiteren Kommentare oder Erläuterungen hinzufügen."
        

            return meine_frage 
                
                
        
        # Stelle sicher, dass openai.api_key zu Beginn deines Skripts oder vor dem API-Aufruf gesetzt wird
        openai.api_key = CahtGPT_API

        def chat(prompt):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0125", # Aktualisieren Sie dies entsprechend Ihrem gewünschten Modell, z.B. auf ein GPT-4 Modell, falls verfügbar und gewünscht
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                # Die Annahme hier ist, dass die Antwort in einem Format zurückgegeben wird, das direkt verwendet werden kann.
                # Dies könnte je nach Ihrer spezifischen Anforderung variieren.
                responses = response['choices'][0]['message']['content'].strip().split('\n')
                
                # Filtern, um nur "ja" oder "nein" zu behalten
                gefilterte_antworten = [antwort for antwort in responses if antwort.strip().lower() in ["ja", "nein"]]
                
                return gefilterte_antworten
            except Exception as e:
                print(f"Ein Fehler ist aufgetreten: {e}")
                return []
        
        # Beispiel für die Verwendung der angepassten Funktion
        frage = question(quiz_frage, antwort_1, antwort_2, antwort_3, antwort_4, antwort_5)
        ergebnisse = chat(frage)
        print("Ergebnisse: ", ergebnisse)
        time.sleep(18)
        ergebnisse_zeilen = []
        
        if len(ergebnisse) > 0 and ergebnisse[0] != '.':
            for ergebnis in ergebnisse:
                ergebnisse_zeilen.extend(ergebnis.strip().split("\n"))
        else:
            print("Keine Ergebnisse erhalten oder ungültiges Ergebnis.")
                
        
        

        def execute_command_based_on_answer(answer, zeilennummer):
            if answer.lower() == 'ja':
                # Führe den Befehl aus, wenn die Antwort "ja" ist
                xpath = '/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/table/tbody/tr[{}]/td[1]/label'.format(zeilennummer)
                element = find_by_xpath(xpath)
                element.click()
            elif answer.lower() == 'nein':
                # Führe keinen Befehl aus, wenn die Antwort "nein" ist
                pass

        time.sleep(2)
    

        for i, ergebnis in enumerate(ergebnisse_zeilen):
            # print(f"Antwort für Zeile {i+1}: {ergebnis}")
            execute_command_based_on_answer(ergebnis, i+1)
        
        time.sleep(2)
        button_weiter = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/form/div[3]/span/input')
        button_weiter.click()     
        
        counter += 1

        # Überprüfen, ob der Zähler neun erreicht hat
        if counter == 10:
            break

print("Counter: ", counter)


counter1 = 0
while True:    
    clickfunktion()
    save_result = find_by_xpath('/html/body/div[1]/div/div/main/div/div[1]/div[1]/div/div[2]/table/tbody/tr/td[1]/a')
    save_result.click()
    print("Counter: click speichern", counter1)
    time.sleep(3)
    driver.get(url_test_seite)
    counter += 1
    if counter1 == 50:
        break
