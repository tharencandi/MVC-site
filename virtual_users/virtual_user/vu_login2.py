from virtual_user import Virtual_user
print("login with incorrect username and password combination")
vu1 = Virtual_user()
vu1.sign_up("jghcdtfyghgcfxndty", "i;pojkkyigyehap'[")
vu1.log_in("jghcdtfyghgcfxndty", "i;pojkgyehap'[")
vu1.quit()
print("login failed")