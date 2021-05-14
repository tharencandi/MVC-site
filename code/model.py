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
    print(paramaters)
    print(function)


    query = {
        "function": function,
        "params": paramaters,
        "auth": "password",      
    }
    HOST, PORT = "localhost", 9999
    # SOCK_DGRAM is the socket type to use for UDP sockets
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(bytes(json.dumps(query), encoding="utf-8"))
    data = sock.recv(2048)
    if data != None:
        received = json.loads(data.decode())
        return received
    return None


def hash_password(password, salt):
    m = hashlib.sha512()
    m.update(password.encode())
    hashed_password = m.digest()
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
    if not cookie:
        return None

    res = None
    try:
        if cookie in cookies:
            print("cookie exists")
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
        print("error")
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

    return page_view("index", has_session=False, is_admin=False)

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
    return page_view("login", has_session=False, is_admin=False)

#-----------------------------------------------------------------------------
def logout(session_cookie=None):
    if not session_cookie:
        return page_view("error", message="You are not logged in.", has_session=False, is_admin=False)
    else:
        print(session_cookie)
        print(cookies[session_cookie])
        del cookies[session_cookie]
        return page_view("index", has_session=False, is_admin=False)
        

  
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

    print("check_credentials")
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return (page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2]), None)

    db_res = db_req("get_salt_by_username", {"username": username})
    print(db_res)

    if not db_res or not "data" in db_res or not db_res["data"]:
        return (page_view("error", message="Incorrect username or password", has_session=False, is_admin=False), None)
    
    print(db_res)
    salt = db_res["data"][0]["salt"]

    hashed_password, salt = hash_password(password, salt.encode())

    res = db_req("check_credentials", {"username": username, "password": hashed_password.decode(),})

    if res["status"] == False :
        print("hello")
        err_str = "Incorrect username or password"
        return (page_view("error", message=err_str, has_session=False, is_admin=False), None)
    elif res["is_banned"]:
        return (page_view("error", message="Nah bro your toxic af", has_session=False, is_admin=False), None)
    else:

        cookie = create_cookie(res["id"], res['is_admin'])
     
        return (page_view("success", name=global_san.sanitize(username), has_session=False, is_admin=False), cookie)
 
        

def signup_form(session_cookie=None):
    '''
        signup_form
        Returns the view for the signup_form
    '''

    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return page_view("error", message="You are already signed in.", has_session=True, is_admin=session_cookie[2])

    return page_view("signup", has_session=False, is_admin=False)




def create_user(username, password, confirm_password, session_cookie=None):
    '''
        User sign up logic
        Returns success page if success,
        error page if failed with reasons defined here or sql.
    '''
    session_cookie = validate_cookie(session_cookie)
    if session_cookie:
        return (page_view("error", message="Please logout before creating a user", has_session=True, is_admin=session_cookie[2]), None)

    if username == None or password == None or confirm_password == None:
        return (page_view("error", message="Internal server error", has_session=False, is_admin=False), None)
    
    ##### Doesn't black list script tags need to fix
    if global_san.contains_black_list(username):
        return (page_view("error", message="That username is not allowed", has_session=False, is_admin=False), None)

    if password != confirm_password:
        return (page_view("error", message="Password does not match!", has_session=False, is_admin=False), None)

    print(password)
    hashed_password, salt = hash_password(password=password, salt=None)
    res = db_req("add_user", {'username': username, 'password': hashed_password.decode(), "salt": salt.decode(), "is_admin": 0})
   
    if res["status"] == True:
        cookie = create_cookie(res["id"], res["is_admin"]) 
        return (page_view("success", name=global_san.sanitize(username), has_session=True, is_admin=False), cookie)
    else:
        print(res)
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

def forum_page(cat, session_cookie=None):
    path = f"d_forum/{cat}"
    db_res = db_req("get_posts", {"forum": cat})
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

    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.", has_session=False, is_admin=False)

  

    #post_details :(author_id, forum, title, body, parent_id )
    print(cookies)
    print(session_cookie)
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

    return forum_page(post["forum"], session_cookie)

def create_post_reply(post, session_cookie=None):

    session_cookie = validate_cookie(session_cookie)
    if not session_cookie:
        return page_view("error", message="Please log in to post.", has_session=False, is_admin=False)
    
    print(post)
    print(post["parent_id"])
    print(post["answer"])
    parent_post = db_req("get_post", {"id": post["parent_id"]})
    if not parent_post["status"]:
            return page_view("error", message="Sorry, your reply could not be added.", has_session=True, is_admin=session_cookie[2])
    else:
        res = parent_post["data"][0]

    print(parent_post)
   
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

    return forum_post(post["parent_id"], session_cookie)

    
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
        print("no cookie")
        page_view("error", message="Permission Denied.", has_session=False, is_admin=False)
    elif not session_cookie[2]:
        print("isnt admin")
        page_view("error", message="Permission Denied.", has_session=True, is_admin=False)
    else:
        res = db_req("get_users", None)
        print("ADMIN DATA", res)

        return page_view("admin_users", users=res["data"], has_session=True, is_admin=True)

def admin_posts(user, session_cookie=None):
    session_cookie = validate_cookie(session_cookie)
    print("ADMIN POSTSSSSSS")
    if not session_cookie:
        page_view("error", message="You do not have permission to view this resource.", has_session=False, is_admin=False)
    if not session_cookie[2]:
        page_view("error", message="You do not have permission to view this resource.", has_session=True, is_admin=False)

    res = db_req("get_user", {"id": user})
    print(res)
    if res:
        res = res["data"][0]
        print(res)
        username = res["username"]
        posts_res = db_req("get_user_posts", {"id": user})
        print(posts_res)
        if posts_res:
            if posts_res["status"]:
                posts = posts_res["data"]
                num_posts = len(posts)
        else:
            pass
    else:
        page_view("error", message="Cant find ", has_session=True, is_admin=session_cookie[2])
    
    
    

    return page_view("admin_posts", username=username, num_posts=num_posts, posts=posts, has_session=True, is_admin=session_cookie[2])


def del_post(pid, session_cookie=None):
    print("del_post")
    print(pid)
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)
    print(session_cookie)
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
    
    print("rawest of cookies " + raw_cookie)
    print(session_cookie[0])
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
    print(res2)
    if not res2 or not "status" in res2 or not res2["status"]:
        return page_view("error", message="woops", has_session=True, is_admin=session_cookie[2])
    if res2["data"][0]["parent_id"] != -1:
        pid = res2["data"][0]["parent_id"]

    return forum_post(pid, session_cookie=raw_cookie)

   
    


def ban_user(uid, session_cookie=None):
    print(uid)
    print("ban user request recieved")
    print(session_cookie + "the cooooooookie")
    raw_cookie = session_cookie
    session_cookie = validate_cookie(session_cookie)
    print("cookies user: " + str(session_cookie[0]))
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
    print("unban user request recieved")
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


