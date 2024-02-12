# clickfunktion.py
from selenium.common.exceptions import NoSuchElementException
from config import url_test_seite, find_by_xpath, driver, CahtGPT_API
import openai
import time



def clickfunktion():
   
    
        
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
    # print("Ergebnisse: ", ergebnisse)
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
    






