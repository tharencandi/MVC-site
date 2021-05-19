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
    }
    HOST, PORT = "localhost", 9999
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(len(bytes(json.dumps(query), encoding="utf-8")))
    sock.sendall(bytes(json.dumps(query), encoding="utf-8"))
    data = sock.recv(2048)
    if data != None:
        received = json.loads(data.decode())
        return received
    return None


def hash_password(password, salt):
    #hash once to avoid bcrypt password truncation`
    m = hashlib.sha512()
    m.update(password.encode())
    hashed_password = m.digest()

    #generate salt if none exist
    if salt == None:
        salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(hashed_password, salt)
    return hashed_password, salt

def create_cookie(user_id, is_admin = False):
    cookie = secrets.token_hex(16)
    cookies[cookie] = [user_id, datetime.now(), is_admin]
    return cookie

"""Ensures a cookie exists and hasn't expired. If it exists and hasn't expired,
expiry time is reset to 5 minutes from current time"""
def validate_cookie(cookie):
    #no cookie
    if not cookie:
        return None

    res = None
    try:
        # check if cookie exists in the dictionary
        if cookie in cookies:
            #calculate expiry date 
            birth_time = cookies.get(cookie)[1]
            now = datetime.now()
            tdelta = now - birth_time
            delta_threshold = timedelta(minutes=5)
            
            # cookie has expired
            if tdelta > delta_threshold:
                cookies.pop(cookie)

            #cookie is valid
            else:
                exp_time = now + timedelta(minutes=5)
                cookies.get(cookie)[1] = exp_time
                res = cookies.get(cookie)

    #Exception processing cookie
    except Exception as e:
        print("error in validation")
        print(e)
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
    
    #validate cookie
    session_cookie = validate_cookie(session_cookie)

    #cookie render front end for logged in user
    if session_cookie:
        return page_view("index", has_session=True, is_admin=session_cookie[2])
    
    #no session so render for non signedup user
    return page_view("index", has_session=False, is_admin=False)

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form(session_cookie=None):
    '''
        login_form
        Returns the view for the login_form
    '''

    #validate cookie
    session_cookie = validate_cookie(session_cookie)

    #cookie render front end for logged in user
    if session_cookie:
        return page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2])

    #no session so render for non signedup user
    return page_view("login", has_session=False, is_admin=False)

#-----------------------------------------------------------------------------
def logout(session_cookie=None):

    #invalid path if not logged in
    if not session_cookie:
        return page_view("error", message="You are not logged in.", has_session=False, is_admin=False)
    
    # attempt to delete session to logout
    else:
        if session_cookie in cookies:
            del cookies[session_cookie]

        return page_view("index", has_session=False, is_admin=False)
        

  
# Check the login credential
def login_check(username, password, session_cookie=None):

    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    
    #check for session
    session_cookie = validate_cookie(session_cookie)

    # if session already exists don't attempt to log in
    if session_cookie:
        return (page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2]), None)
    
    # get salt corresponding to username 
    db_res = db_req("get_salt_by_username", {"username": username})
    
    # if database response is malformed or failed, return error page and stop login
    if not db_res or not "data" in db_res or not db_res["data"]:
        return (page_view("error", message="Incorrect username or password", has_session=False, is_admin=False), None)
    
    salt = db_res["data"][0]["salt"]
    
    #hash the input password with stored salt
    hashed_password, salt = hash_password(password, salt.encode())
    
    # get stored hash of password from db
    res = db_req("check_credentials", {"username": username, "password": hashed_password.decode(),})
    
    # check if password matched
    if res["status"] == False :
        err_str = "Incorrect username or password"
        return (page_view("error", message=err_str, has_session=False, is_admin=False), None)

    # check if user is banned
    elif res["is_banned"]:
        return (page_view("error", message="Nah bro your toxic af", has_session=False, is_admin=False), None)
    # proceed with login. create cookie 
    else:
        cookie = create_cookie(res["id"], res['is_admin'])
        # sanitize username 
        return (page_view("success", name=global_san.sanitize(username), has_session=True, is_admin=res["is_admin"]), cookie)
 
        

def signup_form(session_cookie=None):
    '''
        signup_form
        Returns the view for the signup_form
    '''
    
    session_cookie = validate_cookie(session_cookie)
    
    # already logged in
    if session_cookie:
        return page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2])

    return page_view("signup", has_session=False, is_admin=False)




def create_user(username, password, confirm_password, session_cookie=None):
    '''
        User sign up logic
        Returns success page if success,
        error page if failed with reasons defined here or sql.
    '''

    # check if already logged in and fail if so
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return (page_view("error", message="Please logout before creating a user", has_session=True, is_admin=session_cookie[2]), None)
    
    # check all fields are available
    if username == None or password == None or confirm_password == None:
        return (page_view("error", message="Internal server error", has_session=False, is_admin=False), None)
    
    # check if username has banned characters or phrases. Fail if so
    if global_san.contains_black_list(username):
        return (page_view("error", message="That username is not allowed", has_session=False, is_admin=False), None)
    
    # check password confirmation passed
    if password != confirm_password:
        return (page_view("error", message="Password does not match!", has_session=False, is_admin=False), None)

    # hash password and store in database
    hashed_password, salt = hash_password(password=password, salt=None)
    res = db_req("add_user", {'username': username, 'password': hashed_password.decode(), "salt": salt.decode(), "is_admin": 0})
    
    # check storage of has succeeded
    if res["status"] == True:
        cookie = create_cookie(res["id"], res["is_admin"]) 
        return (page_view("success", name=global_san.sanitize(username), has_session=True, is_admin=False), cookie)

    else:
        return (page_view("error", message=global_san.sanitize(res["message"]), has_session=False, is_admin=False), None)

    
#----------------------------------------------------------------------------

def content_index(cat, session_cookie=None):
    path = "content"

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
            return page_view("content", has_session=True, is_admin=session_cookie[2])

    return page_view("content", has_session=False, is_admin=False)

#-----------------------------------------------------------------------------

def content(cat, sub_cat, session_cookie=None):
    # add type information and any other template vars to page view function
    path = "d_content/" + cat + "/" + sub_cat

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
            return page_view(path, has_session=True, is_admin=session_cookie[2])
    
    return page_view(path, has_session=False, is_admin=False)

#-----------------------------------------------------------------------------

def forum_page(cat, gid=None, session_cookie=None):
    path = f"d_forum/{cat}"
    if not gid:
        gid = 0

    print("here")

    db_res = db_req("get_posts", {"forum": cat, "gid": gid})
    posts = db_res["data"]
    
    session_cookie = validate_cookie(session_cookie)
    
    if session_cookie:
        return page_view("d_forum/forum", forum=cat, posts=posts, has_session=True, is_admin=session_cookie[2])


    return page_view("d_forum/forum", forum=cat, posts=posts, has_session=False, is_admin=False)


def forum_landing(session_cookie=None):
    # Forum landing page

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("forum", has_session=True, is_admin=session_cookie[2])

    return page_view("forum", has_session=False, is_admin=False)

#-----------------------------------------------------------------------------

def forum_post(pid, session_cookie=None):
    # Forum landing post
    session_cookie = validate_cookie(session_cookie)

    db_res = db_req("get_post_thread", {"id": pid})
    post = db_res["data"][0]
    replies = db_res["data"][1:]

    if session_cookie:
        return page_view("d_forum/forum_post", post=post, replies=replies, has_session=True, is_admin=session_cookie[2])


    return page_view("d_forum/forum_post", post=post, replies=replies, has_session=False, is_admin=False)


#-----------------------------------------------------------------------------

def forum_new_post(session_cookie=None):
    # Forum landing post

    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.", has_session=False, is_admin = False)

    return page_view("d_forum/forum_new_post", has_session=True, is_admin=session_cookie[2])


def forum_create_new_post(post, session_cookie=None):
    
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.", has_session=False, is_admin=False)

  
    title_len = len(post["title"])
    print(title_len)
    body_len = len(post["body"])
    print(body_len)
    if (title_len + body_len) > 1000:
        return page_view("error", message="Sorry your post was to big and won't be added.", has_session=True, is_admin=session_cookie[2])
    post_dict = {
        "author_id": session_cookie[0],
        "forum": post["forum"],
        "title": post["title"],
        "body": post["body"],
        "parent_id": -1,
    } 

    if global_san.contains_black_list(post_dict["title"]) or global_san.contains_black_list(post_dict["body"]):
        return page_view("error", message="Sorry, your reply could not be added.", has_session=True, is_admin=session_cookie[2])
    else:
        post_dict["title"] = global_san.sanitize(post_dict["title"])
        post_dict["body"] = global_san.sanitize(post_dict["body"])

    db_req("add_post",  post_dict)

    return forum_page(post["forum"], raw_cookie)

def create_post_reply(post, session_cookie=None):
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.", has_session=False, is_admin=False)
    
    parent_post = db_req("get_post", {"id": post["parent_id"]})
    if not parent_post["status"]:
            return page_view("error", message="Sorry, your reply could not be added.", has_session=True, is_admin=session_cookie[2])
    else:
        res = parent_post["data"][0]

   
    post_dict = {
        "title": "reply",
        "body": post["answer"], 
        "forum": res["forum"],
        "parent_id": post["parent_id"],
        "author_id": session_cookie[0],
    }

    if global_san.contains_black_list(post_dict["title"]) or global_san.contains_black_list(post_dict["body"]):
        return page_view("error", message="Sorry, your reply could not be added.", has_session=True, is_admin=session_cookie[2])
    else:
        post_dict["title"] = global_san.sanitize(post_dict["title"])
        post_dict["body"] = global_san.sanitize(post_dict["body"])


    res = db_req("add_post", post_dict)
  
    if res == False:
        return page_view("error", reason="internal server error", has_session=True, is_admin=session_cookie[2])

    return forum_post(post["parent_id"], raw_cookie)

    
#-----------------------------------------------------------------------------

def faq(session_cookie=None):
    # Forum landing post
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("faq", has_session = True, is_admin=session_cookie[2]) 

    return page_view("faq", has_session=False, is_admin=False) 

def about(session_cookie=None):
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("about", has_session=True, is_admin=session_cookie[2])

    return page_view("about", has_session=False, is_admin=False)
#-----------------------------------------------------------------------------

def admin_users(session_cookie=None):
    session_cookie = validate_cookie(session_cookie)

    if not session_cookie:
        page_view("error", message="Permission Denied.", has_session=False, is_admin=False)

    elif not session_cookie[2]:
        page_view("error", message="Permission Denied.", has_session=True, is_admin=False)

    else:
        res = db_req("get_users", None)
        return page_view("admin_users", users=res["data"], has_session=True, is_admin=True)

def admin_posts(user, session_cookie=None):
    session_cookie = validate_cookie(session_cookie)

    if not session_cookie:
        page_view("error", message="You do not have permission to view this resource.", has_session=False, is_admin=False)

    if not session_cookie[2]:
        page_view("error", message="You do not have permission to view this resource.", has_session=True, is_admin=False)

    res = db_req("get_user", {"id": user})
    if res:
        res = res["data"][0]
        username = res["username"]
        posts_res = db_req("get_user_posts", {"id": user})

        if posts_res:
            if posts_res["status"]:
                posts = posts_res["data"]
                num_posts = len(posts)
            else:
                page_view("error", message="Can't retrieve posts.", has_session=True, is_admin=session_cookie[2])

        else:
            page_view("error", message="Can't retrieve posts.", has_session=True, is_admin=session_cookie[2])

    else:
        page_view("error", message="Can't retrieve posts.", has_session=True, is_admin=session_cookie[2])
    
    return page_view("admin_posts", username=username, num_posts=num_posts, posts=posts, has_session=True, is_admin=session_cookie[2])


def del_post(pid, session_cookie=None):
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)

    if not session_cookie:
        return page_view("error", message="Permission denied hombre", has_session=False, is_admin=False)
    if not session_cookie[2]:
        return page_view("error", message="Permission denied hombre", has_session=True, is_admin=False)
    try:
        pid = int(pid)
        params = {"id": pid}
    except ValueError:
        return page_view("error", message="not a post", has_session=True, is_admin=True)

    res = db_req("delete_post", params)
    
    return admin_posts(session_cookie[0], session_cookie=raw_cookie)


def report_post(pid, session_cookie=None):
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Permission denied hombre", has_session=False, is_admin=False)
    
    try:
        pid = int(pid)
        params = {"id": pid}
    except ValueError:
        return page_view("error", message="not a post", has_session=True, is_admin=session_cookie[2])
    res = db_req("report_post", params)

    res2 =  db_req("get_post", params)
    if not res2 or not "status" in res2 or not res2["status"]:
        return page_view("error", message="woops", has_session=True, is_admin=session_cookie[2])

    if res2["data"][0]["parent_id"] != -1:
        pid = res2["data"][0]["parent_id"]

    return forum_post(pid, session_cookie=raw_cookie)

   
    


def ban_user(uid, session_cookie=None):
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)

    if not session_cookie:
        return page_view("error", message="Absolutely not!.", has_session=False, is_admin=False)

    if not session_cookie[2]:
        return page_view("error", message="Absolutely not sir.", has_session=True, is_admin=False)

    try:
        uid = int(uid)
        params = {"id": uid}
    except ValueError:
        return

    if uid == session_cookie[0]:
        return page_view("error", message="Are you ok? Please contact a helpline xx", has_session=True, is_admin=True)
    
    to_remove = None
    for k,v in cookies.items():
        if v[0] == uid:
            to_remove = k
    if to_remove:
        cookies.pop(to_remove)

    res = db_req("ban_user", params)

    return admin_users(session_cookie=raw_cookie)

def unban_user(uid, session_cookie=None):
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)

    if not session_cookie:
        return page_view("error", message="Absolutely not!", has_session=False, is_admin=False)

    if not session_cookie[2]:
        return page_view("error", message="Absolutely not sir.", has_session=True, is_admin=False)
    try:
        uid = int(uid)
        params = {"id": uid}
    except ValueError:
        return page_view("error", message="not a user", has_session=True, is_admin=session_cookie[2])

    res = db_req("unban_user", params)

    return admin_users(session_cookie=raw_cookie)


