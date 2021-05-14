from virtual_user import Virtual_user
print("sign up with passwords which don't match each other")
vu1 = Virtual_user()
vu1.click_button('//*[@id="login"]')
vu1.click_button('/html/body/div/form/p/a')
usename = "pdkpjcdsc"
vu1.text('/html/body/div/form/input[1]', usename)
vu1.text('/html/body/div/form/input[2]', "123456")
vu1.text('/html/body/div/form/input[3]', "8675rthshgfd")

vu1.click_button('/html/body/div/form/input[4]')
vu1.quit()
print("sign up failed")