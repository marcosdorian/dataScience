import PySimpleGUI as sg
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import csv
import os
import pandas as pd
import glob
import openai

""" 
This is a tool that searches the trends on Google, uses the AI to interpret the data and creates insights for the 
companies to help them increase their sales and get more leads for the commercial department.    
"""

# Defining layouts for the options
layoutRegion = [[sg.Text('Opção 1 - Region')]]
layoutState = [[sg.Text('Opção 2 - State')]]

sg.set_global_icon('logo-menor.ico')

# Defining main layout
layout = [
    [sg.Text('Escolha uma palavra-chave:'), sg.InputText(key='keyword')],
    [sg.Text('A busca pelo termo será:')],
    [sg.Radio('Por região', group_id='option', key='region'),
     sg.Radio('Por estado', group_id='option', key='state')],
    [sg.Text('Resultado:', font=('Arial', 12), size=(10, 1)), sg.Output(key='-OUTPUT-', font=('Arial', 12), size=(60, 20))],
    [sg.Button('Enviar'), sg.Button('Cancelar')]
]

# Creating the window
window = sg.Window('Redrive', layout)

# Main loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancelar':
        break
    elif event == 'Enviar':
        keyword = values['keyword']
        if values['region']:
            windowRegionStart = sg.Window('Opção 2', layoutRegion)
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome()
            driver.set_window_size(1024, 600)
            driver.maximize_window()
            driver.get("https://trends.google.com/trends/?geo=BR")

            wait = WebDriverWait(driver, 10)

            searchBox = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                   "/html/body/c-wiz/div/div[4]/div/c-wiz[1]/div/div[1]/div[3]/div/div/div[2]/div/label/input")))
            searchBox.click()
            sleep(1)
            searchBox.send_keys(keyword)
            searchBox.send_keys(Keys.RETURN)

            # It starts the search for region and creates the CSV file
            cookieButton = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/span[2]/a[2]")))
            if cookieButton:
                cookieButton.click()
                downloadButtonRegion = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))

                sleep(1)
                downloadButtonRegion.click()
            else:
                downloadButtonRegion = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))
                sleep(1)
                downloadButtonRegion.click()

            sleep(2)

            # It gets the CSV file and turns it into a TXT
            downloadPathRegion = r'C:\Users\marco\Downloads'
            latestFileRegion = max(glob.glob(os.path.join(downloadPathRegion + "/*.csv")), key=os.path.getctime)
            pathFileRegion = latestFileRegion

            driver.quit()

            with open(pathFileRegion, 'r') as arquivo_csv:
                leitor = csv.reader(arquivo_csv)
                linhas = list(leitor)

            with open('dfRegion.txt', 'w') as arquivo_txt:
                for linha in linhas:
                    arquivo_txt.write('\t'.join(linha))
                    arquivo_txt.write('\n')

            openai.organization = "org-ueUQwJLmlKxZ1qIpXqn9VyEL"
            openai.api_key = "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"
            openai.Model.list()
            # It reads the text and turns it into a variable
            with open(f"dfRegion.txt", "r", encoding="ISO-8859-1") as f:
                text = f.read()

            # It calls the function from the AI to read the documents and interpret the data
            def generate_text():
                completions = openai.Completion.create(
                    engine="text-davinci-002",
                    # prompt = f"Interprete os dados desta tabela e faça um texto explicando-os.\n{text}\n---\n",
                    prompt=f"Interprete os dados do Google Trends e crie 5 notificações sobre os dados,"
                           f"mostrando números e porcentagens das tendências.\n{text}\n---\n",
                    max_tokens=3500,
                    stop=None,
                    temperature=0.5,

                )
                message = completions.choices[0].text
                return message.strip()

            print(generate_text())

            def generate_insight():
                completions = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Analise os dados e crie um texto em Português para alavancar as vendas"
                           f"com base nas porcentagens das buscas.\n{text}\n---\n",
                    max_tokens=3500,
                    stop=None,
                    temperature=0.5,

                )
                message = completions.choices[0].text
                return message.strip()


            print(generate_insight())

            notes = generate_text()
            insight = generate_insight()

            # window['-OUTPUT-'].update("Noficações: " + '\n' + notes + "Dica: " + '\n' + insight)
            window['-OUTPUT-'].update("Notificações: \n" + notes + "\n\nDica: \n" + insight)

            while True:
                event, values = windowRegionStart.read()
                if event == sg.WIN_CLOSED:
                    break
            windowRegionStart.close()
        elif values['state']:
            stateSearch = sg.popup_get_text('Digite o nome do estado:')
            windowStateStart = sg.Window('Opção 2', layoutState)
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            driver = webdriver.Chrome()
            driver.set_window_size(1024, 600)
            driver.maximize_window()
            driver.get("https://trends.google.com/trends/?geo=BR")

            wait = WebDriverWait(driver, 10)

            # It seaches for the interest over time and creates the CSV files
            searchBox = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                   "/html/body/c-wiz/div/div[4]/div/c-wiz[1]/div/div[1]/div[3]/div/div/div[2]/div/label/input")))
            searchBox.click()
            sleep(1)
            searchBox.send_keys(keyword)
            searchBox.send_keys(Keys.RETURN)

            cookieButton = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/span[2]/a[2]")))
            if cookieButton:
                cookieButton.click()
                downloadButtonRegion = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))

                sleep(1)

                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)

                sleep(2)

                oneState = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                          "/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/hierarchy-picker[1]/ng-include/div[1]")))
                oneState.click()
                sleep(2)

                inputState = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                            "/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/hierarchy-picker[1]/ng-include/div[2]/md-autocomplete/md-autocomplete-wrap/input")))
                sleep(4)
                inputState.send_keys(stateSearch)
                inputStateButton = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                  "/html/body/md-virtual-repeat-container[1]/div/div[2]/ul/li/md-autocomplete-parent-scope/div/div/span[2]")))
                inputStateButton.click()
                sleep(4)

                downloadButtonRelated = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                       "/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))
                sleep(6)
                downloadButtonRelated.click()
                sleep(4)
            else:
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
                driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)

                sleep(2)

                oneState = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      "/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/hierarchy-picker[1]/ng-include/div[1]")))
                oneState.click()
                sleep(2)

                inputState = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        "/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/hierarchy-picker[1]/ng-include/div[2]/md-autocomplete/md-autocomplete-wrap/input")))
                sleep(2)
                inputState.send_keys(stateSearch)
                inputStateButton = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                              "/html/body/md-virtual-repeat-container[1]/div/div[2]/ul/li/md-autocomplete-parent-scope/div/div/span[2]")))
                inputStateButton.click()
                sleep(4)

                downloadButtonRelated = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                                   "/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))
                sleep(6)
                downloadButtonRelated.click()
                sleep(4)

            driver.quit()

            downloadPathRegion = r'C:\Users\marco\Downloads'
            latestFileRegion = max(glob.glob(os.path.join(downloadPathRegion + "/*.csv")), key=os.path.getctime)
            df = pd.read_csv(latestFileRegion, skiprows=1, encoding='UTF-8', header=1, delimiter=',')
            df.reset_index(inplace=True)
            df.rename(columns={'index': 'Palavras'}, inplace=True)

            if 'RISING' in df['Palavras'].values:
                # It finds the index with the line "RISING"
                risingIndex = df.loc[df['Palavras'] == 'RISING'].index[0]

                # It selects only lines that go until "RISING"
                df = df.iloc[:risingIndex]

            # It turns the CSV into TXT
            with open(stateSearch + '.txt', 'w') as f:
                f.write(df.to_csv(index=True, header=True, sep='\t'))

            sleep(1)

            openai.organization = "org-ueUQwJLmlKxZ1qIpXqn9VyEL"
            openai.api_key = "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"
            openai.Model.list()
            # It reads the file and stores it in a variable
            with open(f"{stateSearch}.txt", "r", encoding="ISO-8859-1") as f:
                text = f.read()



            # It calls the function with the AI to read and interpret the data
            def generate_text():
                completions = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Interprete os dados do Google Trends e crie 5 notificações em Português sobre os dados,"
                           f"mostrando porcentagens das tendências.\n{text}\n---\n",
                    max_tokens=3500,
                    stop=None,
                    temperature=0.5,

                )
                message = completions.choices[0].text
                return message.strip()


            print(generate_text())


            def generate_insight():
                completions = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=f"Crie um texto dando uma ideia de como alavancar"
                               f"as vendas para as empresas com base nos números e porcentagens analisados"
                               f"em português.\n{text}\n---\n",
                    max_tokens=3500,
                    stop=None,
                    temperature=0.5,

                )
                message = completions.choices[0].text
                return message.strip()


            print(generate_insight())

            notes = generate_text()
            insight = generate_insight()

            # window['-OUTPUT-'].update("Noficações: " + '\n' + notes + "Dica: " + '\n' + insight)
            window['-OUTPUT-'].update("Notificações: \n" + notes + "\n\nDica: \n" + insight)

            while True:
                event, values = windowStateStart.read()
                if event == sg.WIN_CLOSED:
                    break
            windowStateStart.close()

window.close()


