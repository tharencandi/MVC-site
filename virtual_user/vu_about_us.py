from virtual_user import Virtual_user

print("starting going through about us page")
# this virtual user goes to the About Us page and back to the main page
new_virtual = Virtual_user()

new_virtual.click_button('/html/body/nav/div/a[5]')

new_virtual.click_button('/html/body/nav/div/a[1]/b')

new_virtual.quit()
print("Successfully went through the about us page!")