from virtual_user import Virtual_user
print("login, post, reply and report post in the JS forum")
vu1 = Virtual_user()
vu1.sign_up("jarrd100", "jarrd100")
vu1.log_in("jarrd100", "jarrd100")
vu1.click_button('/html/body/p/a')
vu1.click_button('/html/body/nav[1]/div/a[3]')
vu1.click_button('/html/body/main/article/div[1]/a/button')
vu1.text('//*[@id="title"]', "I'm jarrd100")
vu1.text('//*[@id="body"]', "I'm jarrd100")
vu1.click_button('/html/body/div/div/article/form/select/option[6]')
vu1.click_button('/html/body/div/div/article/form/input[3]')

vu1.click_button('/html/body/nav[1]/div/a[3]')
vu1.click_button('/html/body/nav[2]/a[6]')
vu1.click_button('/html/body/main/article/div[3]/article[1]/header/div/a/h1')
vu1.click_button('/html/body/main/div[1]/article/form/input')
vu1.click_button('/html/body/main/div[1]/a/button')
vu1.quit()
print("Successfully reported post in the JS forum")