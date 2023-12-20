import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd


r_options = Options()
r_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=r_options)
driver.get("https://www.thefantasyfootballers.com/")
#Player_name = "Lamb, Ceedee"
with open('contqbfantasytrain.csv', 'w') as f:
            f.write("SEASON,TEAM,GP,GS,PTS,PPG,SNP%,CMP,ATT,CMP%,YDS,Y/A,TD,TD%,INT,SCK,QB RT,ATT,YDS,Y/A,LNG,TD,FUM"+'\n')
'''driver.get('https://www.google.com')
driver.get('https://www.footballdb.com/players/current.html?pos=WR');


namesearches = driver.find_elements(By.CLASS_NAME,"tr ")
for name in namesearches:
    time.sleep(5)
    beeb = name.text.split()
    bong = ''.join(beeb[:2])
    Player_name = bong
    try:
        driver.switch_to.new_window('tab')
        driver.get("https://www.google.com")
        search = driver.find_element(By.ID,"APjFqb")
        search.send_keys(Player_name+ " 'thefantasyfootballers.com'")
        search.send_keys(Keys.RETURN)
        time.sleep(5)
        search2 = driver.find_element(By.PARTIAL_LINK_TEXT,"https://www.thefantasyfootballers.com")
        search2.click()
        search3 = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[4]/section/div[2]/div[3]/div[1]/ul/li[2]")
        search3.click()
        time.sleep(5)
        search4 = driver.find_element(By.ID, "scoring")
        drop = Select(search4)
        drop.select_by_value("ppr-four")
        time.sleep(5)
        search5 = driver.find_element(By.CLASS_NAME,"ffb-pp--data")
        data = search5.text
        lines = data.split('\n')
        lines_to_remove =  ["SEASON TEAM GP RNK PTS PPG SNP% TGT REC CTCH% YDS Y/C LNG TD ATT YDS Y/A LNG TD FUM", "Fantasy Receiving Rushing",]
        filtered_lines = [line for line in lines if line not in lines_to_remove]
        combined_lines = []
        for i in range(0, len(filtered_lines), 2):
            if i + 1 < len(filtered_lines):
                combined_lines.append(filtered_lines[i] + ' ' + filtered_lines[i+1])
            else:
                combined_lines.append(filtered_lines[i])
        
        resulta = combined_lines[:-1]
        csv_lines = []
        for lpine in resulta:
            parts = lpine.split()
            csv_line = ','.join(parts)  # Join the parts with a comma
            csv_lines.append(csv_line)

        csv_content = '\n'.join(csv_lines)

        with open('WRFANTASYTRAIN.csv', 'a') as f:
            f.write(csv_content+"\n")
        print(csv_content)
    except selenium.common.exceptions.NoSuchElementException:
        pass
    driver.close()
    driver.switch_to.window(driver.window_handles[0])'''

names = []

with open('contqbnames.csv', 'r') as file:
    for line in file:
        names.append(line.strip())

for name in names:
    Player_name = name
    try:
        time.sleep(3)
        search = driver.find_element(By.NAME,"player")
        search.send_keys(Player_name)
        time.sleep(2)
        search.send_keys(Keys.RETURN)
        search3 = driver.find_element(By.XPATH, "/html/body/div[1]/main/div/div[4]/section/div[2]/div[3]/div[1]/ul/li[2]")
        search3.click()
        search4 = driver.find_element(By.ID, "scoring")
        drop = Select(search4)
        drop.select_by_value("ppr-four")
        time.sleep(3)
        search5 = driver.find_element(By.CLASS_NAME,"ffb-pp--data")
        time.sleep(2)
        data = search5.text
        time.sleep(2)
        lines = data.split('\n')
        lines_to_remove =  ["SEASON TEAM GP GS RNK PTS PPG SNP% CMP ATT CMP% YDS Y/A TD	TD%	INT	SCK	QB RT ATT YDS Y/A LNG TD FUM SEASON TEAM GP GS RNK PTS PPG SNP% CMP ATT CMP% YDS Y/A TD	TD%	INT	SCK	QB RT ATT YDS Y/A LNG TD FUM", "Fantasy Passing Rushing",]
        filtered_lines = [line for line in lines if line not in lines_to_remove]
        combined_lines = []
        for i in range(0, len(filtered_lines), 2):
            if i + 1 < len(filtered_lines):
                combined_lines.append(filtered_lines[i] + ' ' + filtered_lines[i+1])
            else:
                combined_lines.append(filtered_lines[i])
        
        resulta = combined_lines[:-1]
        csv_lines = []
        for lpine in resulta:
            parts = lpine.split()
            csv_line = ','.join(parts)  # Join the parts with a comma
            csv_lines.append(csv_line)

        csv_content = '\n'.join(csv_lines)

        with open('contqbfantasytrain.csv', 'a') as f:
            f.write(csv_content+"\n")
        print(csv_content)
    except selenium.common.exceptions.NoSuchElementException:
        print("ERROR")
        pass
driver.quit()
