import os
import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
options = Options()
rawdata = os.path.join('F:\\Selenium\\rawData')
saveData = os.path.join('F:\\Selenium\\saveData')
backupData = os.path.join('F:\\Selenium\\backupData')
driver = webdriver.Chrome(executable_path=r"F:\\driver\\chromedriver.exe")
datas = []
def valid_date(startdate,enddate):
    url = "https://amg.gwynedd.llyw.cymru/planning/index.html?fa=search"
    driver.get(url)    
    driver.implicitly_wait(30)
    driver.maximize_window()
    driver.find_element_by_xpath("//input[@name='valid_date_from']").send_keys(startdate)
    driver.find_element_by_xpath("//input[@name='valid_date_to']").send_keys(enddate)
    driver.find_element_by_xpath("//button[@type='submit']").click()
    driver.implicitly_wait(30)  
    pre = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(5)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height==pre:
            break
        pre=new_height 

def extract_data():
    all_data = driver.find_elements_by_xpath("//tbody/tr")
    print(len(all_data))
    actions = ActionChains(driver)
    for data in all_data:
        actions = ActionChains(driver)
        actions.move_to_element(data).perform()
        try:
            Proposal = data.find_element_by_xpath(".//td[4]").text
            print(Proposal)            
        except:
            Proposal = ""
            print(Proposal)
        try:
            Decision = data.find_element_by_xpath(".//td[7]").text
            print(Decision)
        except:
            Decision = ""
            print(Decision) 
        try:
            Ward = data.find_element_by_xpath(".//td[5]").text
            print(Ward)
        except: 
            Ward = ""
            print(Ward)
        temp = "https://amg.gwynedd.llyw.cymru/planning/index.html?fa=getApplication&id="   
        id = data.find_element_by_xpath(".//button").get_attribute('data-id')
        View = temp+id
        print(View)   
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        datas.append([Proposal, Decision, Ward, View])

    def GetDetailsOfItem(Link):
        driver.get(Link)
        driver.implicitly_wait(10)
        try:
            ApplicationReferenceNumber = driver.find_element_by_xpath("//div[@class='col-md-7']").text            
            print(ApplicationReferenceNumber)
        except:
            ApplicationReferenceNumber = ""                 
        return pd.Series([ApplicationReferenceNumber])    

    datadf = pd.DataFrame(datas, columns=['Proposal', 'Decision', 'Ward', 'View'])
    datadf.to_csv(os.path.join(rawdata, 'temp.csv'), index=False)
    if len(datadf) == 0:
        driver.close()
    else:
        datadf[['ApplicationReferenceNumber']] = datadf[['View']].apply(lambda x: GetDetailsOfItem(x[0]), axis=1)
        datadf = datadf[['Proposal', 'Decision', 'Ward', 'View','ApplicationReferenceNumber']]
        datadf.to_csv(os.path.join(saveData, 'gwynedd.csv'), index=False)

    driver.close()    

valid_date('01-12-2020','01-12-2021') 
extract_data()   
 