from virtual_user import Virtual_user
print("login, post, reply and report reply in the css forum")
vu1 = Virtual_user()
vu1.sign_up("jarrd100", "jarrd100")
vu1.log_in("jarrd100", "jarrd100")
vu1.click_button('/html/body/p/a')
vu1.click_button('/html/body/nav[1]/div/a[3]')
vu1.click_button('/html/body/main/article/div[1]/a/button')
vu1.text('//*[@id="title"]', "a")
vu1.text('//*[@id="body"]', "a")
vu1.click_button('/html/body/div/div/article/form/select/option[4]')
vu1.click_button('/html/body/div/div/article/form/input[3]')

vu1.click_button('/html/body/nav[1]/div/a[3]')
vu1.click_button('/html/body/nav[2]/a[4]')
vu1.click_button('/html/body/main/article/div[3]/article[1]/header/div/a/h1')
vu1.text('//*[@id="answer"]', "a")
vu1.click_button('/html/body/main/div[2]/article/form/input[2]')
vu1.click_button('/html/body/main/div[3]/article[1]/form')
vu1.quit()
print("Successfully reported reply in the css forum")
