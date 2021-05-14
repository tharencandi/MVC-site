from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options
import time

class Virtual_user:

    def __init__(self):
        #driverpath = "/home/roy/geckodriver"
        driverpath = "/usr/local/bin/geckodriver"
        url = "https://jerry.voyager.my"
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options, executable_path=driverpath)
        #self.driver = webdriver.Firefox(executable_path=driverpath)
        self.driver.get(url)

    def log_in(self, username, password):
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        nameinput = self.driver.find_element_by_xpath('/html/body/div/form/input[1]')
        nameinput.send_keys(username)
        #time.sleep(1)
        pwdinput = self.driver.find_element_by_xpath('/html/body/div/form/input[2]')
        pwdinput.send_keys(password)
        #time.sleep(1)
        loginbutton = self.driver.find_element_by_xpath('/html/body/div/form/input[3]')
        #time.sleep(1)
        loginbutton.click()
        #time.sleep(1)

        

    def sign_up(self, username, password):
        
        self.driver.find_element_by_xpath('//*[@id="login"]').click()
        self.driver.find_element_by_xpath('/html/body/div/form/p/a').click()
        nameinput = self.driver.find_element_by_xpath('/html/body/div/form/input[1]')
        nameinput.send_keys(username)
        #time.sleep(1)
        pwdinput = self.driver.find_element_by_xpath('/html/body/div/form/input[2]')
        pwdinput.send_keys(password)
        #time.sleep(1)
        cpwdinput = self.driver.find_element_by_xpath('/html/body/div/form/input[3]')
        cpwdinput.send_keys(password)
        #time.sleep(1)
        signupbutton = self.driver.find_element_by_xpath('/html/body/div/form/input[4]')
        #time.sleep(1)
        signupbutton.click()
        #time.sleep(1)

    def click_button(self, xpath):
        self.driver.find_element_by_xpath(xpath).click()
        time.sleep(1)
    
    def text(self,xpath, content):
        box = self.driver.find_element_by_xpath(xpath)
        box.send_keys(content)

    def goback(self):
        self.driver.back()
    
    def quit(self):
        self.driver.quit()
        