from virtual_user import Virtual_user
import time

# this virtual user tries to log in as a user and then logged in as the admin
# to ban that user. Then when the virtual user tries to log in as that user which
# is not allowed. Therefore, when the virtual user then tires to go to the forum
# and add a question, it shouldn't allow the virtual user to do that
vu1 = Virtual_user()
print('Admin ban and unban a user')
vu1.sign_up('jarred1', 'blah')

vu1.click_button('//*[@id="login"]')
vu1.click_button('//*[@id="login"]')
print("This test requires admin account log-in. \nPlease email or ask us for login information.\nhcai7597@uni.sydney.edu.au")
username = input('Enter username: ')
password = input('Enter password: ')

vu1.text('//*[@id="main"]/form/input[1]', username)
vu1.text('//*[@id="main"]/form/input[2]', password)
vu1.click_button('//*[@id="main"]/form/input[3]')

vu1.click_button('/html/body/nav/div/a[6]')
vu1.driver.find_element_by_id('jarred1').click()
vu1.click_button('//*[@id="login"]')
vu1.click_button('//*[@id="login"]')
vu1.log_in('jarred1', 'blah')
vu1.click_button('/html/body/nav/div/a[3]')
vu1.click_button('/html/body/main/article/div[1]/a/button')

vu1.click_button('//*[@id="login"]')
vu1.text('//*[@id="main"]/form/input[1]', username)
vu1.text('//*[@id="main"]/form/input[2]', password)
vu1.click_button('//*[@id="main"]/form/input[3]')
vu1.click_button('/html/body/nav/div/a[6]')
vu1.driver.find_element_by_id('jarred1').click()
vu1.quit()
print('Admin ban and unban functioned successfully')