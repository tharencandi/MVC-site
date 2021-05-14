from virtual_user import Virtual_user

#goes to the web works content page, then goes back
# then goes through all headings in HTML and goes back to the main page 
print("Start going through all html contents")
new_virtual = Virtual_user()


new_virtual.click_button('//*[@id="content_cards"]/li[2]/a/div')
new_virtual.click_button('/html/body/nav[2]/a[3]')
new_virtual.click_button('/html/body/nav[2]/a[4]')
new_virtual.click_button('/html/body/nav[2]/a[5]')
new_virtual.click_button('/html/body/nav[2]/a[6]')
new_virtual.click_button('/html/body/nav[2]/a[1]')
new_virtual.quit()
print("Successfully go through all html contents!")