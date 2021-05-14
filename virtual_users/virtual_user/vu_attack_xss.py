from virtual_user import Virtual_user

# this virtual user tries to do a xss attack on the login page and forum page
new_virtual = Virtual_user()
print('Virtual User has started on the Sign In Page and started xss attack')

new_virtual.sign_up("jerry1", "password")
new_virtual.click_button('//*[@id="login"]')
new_virtual.text('//*[@id="main"]/form/input[1]', '<script> alert("Hello!"); </script>')
new_virtual.text('//*[@id="main"]/form/input[2]', 'yes')
new_virtual.click_button('//*[@id="main"]/form/input[3]')
new_virtual.click_button('//*[@id="login"]')

new_virtual.text('//*[@id="main"]/form/input[1]', '<body onload=alert("XSS")>')
new_virtual.text('//*[@id="main"]/form/input[2]', 'yes')
new_virtual.click_button('//*[@id="main"]/form/input[3]')
new_virtual.click_button('//*[@id="login"]')

new_virtual.text('//*[@id="main"]/form/input[1]', 'jerry1')
new_virtual.text('//*[@id="main"]/form/input[2]', 'password')
new_virtual.click_button('//*[@id="main"]/form/input[3]')
new_virtual.click_button('//*[@id="login"]')


new_virtual.click_button('/html/body/nav/div/a[3]')
new_virtual.click_button('/html/body/main/article/div[1]/a/button')
new_virtual.text('//*[@id="title"]', '<script> alert("Hello!"); </script>')
new_virtual.text('//*[@id="body"]', '<script> alert("Hello!"); </script>')
new_virtual.click_button('//*[@id="main"]/div/article/form/input[3]')

new_virtual.click_button('/html/body/main/article/div[3]/article[1]/header/div/a/h1')

new_virtual.text('//*[@id="answer"]', '<script> alert("Hello!"); </script>')
new_virtual.click_button('/html/body/main/div[2]/article/form/input[2]')

new_virtual.quit()


print('xss attack failed')
