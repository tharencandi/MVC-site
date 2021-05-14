from virtual_user import Virtual_user

# this virtual user goes to each link for the css section on the learn page
new_virtual = Virtual_user()
print('Virtual User has started on the Learn Page, in the CSS section')

new_virtual.click_button('/html/body/nav/div/a[2]')
new_virtual.click_button('//*[@id="main"]/ul[3]/li[1]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[3]/li[2]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[3]/li[3]/a')
new_virtual.goback()
new_virtual.click_button('//*[@id="main"]/ul[3]/li[4]/a')
new_virtual.goback()
new_virtual.quit()
print('Virtual user has successfully completed going though this section')
