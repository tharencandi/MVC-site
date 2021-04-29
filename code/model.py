'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
from sql import SQLDatabase

# Initialise our views, all arguments are defaults for the template
page_view = view.View()
db = SQLDatabase("database.db")

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):

    ##########################################
    ##########################################
    ##########################################
    ########            API          #########
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    login = db.check_credentials(username, password)

    if login == False:
        err_str = "Incorrect username/password"
        
    if login: 
        return page_view("success", name=username)
    else:
        return page_view("error", reason=err_str)

def signup_form():
    '''
        signup_form
        Returns the view for the signup_form
    '''
    return page_view("signup")

def create_user(username, password, confirm_password):
    ##########################################
    ##########################################
    ##########################################
    ########            API          #########
    '''
        User sign up logic
        Returns success page if success,
        error page if failed with reasons defined here or sql.
    '''
    if username == None or password == None or confirm_password == None:
        return page_view("error", reason="Internal server error")
    
    if password != confirm_password:
        return page_view("error", reason="Password does not match!")

    result = db.add_user(username=username, password=password)
    if result[0] == True:
        return page_view("success", name=username)
    else:
        return page_view("error", reason=result[1])

    

def set_user_pass(username, password):
    original_username = username
    original_password = password
    return
    
#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())

# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace diversity and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from generation X and is on the runway heading towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]

#----------------------------------------------------------------------------

def content_index(cat):
    path = f"content"
    return page_view(path)

#-----------------------------------------------------------------------------

def content(cat, sub_cat):
    # add type information and any other template vars to page view function
    path = "d_content/" + cat + "/" + sub_cat

    return page_view(path)

#-----------------------------------------------------------------------------

def forum_page(cat):
    path = f"d_forum/{cat}"
    return page_view(path)


def forum_landing():
    # Forum landing page
    return page_view("forum")

#-----------------------------------------------------------------------------

def forum_post():
    # Forum landing post
    return page_view("forum_post")

#-----------------------------------------------------------------------------

def forum_new_post():
    # Forum landing post
    return page_view("forum_new_post")
#-----------------------------------------------------------------------------

def faq():
    # Forum landing post
    return page_view("faq")
