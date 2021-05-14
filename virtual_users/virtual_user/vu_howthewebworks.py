from virtual_user import Virtual_user
print("Start going through all how the web works contents")
vu1 = Virtual_user()
vu1.click_button('//*[@id="content_cards"]/li[1]/a/div')

vu1.click_button('/html/body/nav[2]/a[1]')
vu1.quit()
print("Successfully go through all how the web works contents!")