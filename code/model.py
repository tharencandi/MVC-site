'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
import socket
import json
import bcrypt
import hashlib
from datetime import date, datetime, timedelta

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

cookies = {}

def db_req(function, paramaters):

    query = {
        "function": function,
        "params": paramaters,
        "auth": "password",      
    }
    HOST, PORT = "localhost", 9999
    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(bytes(json.dumps(query), encoding="utf-8"), (HOST, PORT))
    data = sock.recv(2048)
    if data != None:
        received = json.loads(data.decode())
        return received
    return None


def encrypt_password(password,salt):
    m = hashlib.sha512()
    m.update(password.encode())
    hashed_password = m.digest()
    if salt == None:
        salt = bcrypt.gensalt()
    encrypted_password = bcrypt.hashpw(hashed_password, salt)
    return encrypted_password, salt

def create_cookie(user_id, is_admin = False):
    cookie = bcrypt.Random.get_random_bytes(16)
    cookies[cookie] = [user_id, datetime.now(), is_admin]
    return cookie

"""Ensures a cookie exists and hasn't expired. If it exists and hasn't expired,
expory time is reset to 5 minutes from current time"""
def get_cookie(cookie):
    if not cookie:
        return None

    res = None
    try:
        if cookie in cookies:
            birth_time = cookies.get(cookie)[1]
            now = datetime.now()
            tdelta = now - birth_time
            delta_threshold = timedelta(minutes=5)
            
            # cookie has expired
            if tdelta > delta_threshold:
                cookies.pop(cookie)
            else:
                exp_time = now + timedelta(minutes=5)
                cookies.get(cookie)[1] = exp_time
                res = cookies.get(cookie)[0]
    except:
        return None

    return res

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index(unvalidated_session_cookie=None):
    '''
        index
        Returns the view for the index
    '''
    try:
        if unvalidated_session_cookie:
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("index", is_admin=session_cookie[2])
    except:
        pass

    return page_view("index", message=None)

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form(unvalidated_session_cookie=None):
    '''
        login_form
        Returns the view for the login_form
    '''
    try:
        if unvalidated_session_cookie:
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("index", is_admin=session_cookie[2])
    except:
        pass
    return page_view("login", message=None)

#-----------------------------------------------------------------------------

  
# Check the login credential
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
    salt = db_req("get_salt_by_username", {"username": username})[0]["salt"]

    encrypted_password, salt = encrypt_password(password, salt.encode())
    print(encrypted_password)

    res = db_req("check_credentials", {"username": username, "password": encrypted_password.decode(),})
    print("REEEEEE", res)

    if res["success"] == False :
        print("hello")
        err_str = "Incorrect username/password"
        return (page_view("error", reason=err_str), None)
    else:

        cookie = create_cookie(res["id"])
     
        return (page_view("success", name=username), cookie)
 
        

def signup_form(unvalidated_session_cookie=None):
    '''
        signup_form
        Returns the view for the signup_form
    '''
    try:
        if unvalidated_session_cookie:
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("index", message="You are already signed in." is_admin=session_cookie[2])
    except:
        pass

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


    encrypted_password, salt = encrypt_password(password=password, salt=None)
    res = db_req("add_user", {'username': username, 'password': encrypted_password.decode(), "salt": salt.decode(), "is_admin": 0})
   
    if res["success"] == True:
        return page_view("success", name=username)
    else:
        return page_view("error", reason=res["error_msg"])

    

def set_user_pass(username, password):
    original_username = username
    original_password = password
    return
    
#----------------------------------------------------------------------------

def content_index(cat, session=None):
    path = "content"

    try:
        if session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("content", is_admin=session_cookie[2])
    except:
        pass

    return page_view("content")

#-----------------------------------------------------------------------------

def content(cat, sub_cat, session=None):
    # add type information and any other template vars to page view function
    path = "d_content/" + cat + "/" + sub_cat

    try:
        if session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view(path, is_admin=session_cookie[2])
    except:
        pass

    return page_view(path)

#-----------------------------------------------------------------------------

def forum_page(cat, session=None):
    path = f"d_forum/{cat}"
    posts = db_req("get_posts", {"forum": cat})

    try:
        if session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("d_forum/forum", forum=cat, posts=posts, hasSession=True is_admin=session_cookie[2])
    except:
        pass

    return page_view("d_forum/forum", forum=cat, posts=posts)


def forum_landing(**kwargs):
    # Forum landing page
    try:
        if session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("forum", hasSession=True, is_admin=session_cookie[2])
    except:
        pass

    return page_view("forum")

#-----------------------------------------------------------------------------

def forum_post(id, **kwargs):
    # Forum landing post
    res = db_req("get_post_thread", {"id": id})
    print(res)
    post = res[0]
    replies = res[1:]

    try:
        if session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("d_forum/forum_post", post=post, replies=replies, hasSession=True is_admin=session_cookie[2])
    except:
        pass

    return page_view("d_forum/forum_post", post=post, replies=replies)

#-----------------------------------------------------------------------------

def forum_new_post(**kwargs):
    # Forum landing post

    try:
        if session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("d_forum/forum_new_post", hasSession=True, is_admin=session_cookie[2])
    except:
        pass
    return page_view("login", message="Please log in before posting.")

def forum_create_new_post(cookie, post):

    try:
        if not session in kwargs:
            unvalidated_session_cookie = kwargs['session']
            session_cookie = get_cookie(unvalidated_session_cookie)
            if session_cookie:
                return page_view("d_forum/forum_new_post", hasSession=True, is_admin=session_cookie[2])
    except:
        pass

  

    #post_details :(author_id, forum, title, body, parent_id )

    post_dict = {
        "author_id": user_id,
        "forum": post["forum"],
        "title": post["title"],
        "body": post["body"],
        "parent_id": -1,
    } 
    res = db_req("add_post",  post_dict)

    if res["success"] == False:
        return page_view("error", reason="internal server error")
    return forum_page(post["forum"])

def create_post_reply(cookie, post):

    user_id = get_id(cookie)
    if user_id == None:
        print("cookie not found")
        return page_view("error", reason="must be logged in")

    parent_post = db_req("get_post", {"id": post["parent_id"]})[0]
   
    print("\n parent")
    print(parent_post)

    
    post_dict = {
        "title": "",
        "body": post["answer"], 
        "forum": parent_post["forum"],
        "parent_id": post["parent_id"],
        "author_id": user_id,
    }


    res = db_req("add_post", post_dict )
  
    if res == False:
        return page_view("error", reason="internal server error")
    return forum_post(post["parent_id"])

    

   
    
#-----------------------------------------------------------------------------

def faq():
    # Forum landing post
    return page_view("faq") 

#-----------------------------------------------------------------------------

def admin_users():
    users = [{"id": 1, "username": "tharen", "num_posts": 9000000}, {"id": 2, "username": "tharen", "num_posts": 9000000}]
    # "posts": [{"id": 1, "reports": 1000}]},{"username": "tharen", "num_posts": 9000000, "posts": [{"id": 1, "reports": 1000, "title": "bla bla"}]
    return page_view("admin_users", users=users)

def admin_posts(user):
    # get the users name, number of posts and posts 
    username="Username"
    num_posts = 1
    posts = [{"id": 1, "reports": 1000, "title": "bla bla"}, {"id": 2, "reports": 1000, "title": "bla bla"}, {"id": 3, "reports": 1000, "title": "bla bla"}]

    return page_view("admin_posts", username=username, num_posts=num_posts, posts=posts)


def del_post(pid):
    print("delete http method")
    print(pid)

            
def del_user(uid):
    print(f"delete user {uid}")

