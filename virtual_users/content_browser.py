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

        #need to make sign_up page for website 
        #can then login with this function for every vu

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

