'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import socket
import json
import bcrypt
import hashlib
import secrets
from datetime import date, datetime, timedelta

import view
from sanitizer import Sanitizer
# Initialise our views, all arguments are defaults for the template
page_view = view.View()

cookies = {}
global_san = Sanitizer()

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
    cookie = secrets.token_hex(16)
    cookies[cookie] = [user_id, datetime.now(), is_admin]
    return cookie

"""Ensures a cookie exists and hasn't expired. If it exists and hasn't expired,
expory time is reset to 5 minutes from current time"""
def validate_cookie(cookie):
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
                res = cookies.get(cookie)
    except:
        return None

    return res

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index(session_cookie=None):
    '''
        index
        Returns the view for the index
    '''

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("index", has_session=True, is_admin=session_cookie[2])

    return page_view("index")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form(session_cookie=None):
    '''
        login_form
        Returns the view for the login_form
    '''

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2])
    return page_view("login")

#-----------------------------------------------------------------------------

  
# Check the login credential
def login_check(username, password, session_cookie=None):

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

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2])

    salt = db_req("get_salt_by_username", {"username": username})[0]["salt"]

    encrypted_password, salt = encrypt_password(password, salt.encode())
    print(encrypted_password)

    res = db_req("check_credentials", {"username": username, "password": encrypted_password.decode(),})

    if res["success"] == False :
        print("hello")
        err_str = "Incorrect username or password"
        return (page_view("error", message=err_str), None)
    else:

        cookie = create_cookie(res["id"])
     
        return (page_view("success", name=global_san.sanitize(username)), cookie)
 
        

def signup_form(session_cookie=None):
    '''
        signup_form
        Returns the view for the signup_form
    '''

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2])

    return page_view("signup")




def create_user(username, password, confirm_password, session_cookie=None):
    '''
        User sign up logic
        Returns success page if success,
        error page if failed with reasons defined here or sql.
    '''
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("error", message="Please logout before creating a user", has_session=True, is_admin=session_cookie[2])

    if username == None or password == None or confirm_password == None:
        return page_view("error", message="Internal server error")
    
    ##### Doesn't black list script tags need to fix
    if global_san.contains_black_list(username):
        return page_view("error", message="That username is not allowed")

    if password != confirm_password:
        return page_view("error", message="Password does not match!")


    hashed_password, salt = encrypt_password(password=password, salt=None)
    res = db_req("add_user", {'username': username, 'password': hashed_password.decode(), "salt": salt.decode(), "is_admin": 0})
   
    if res["success"] == True:
        return page_view("success", name=global_san.sanitize(username))
    else:
        return page_view("error", message=global_san.sanitize(res["error_msg"]))

    
#----------------------------------------------------------------------------

def content_index(cat, session_cookie=None):
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

def content(cat, sub_cat, session_cookie=None):
    # add type information and any other template vars to page view function
    path = "d_content/" + cat + "/" + sub_cat

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
            return page_view(path, has_session=True, is_admin=session_cookie[2])
    
    return page_view(path, has_session=False)

#-----------------------------------------------------------------------------

def forum_page(cat, session_cookie=None):
    path = f"d_forum/{cat}"
    posts = db_req("get_posts", {"forum": cat})
    
    session_cookie = validate_cookie(session_cookie)
    
    if session_cookie:
        return page_view("d_forum/forum", forum=cat, posts=posts, hasSession=True, is_admin=session_cookie[2])


    return page_view("d_forum/forum", forum=cat, posts=posts, has_session=False)


def forum_landing(session_cookie=None):
    # Forum landing page

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("forum", has_session=True, is_admin=session_cookie[2])

    return page_view("forum", has_session=False)

#-----------------------------------------------------------------------------

def forum_post(pid, session_cookie=None):
    # Forum landing post

    session_cookie = validate_cookie(session_cookie)

    res = db_req("get_post_thread", {"id": pid})
    post = res[0]
    replies = res[1:]

    if session_cookie:
        return page_view("d_forum/forum_post", post=post, replies=replies, has_session=True, is_admin=session_cookie[2])


    return page_view("d_forum/forum_post", post=post, replies=replies, has_session=False)


#-----------------------------------------------------------------------------

def forum_new_post(session_cookie=None):
    # Forum landing post

    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.")

    return page_view("d_forum/forum_new_post", has_session=True, is_admin=session_cookie[2])


def forum_create_new_post(post, session_cookie=None):

    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.")

  

    #post_details :(author_id, forum, title, body, parent_id )

    post_dict = {
        "author_id": cookies[session_cookie[0]],
        "forum": post["forum"],
        "title": post["title"],
        "body": post["body"],
        "parent_id": -1,
    } 

    for key in post_dict:
        if global_san.contains_black_list(post_dict[key]):
            return page_view("error", message="Sorry, your reply could not be added.")
        else:
            post_dict[key] = global_san.sanitize(post_dict[key])

    db_req("add_post",  post_dict)

    return forum_page(post["forum"], session_cookie)

def create_post_reply(post, session_cookie=None):

    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.")

    parent_post = db_req("get_post", {"id": post["parent_id"]})[0]
   
    post_dict = {
        "title": "",
        "body": post["answer"], 
        "forum": parent_post["forum"],
        "parent_id": post["parent_id"],
        "author_id": cookies[session_cookie[0]],
    }

    for key in post_dict:
        if global_san.contains_black_list(post_dict[key]):
            return page_view("error", message="Sorry, your reply could not be added.")
        else:
            post_dict[key] = global_san.sanitize(post_dict[key])


    res = db_req("add_post", post_dict)
  
    if res == False:
        return page_view("error", reason="internal server error", has_session=True)

    return forum_post(post["parent_id"], session_cookie)

    
#-----------------------------------------------------------------------------

def faq(session_cookie=None):
    # Forum landing post
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("faq", has_session = True, is_admin=session_cookie[2]) 

    return page_view("faq") 

#-----------------------------------------------------------------------------

def admin_users():
    users = [{"id": 1, "username": "tharen", "num_posts": 9000000}, {"id": 2, "username": "tharen", "num_posts": 9000000}]
    # "posts": [{"id": 1, "reports": 1000}]},{"username": "tharen", "num_posts": 9000000, "posts": [{"id": 1, "reports": 1000, "title": "bla bla"}]
    return page_view("admin_users", users=users)

def admin_posts(user, session_cookie=None):
    session_cookie = validate_cookie(session_cookie)
    if not session_cookie or not session_cookie[2]:
        page_view("error", message="You do not have permission to view this resource.")
    
    
    

    return page_view("admin_posts", username=username, num_posts=num_posts, posts=posts, has_session=True, is_admin=session_cookie[2])


def del_post(pid, session_cookie=None):
    session_cookie = validate_cookie(session_cookie)
    if not session_cookie or not session_cookie[2]:
        return 
    try:
        pid = int(pid)
        params = {"id": pid}
    except ValueError:
        return
    db_req("delete_post", params)

            
def del_user(uid, session_cookie=None):
    session_cookie = validate_cookie(session_cookie)
    if not session_cookie or not session_cookie[2]:
        return 
    try:
        uid = int(uid)
        params = {"id": uid}
    except ValueError:
        return
    db_req("delete_user", params)

