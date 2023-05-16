from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import csv
import os
import glob
import openai
from datetime import datetime, timedelta

searchTerm = "Páscoa"

options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome()
driver.set_window_size(1024, 600)
driver.maximize_window()
driver.get("https://trends.google.com/trends/?geo=BR")

wait = WebDriverWait(driver, 10)

# searching for the term per region
searchBox = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/c-wiz/div/div[4]/div/c-wiz[1]/div/div[1]/div[3]/div/div/div[2]/div/label/input")))
searchBox.click()
searchBox.send_keys(searchTerm)
searchBox.send_keys(Keys.RETURN)

cookieButton = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/span[2]/a[2]")))
if cookieButton:
    cookieButton.click()

downloadButtonRegion = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      "/html/body/div[2]/div[2]/div/md-content/div/div/div[2]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))

sleep(1)
downloadButtonRegion.click()

sleep(2)

# it saves the latest downloaded document for the region
downloadPathRegion = r'C:\Users\marco\Downloads'
latestFileRegion = max(glob.glob(os.path.join(downloadPathRegion + "/*.csv")), key=os.path.getctime)
pathFileRegion = latestFileRegion

with open(pathFileRegion, 'r') as regionCsv:
    reader = csv.reader(regionCsv)
    lines = list(reader)

with open('dfRegion.txt', 'w') as regionTxt:
    for line in lines:
        regionTxt.write('\t'.join(line))
        regionTxt.write('\n')

# it calls the chatGPT and delivers the api key
openai.organization = "org-ueUQwJLmlKxZ1qIpXqn9VyEL"
openai.api_key = "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"
openai.Model.list()

# It reads the text and turns it into a variable
with open(f"dfRegion.txt", "r", encoding="ISO-8859-1") as f:
    regionText = f.read()

# It starts and calls the function from the AI to read "dfRegion" and interpret the data
def generate_text():
    completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Interprete os dados do Google Trends.\n{regionText}\n---\n",
    max_tokens=3500,
    stop=None,
    temperature=0.5,

)
    message = completions.choices[0].text
    return message.strip()

print(generate_text())

# It starts and calls the function from the AI to read "dfRegion" to generate the insights
def generate_insight():
    completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Analise os dados e crie 5 insights com base na busca para alavancar as vendas.\n{regionText}\n---\n",
    max_tokens=3500,
    stop=None,
    temperature=0.5,

)
    message = completions.choices[0].text
    return message.strip()

print(generate_insight())

# it scrolls up the page to find the "state" button
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)

sleep(2)

# it goes for the specific state
stateSearch = "São Paulo"

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
sleep(2)

downloadButtonRelated = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                       "/html/body/div[2]/div[2]/div/md-content/div/div/div[4]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]/i")))
sleep(2)
downloadButtonRelated.click()
sleep(2)

# it saves the latest downloaded documento for the state
downloadPathRegion = r'C:\Users\marco\Downloads'
latestFileRegion = max(glob.glob(os.path.join(downloadPathRegion + "/*.csv")), key=os.path.getctime)
pathFileRegion = latestFileRegion

with open(pathFileRegion, 'r') as stateCsv:
    reader = csv.reader(stateCsv)
    lines = list(reader)

with open(stateSearch + '.txt', 'w') as stateTxt:
    for line in lines:
        stateTxt.write('\t'.join(line))
        stateTxt.write('\n')

# it reads the TXT
with open(f"{stateSearch}.txt", "r", encoding="ISO-8859-1") as f:
    stateText = f.read()

# It starts and calls the function from the AI to read "dfRegion" and interpret the data
def generate_text():
    completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Interprete os dados do Google Trends.\n{stateText}\n---\n",
    max_tokens=3500,
    stop=None,
    temperature=0.5,
)

    message = completions.choices[0].text
    return message.strip()

print(generate_text())

# It starts and calls the function from the AI to read "dfState" to generate the insights
def generate_insight():
    completions = openai.Completion.create(
    engine="text-davinci-002",
    prompt=f"Analise os dados e crie 5 insights com base na busca para alavancar as vendas.\n{stateText}\n---\n",
    max_tokens=3500,
    stop=None,
    temperature=0.5,
)

    message = completions.choices[0].text
    return message.strip()

print(generate_insight())

driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)

# it creates a time zone to search for the trends monthly in a range of 2 years
firstDate = datetime(2021, 1, 1)
lastDate = datetime(2023, 1, 1)
searchRange = timedelta(days=31)

while firstDate < lastDate:
    # it clicks on the date button
    dateButton = wait.until(EC.presence_of_element_located(
        (By.XPATH, "/html/body/div[2]/div[2]/div/header/div/div[3]/ng-transclude/div[2]/div/div/custom-date-picker")))
    dateButton.click()
    sleep(1)
    # it chooses the personalized date
    personalizedDate = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#select_option_22")))
    personalizedDate.click()
    # it clears and chooses the starting date
    buttonFrom = wait.until(EC.presence_of_element_located((By.XPATH,
                                                            "/html/body/div[2]/div[4]/md-dialog/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/md-content/form/div[1]/md-datepicker/div[1]/input")))
    buttonFrom.clear()
    buttonFrom.send_keys(firstDate.strftime("%m/%d/%Y"))
    sleep(1)
    buttonFrom.send_keys(Keys.RETURN)
    # it chooses the ending date
    buttonTo = wait.until(EC.presence_of_element_located((By.XPATH,
                                                          "/html/body/div[2]/div[4]/md-dialog/md-tabs/md-tabs-content-wrapper/md-tab-content[1]/div/md-content/form/div[2]/md-datepicker/div[1]/input")))
    buttonTo.clear()
    buttonTo.send_keys((firstDate + searchRange).strftime("%m/%d/%Y"))
    sleep(1)
    buttonTo.send_keys(Keys.RETURN)

    okButton = wait.until(
        EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/md-dialog/md-dialog-actions/button[2]")))
    okButton.click()
    sleep(3)

    downloadButtonTime = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                    "/html/body/div[2]/div[2]/div/md-content/div/div/div[1]/trends-widget/ng-include/widget/div/div/div/widget-actions/div/button[1]")))
    downloadButtonTime.click()
    sleep(3)

    # it saves the files
    downloadPathTime = r'C:\Users\marco\Downloads'
    csvFiles = glob.glob(os.path.join(downloadPathTime, "*.csv"))

    # it joins all the files in one
    answers = []

    for csvFile in csvFiles:
        with open(csvFile, 'r') as file:
            reader = csv.reader(file)
            lines = list(reader)

        fileName = os.path.splitext(csvFile)[0] + ".txt"
        with open(fileName, 'w') as file:
            for line in lines:
                file.write('\t'.join(line))
                file.write('\n')

        with open(fileName, 'r') as file:
            content = file.read()

        # it calls the chatGPT to interpret the data of all files together
        answer = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Com base nas datas da lista, indique qual é o dia da semana que mais se repete com o maior"
                   f"número de pesquisas",
            max_tokens=3500,
            n=1,
            stop=None,
            temperature=0.7
        )

        fileResult = os.path.splitext(csvFile)[0] + "_resultado.txt"
        with open(fileResult, 'w') as results:
            results.write(answer.choices[0].text.strip())

        answers.append(answer.choices[0].text.strip())

    # it makes the process restart until the last day is reached
    firstDate = firstDate + timedelta(days=31)
    print("Next sequence of dates:", firstDate.strftime("%m/%d/%Y"), "-",
          (firstDate + searchRange).strftime("%m/%d/%Y"))

    # it brings all the info together
    finalResult = "\n".join(answers)
    finalFile = os.path.join(downloadPathTime, "final_result.txt")
    with open(finalFile, 'w') as finalResultFile:
        finalResultFile.write(finalResult)

# it starts and calls the function so chatGPT can interpret the data and bring insights based on it.
def insight_trends():
    with open(finalFile, 'r') as finalResultFile:
        trendsFile = finalResultFile.read()

    resposta = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Analise os dados e diga qual é o dia da semana que mais se repete. Crie 5 insights para"
               f"alavancar as vendas para {searchTerm}\n{trendsFile}\n---\n",
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.7
    )

    return resposta.choices[0].text.strip()

print(insight_trends())


