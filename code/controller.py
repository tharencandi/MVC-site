'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''



from bottle import route, get, post, request, static_file, response, delete


import model

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
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
@route('/css/<css:path>')
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
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------

# Allow serving file
@route('/file/<filename:path>')
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
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    
    return model.login_form()
  
    

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    (page, cookie) = model.login_check(username, password)
    if cookie != None:
        print("COOOKIE", cookie)
        response.set_cookie('authentication', cookie.decode('utf-8'))
    return page
    

#-----------------------------------------------------------------------------

@get('/signup')
def get_signup_controller():
    '''
        get_signup

        Serves the sign up page
    '''
    return model.signup_form()



@post('/signup')
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

    return model.create_user(username=username, password=password, confirm_password=confirm_password)
    
    


#-----------------------------------------------------------------------------

@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
   
#-----------------------------------------------------------------------------

@route('/content', method='GET')
@get('/content/<cat>')
def get_content_index(cat=""):
    """
        serves a content index page
    """
    return model.content_index(cat)

#-----------------------------------------------------------------------------

@get('/content/<cat>/<sub_cat>')
def get_content(cat, sub_cat):
    """
        serves a content page
    """
    return model.content(cat, sub_cat)
#-----------------------------------------------------------------------------

@get('/content/<cat>/<sub_cat>/<sub_sub_cat>')
def get_content_example(cat, sub_cat, sub_sub_cat):
    """
        serves a content page
    """
    return static_file(sub_sub_cat+".html", root="./templates/d_content/" + cat + "/" + sub_cat + "/" )
  
#-----------------------------------------------------------------------------

@get('/forum/<cat>')
def get_forum_page(cat):
    return model.forum_page(cat)

@get('/forum')
def get_forum_landing():
    """
        serves static forum page
    """
    return model.forum_landing()
#-----------------------------------------------------------------------------

@get('/forum_post/<id>')
def get_forum_post(id):
    print("hello")
    """
        serves forum static content page
    """
    return model.forum_post(id)

@post('/forum_post/<id>')
def forum_reply(id):
    print("hello")
    cookie = request.get_cookie('authentication')
    if cookie != None:
        cookie = cookie.encode()
    request.forms["parent_id"] = id
    return model.create_post_reply(cookie=cookie, post=request.forms)

#-----------------------------------------------------------------------------

@get('/forum_new_post')
def get_forum_post():
    """
        serves to write a post
    """
    return model.forum_new_post()

@post('/forum_new_post')
def create_forum_post():
    cookie = request.get_cookie('authentication').encode()
    request.forms["parent_id"] = -1
    return model.forum_create_new_post(cookie=cookie, post=request.forms)

#-----------------------------------------------------------------------------

@get('/faq')
def get_forum_landing():
    """
        serves static forum page
    """
    return model.faq()
#-----------------------------------------------------------------------------


@get('/admin/users')
def get_users():
    """
        serves user page
    """
    return model.admin_users()

@get('/admin/users/<uid>')
def get_posts(uid):
    return model.admin_posts(uid)

@delete('/posts/<pid>')
def del_post(pid):
    model.del_post(pid)

@delete('/users/<uid>')
def del_post(uid):
    model.del_user(uid)

