from virtual_user import Virtual_user

# this virtual user goes to each link for the javascript section on the learn page
new_virtual = Virtual_user()
print('Virtual User has started on the Learn Page, in the Javascript section')

new_virtual.click_button('/html/body/nav/div/a[2]')
new_virtual.click_button('//*[@id="main"]/ul[4]/li[1]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[4]/li[2]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[4]/li[3]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[4]/li[4]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[4]/li[5]/a')
new_virtual.goback()
new_virtual.quit()
print('Virtual user has successfully completed going though this section')
