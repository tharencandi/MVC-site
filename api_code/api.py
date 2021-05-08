import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/', methods=['GET'])
def home():
        return "<h1>API<h1>"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


"""
    GET ALL POSTS
        - recquired query forum=<subforum>

    TO ADD: 
        - answered filter
        - sort by date?    
"""

@app.route('/api/forum', methods=["GET"])
def get_posts():
    query_paramters = request.args
    forum = query_paramters.get('forum')

    query = """SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE"""
    to_filter = []

    #room to add aditional filters
    if forum:
        query += " forum=? AND"
        to_filter.append(forum)
    if not forum:
       return page_not_found(404)
    
    #remove last AND
    query = query[:-4] + ';'

    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, tuple(to_filter)).fetchall()
    conn.close()
  
    return jsonify(results)
 
    

    
"""
    This will get a specic post, or get all replies to that post

    GET A POST
        - recquired query id=<post id>
        - optional: is_reply=1   
"""
@app.route('/api/post', methods=["GET"])
def get_post():
    query_paramters = request.args
    post_id = query_paramters.get('id')
    is_reply = query_paramters.get('is_reply')

    query = """SELECT p.id, title, body, author_id, username FROM Posts p JOIN Users u ON p.author_id = u.id WHERE"""
    to_filter = []

    if post_id:
    
        if is_reply:
            print("appending is reply")
            query += " p.parent_id=?"
            to_filter.append(post_id)
        else:
            query += " p.id=?"
            to_filter.append(post_id)
            query += " AND p.parent_id=?"
            to_filter.append(-1)

    if not post_id:
        return page_not_found(404)
    
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    results = cur.execute(query, tuple(to_filter)).fetchall()
    conn.close()
  
    return jsonify(results)

app.run(port='5001')


