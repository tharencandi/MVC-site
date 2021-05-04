import getpass
import selenium 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class virtual_user:

    options = Options()
    options.headless = True

    def __init__(self):
        self.driver = webdriver.Firefox(options=virtual_user.options)
        self.is_logged_in = False

    def login(self):
        username = getpass.getpass()
        password = getpass.getpass()

        #need to make login page for website 
        #can then login with this function for every vu

    def sign_up(self):
        username = getpass.getpass()
        password = getpass.getpass()

        name_f = self.driver.find_element_by_name('username')
        name_f.clear()
        name_f.send_keys(username)

        pass_f = self.driver.find_element_by_name('password')
        pass_f.clear()
        pass_f.send_keys(password)

        pass_f.submit()

    def visit(self, page_url):
        self.driver.get(page_url)

    def send_message(self, message, dest):
        pass

    def ban(self, target):
        pass

    def unban(self, target):
        pass

    def post(self, title, body):
        pass

