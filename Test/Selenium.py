from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

PATH = '/Users/pouya/chromedriver'
driver = webdriver.Chrome(PATH)

driver.get("http://127.0.0.1:5000/ ")


#Open login page
logInLink = driver.find_element_by_xpath('//a[@href="/Auth/signIn"]')
logInLink.click()

#Login user,'Pouya'
usernameBox = driver.find_element_by_id("username")
usernameBox.send_keys("Pouya")
passwordBox = driver.find_element_by_id("password")
passwordBox.send_keys("Macbof-waqryh-9binba")
passwordBox.send_keys(Keys.RETURN)

for i in range(120):
#wait until the previuos page is loaded and then go to create issue page
    try:
        navbarDropdown2 = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'navbarDropdown2'))
        )
        navbarDropdown2.click()
        createIssueLink = driver.find_element_by_xpath('//a[@href="/createIssue"]')
        createIssueLink.click()
    except:
        print('Error after sigin')
        driver.quit()



#wait until the previuos page is loaded and then create issue 
    try:
        issueTextBox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'issue'))
        )
        issueTextBox.send_keys("Test topic creation using Selenium")
        createButton = driver.find_element_by_xpath("//input[@value='Create']")
        createButton.click()
    except:
        print('CreateIssue page did not load')
        driver.quit()


#Logout user and quit browser
try:
    navbarDropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'navbarDropdown'))
    )
    navbarDropdown.click()
    logOutLink = driver.find_element_by_xpath('//a[@href="/Auth/signOut"]')
    logOutLink.click()

finally:
    driver.quit()


