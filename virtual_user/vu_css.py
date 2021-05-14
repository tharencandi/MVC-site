from virtual_user import Virtual_user
print("Start going through all css contents")

vu1 = Virtual_user()
vu1.click_button('//*[@id="content_cards"]/li[3]/a/div')

vu1.click_button('/html/body/nav[2]/a[3]')

vu1.click_button('/html/body/nav[2]/a[4]')
vu1.click_button('/html/body/nav[2]/a[5]')

vu1.click_button('/html/body/nav[2]/a[1]')

vu1.quit()
print("Successfully go through all css contents!")