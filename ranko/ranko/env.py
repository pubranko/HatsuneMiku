import os
class  MongoEnv():
    CLIENT = 'localhost'
    PORT = ''
    USER = ''
    PASS = ''
    DB = ''
    COLLECTION = ''

class SolrEnv():
    def keystore_get():
        return os.path.dirname(os.path.abspath(__file__))+'/solrの公開鍵'
    URL = ''
    CORE = ''
    VERIFY = keystore_get()
    ADD_USER=''
    ADD_PASS=''
    READ_USER=''
    READ_PASS=''
    
class TwitterEnv():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''

class YoutubeEnv():
    YOUTUBE_API_KEY = ''

class RedisEnv():
    CLIENT = 'localhost'
    PORT = 
    DB = 
    WORKER = ''
    SCRIPT = ''
