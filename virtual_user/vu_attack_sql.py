from virtual_user import Virtual_user

# this virtual user tries to do a sql injection
new_virtual = Virtual_user()
print('Virtual User has started on the Sign In Page and started sql attack')


new_virtual.click_button('//*[@id="login"]')
new_virtual.text('//*[@id="main"]/form/input[1]', '\'OR 1 --')
new_virtual.text('//*[@id="main"]/form/input[2]', 'password')
new_virtual.click_button('//*[@id="main"]/form/input[3]')
new_virtual.click_button('//*[@id="login"]')
new_virtual.sign_up("jerry14", "password")

new_virtual.click_button('/html/body/nav/div/a[3]')
new_virtual.click_button('/html/body/main/article/div[1]/a/button')

new_virtual.text('//*[@id="title"]', '\'OR 1 --')
new_virtual.text('//*[@id="body"]', '\'OR 1 --')
new_virtual.click_button('//*[@id="main"]/div/article/form/input[3]')


new_virtual.quit()
print('sql attack failed')
