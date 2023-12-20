#RB MAIN
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.svm import SVR
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

r_options = Options()
r_options.add_experimental_option('detach', True)
driver = webdriver.Chrome(options=r_options)


name_list1 = ['Austin Ekeler','Christian McCaffrey','Saquon Barkley','Derrick Henry','Tony Pollard','Nick Chubb','Josh Jacobs','Jonathan Taylor','Joe Mixon','Travis Etienne Jr.','Najee Harris','Jahmyr Gibbs','Aaron Jones','Rhamondre Stevenson',
              'Damien Pierce','Breece Hall','Rachaad White','Alvin Kamara','Miles Sanders','James Conner','Kenneth Walker','Alexander Mattison','James Cook','Javonte Williams','Cam Akers','David Montgomery','Isiah Pacheco','JK Dobbins','Dalvin Cook',
              'Khalil Herbert','AJ Dillon','Dandre Swift','Brian Robinson Jr.','Antonio Gibson','Jamaal Williams','Jeff Wilson Jr.','Samaje Perine','Rashaad Penny','Jerick McKinnon','Devin Singletary','Elijah Mitchell','Ezekiel Elliott','Jaylen Warren'
              'Tyler Allgeier','Raheem Mostert','Gus Edwards','Damien Harris','Kenneth Gainwell','Donte Foreman','Kyren Williams']

name_list = ['Travis Etienne Jr.','Najee Harris','Jahmyr Gibbs','Aaron Jones','Rhamondre Stevenson',
              'Damien Pierce','Breece Hall','Rachaad White','Alvin Kamara','Miles Sanders','James Conner','Kenneth Walker','Alexander Mattison','James Cook','Javonte Williams','Cam Akers','David Montgomery','Isiah Pacheco','JK Dobbins','Dalvin Cook',
              'Khalil Herbert','AJ Dillon','Dandre Swift','Brian Robinson Jr.','Antonio Gibson','Jamaal Williams','Jeff Wilson Jr.','Samaje Perine','Rashaad Penny','Jerick McKinnon','Devin Singletary','Elijah Mitchell','Ezekiel Elliott','Jaylen Warren'
              'Tyler Allgeier','Raheem Mostert','Gus Edwards','Damien Harris','Kenneth Gainwell','Donte Foreman','Kyren Williams']



for name in name_list:
    with open('rbfantasytest.csv', 'w') as f:
            f.write("SEASON,TEAM,GP,PTS,PPG,SNP%,OPP,ATT,YDS,Y/A,LNG,TD,FUM,TGT,REC,CTCH%,YDS,Y/C,LNG,TD"+'\n')
    Player_name = name
    driver.get("https://www.google.com")
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
    lines_to_remove =  ["SEASON TEAM GP RNK PTS PPG SNP% OPP ATT YDS Y/A LNG TD FUM TGT REC CTCH% YDS Y/C LNG TD", "Fantasy Rushing Receiving",]
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

    with open('rbfantasytest.csv', 'a') as f:
        f.write(csv_content+"\n")
        print(csv_content)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    
    train_data = pd.read_csv('rbfantasytrain.csv')
    train_data = train_data.drop('TEAM',axis=1)
    for column in train_data.columns:
        if train_data[column].dtype == 'O':  # Check if the data type is object (str)
            train_data[column] = train_data[column].str.replace('%', '').replace('-', np.nan).astype(float)

    #train_data = train_data[train_data['SEASON'] !=2022]

    #train_data['SNP%'] = train_data['SNP%'].str.replace('%', '').astype(float)
    #train_data['CTCH%'] = train_data['CTCH%'].str.replace('%', '').astype(float)


    test_data = pd.read_csv('rbfantasytest.csv')
    test_data = test_data.drop('TEAM',axis=1)
    test_data.fillna(0, inplace=True)
    for column in test_data.columns:
        if test_data[column].dtype == 'O':  # Check if the data type is object (str)
            test_data[column] = test_data[column].str.replace('%', '').replace('-', np.nan).astype(float)
    #test_data = test_data[test_data['SEASON'] !=2022]

    #test_data['SNP%'] = test_data['SNP%'].str.replace('%', '').astype(float)
    #test_data['CTCH%'] = test_data['CTCH%'].str.replace('%', '').astype(float)



    train_data = train_data[train_data['PTS']>=150]
    if(test_data.shape[0]<9):
        borg = test_data[test_data['GP'] >=14]
        if(borg.shape[0]>0):
            test_data=test_data[test_data['GP'] >=14]
        else: test_data = test_data
        

    # Preprocess the data by dropping rows with the year 2022
    #train_data.drop(train_data[train_data['SEASON'] == 2022].index, axis=0, inplace=True)
    #test_data.drop(test_data[test_data['SEASON'] == 2022].index, axis=0, inplace=True)


    def custom_weight_fpts(fpts):
        return np.log(fpts)


    # Prepare the training data
    train_features = train_data[['SEASON','GP','PPG','SNP%','OPP','ATT','YDS','Y/A','LNG','TD','FUM','TGT','REC','CTCH%','YDS.1','Y/C','LNG.1','TD.1']]
    train_target = train_data['PTS']
    weights_fpts = custom_weight_fpts(train_target)
    # Prepare the testing data
    test_features = test_data[['SEASON','GP','PPG','SNP%','OPP','ATT','YDS','Y/A','LNG','TD','FUM','TGT','REC','CTCH%','YDS.1','Y/C','LNG.1','TD.1']]

    # Create an imputer for missing values (if any)
    imputer = SimpleImputer(strategy='mean') 

    # Fill missing values in the training data
    train_features = imputer.fit_transform(train_features)

    # Standardize the features
    scaler = StandardScaler()
    train_features = scaler.fit_transform(train_features)
    test_features = scaler.transform(test_features)

    # Train the SVR model
    svr_model = SVR(kernel='linear', C=1.0, gamma='scale')
    svr_model.fit(train_features, train_target)

    # Predict next year's FPTS for the specific player
    next_year_data = test_data.iloc[-1][['SEASON','GP','PPG','SNP%','OPP','ATT','YDS','Y/A','LNG','TD','FUM','TGT','REC','CTCH%','YDS.1','Y/C','LNG.1','TD.1']].values.reshape(1, -1)
    prediction = svr_model.predict(next_year_data)
    pog = prediction[0]
    barg = pog/100
    with open('V2rbpredcont.csv','a') as file:
        file.write(Player_name+','+str(barg)+"\n")
    print(f'Predicted fantasy points for next year: {barg}')
    with open('rbfantasytest.csv', 'w', newline='') as file:
        file.truncate(0)
    
driver.close()
