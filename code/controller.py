'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''



#from bottle import route, get, post, request, static_file, response, delete
from bottle import request, static_file, response

import bottle_instance

import model


# some utility functions 

"""
    Takes a request object and tries to get the session cookie
    
    Returns the session_cookie value if one exists, otherwise returns None

    If an unspecified exception occurs it returns None
"""
def safe_get_session(request):
    try:
        if not request:
            return None

        session_cookie = request.get_cookie('authentication')

        if not session_cookie:
            return None
        
        return session_cookie
    
    except:
        return None

app = bottle_instance.app


#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@app.route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@app.route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@app.route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
############# THIS IS BROKEN ################
############ CAN'T CORRECTLY CHANGE NAVBAR FOR ADMINS SINCE ITS STATIC
############# NEED TO CHANGE TO A MODEL PAGE VIEW

# Allow serving file
@app.route('/file/<filename:path>')
def serve_file(filename):
    '''
        serve_file

        Serves file from static/file/

        :: filename :: A path to the requested file

        Returns a static file object containing the requested file
    '''
    return static_file(filename, root='static/file/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@app.get('/')
@app.get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    session_cookie = safe_get_session(request)
    return model.index(session_cookie=session_cookie)

#-----------------------------------------------------------------------------

# Display the login page
@app.get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    session_cookie = safe_get_session(request)
    
    return model.login_form(session_cookie=session_cookie)

@app.get('/logout')
def logout():
    session_cookie = safe_get_session(request)

    return model.logout(session_cookie=session_cookie)

    

#-----------------------------------------------------------------------------

# Attempt the login
@app.post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''
    session_cookie = safe_get_session(request)
    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    (page, cookie) = model.login_check(username, password, session_cookie=session_cookie)
    if cookie != None:
        response.set_cookie('authentication', cookie, secure=True, httponly=True)
    return page
    

#-----------------------------------------------------------------------------

@app.get('/signup')
def get_signup_controller():
    '''
        get_signup

        Serves the sign up page
    '''
    session_cookie = safe_get_session(request)

    return model.signup_form(session_cookie=session_cookie)



@app.post('/signup')
def post_signup():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    confirm_password = request.forms.get('confirm_password')
    
    session_cookie = safe_get_session(request)
    (page, cookie) = model.create_user(username=username, password=password, confirm_password=confirm_password, session_cookie=session_cookie)
    if cookie != None:
        response.set_cookie('authentication', cookie)
    return page
    
    


#-----------------------------------------------------------------------------

@app.get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    session_cookie = safe_get_session(request)
    return model.about(session_cookie=session_cookie)
   
#-----------------------------------------------------------------------------

@app.route('/content', method='GET')
@app.get('/content/<cat>')
def get_content_index(cat=""):
    """
        serves a content index page
    """
    session_cookie = safe_get_session(request)
    return model.content_index(cat, session_cookie=session_cookie)

#-----------------------------------------------------------------------------

@app.get('/content/<cat>/<sub_cat>')
def get_content(cat, sub_cat):
    """
        serves a content page
    """
    session_cookie = safe_get_session(request)
    return model.content(cat, sub_cat, session_cookie=session_cookie)
#-----------------------------------------------------------------------------


############# THIS IS BROKEN ################
############ CAN'T CORRECTLY CHANGE NAVBAR FOR ADMINS SINCE ITS STATIC
############# NEED TO CHANGE TO A MODEL PAGE VIEW
@app.get('/content/<cat>/<sub_cat>/<sub_sub_cat>')
def get_content_example(cat, sub_cat, sub_sub_cat):
    """
        serves a content page
    """

    return static_file(sub_sub_cat+".html", root="./templates/d_content/" + cat + "/" + sub_cat + "/" )
  
#-----------------------------------------------------------------------------

@app.get('/forum/<cat>')
def get_forum_page(cat):
    session_cookie = safe_get_session(request)
    return model.forum_page(cat, session_cookie=session_cookie)

@app.get('/forum')
def get_forum_landing():
    """
        serves static forum page
    """
    session_cookie = safe_get_session(request)
    return model.forum_landing(session_cookie=session_cookie)
#-----------------------------------------------------------------------------

@app.get('/forum_post/<id>')
def get_forum_post(id):
    """
        serves forum static content page
    """
    session_cookie = safe_get_session(request)
    return model.forum_post(id, session_cookie=session_cookie)

@app.post('/forum_post/<id>')
def forum_reply(id):
    request.forms["parent_id"] = id
    session_cookie = safe_get_session(request)
    return model.create_post_reply(session_cookie=session_cookie, post=request.forms)

@app.post('/report_post/<id>')
def report_post(id):
    session_cookie = safe_get_session(request)
    return model.report_post(id, session_cookie=session_cookie)

#-----------------------------------------------------------------------------

@app.get('/forum_new_post')
def get_forum_post():
    """
        serves to write a post
    """
    session_cookie = safe_get_session(request)
    return model.forum_new_post(session_cookie=session_cookie)

@app.post('/forum_new_post')
def create_forum_post():

    request.forms["parent_id"] = -1

    session_cookie = safe_get_session(request)
    return model.forum_create_new_post(session_cookie=session_cookie, post=request.forms)



#-----------------------------------------------------------------------------

@app.get('/faq')
def get_forum_landing():
    """
        serves static forum page
    """
    session_cookie = safe_get_session(request)
    return model.faq(session_cookie=session_cookie)
#-----------------------------------------------------------------------------


@app.get('/admin/users')
def get_users():
    """
        serves user page
    """
    session_cookie = safe_get_session(request)
    return model.admin_users(session_cookie=session_cookie)

@app.get('/admin/users/<uid>')
def get_posts(uid):
    session_cookie = safe_get_session(request)
    return model.admin_posts(uid, session_cookie=session_cookie)

@app.route('/posts/<pid>', method="POST")
def del_post(pid):
    session_cookie = safe_get_session(request)
    return model.del_post(pid, session_cookie=session_cookie)

@app.route('/users/ban/<uid>', method='POST')
def ban_user(uid):
    session_cookie = safe_get_session(request)
    return model.ban_user(uid, session_cookie=session_cookie)


@app.route('/users/unban/<uid>', method='POST')
def unban_user(uid):
    session_cookie = safe_get_session(request)
    return model.unban_user(uid, session_cookie=session_cookie)

