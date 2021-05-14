from virtual_user import Virtual_user

#this virtual user goes to the FAQ section and presses the 'CV site' link
#this takes the user to working example page, the user than goes through
#the subheadings on the side nav bar
print("Start going through FAQ page")
new_virtual = Virtual_user()

new_virtual.click_button('/html/body/nav/div/a[4]')


new_virtual.click_button('//*[@id="main"]/div[4]/p/a')

new_virtual.click_button('/html/body/main/div/p[1]/a')

new_virtual.click_button('/html/body/nav[2]/a[4]')

new_virtual.click_button('/html/body/nav[2]/a[5]')

new_virtual.click_button('/html/body/nav[2]/a[6]')

new_virtual.click_button('/html/body/nav[2]/a[1]')
new_virtual.quit()
print("Successfully went through FAQ page!")