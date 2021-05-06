import redis


class Redis_Session_Client:
    def __init__(self, host = None, port = None, db = None, session_length=None):
        self.host = host
        self.port = port
        self.db = db
        self.Redis = None
        self.new_redis(host = host, port = port, db = db)
        self.ConnectionCheck()
        
        self.defualt_session = session_length

    def new_redis(self, host = None, port = None, db = None): 
        if (host is not None) and (port is not None) and (db is not None):
            self.host = host
            self.port = port
            self.db = db
            self.Redis = redis.Redis(host = host, port = port, db = db)
            return self.Redis

    def ConnectionCheck(self):
        if not self.Redis.ping():
            raise ConnectionError

    def validate_session(self, user_id, cookie_secret):
        check = self.Redis.get(user_id)

        if check == cookie_secret:
            return True
        
        return False
    
    def add_session(self, user_id, session_length=None):
        # generate or whatever we use for cookies 













