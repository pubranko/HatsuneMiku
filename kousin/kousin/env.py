import os

'''
solrにアクセスするための基本情報。
ただし、当env.pyと同じ階層にsolr-keystore.pemがあることを前提とする。
'''
class SolrEnv():
    def keystore_get():
        return os.path.dirname(os.path.abspath(__file__))+'/ここにapache solrにアクセスするための公開鍵ファイルを指定'
    URL = 'https://localhost:ポート/solr/'
    CORE = 'コア名/'
    VERIFY = keystore_get()
    READ_USER='参照権限ユーザー名'
    READ_PASS='パスワード'

'''
twitterにアクセスするための基本情報
'''
class TwitterEnv():
    CONSUMER_KEY = ''
    CONSUMER_SECRET = ''
    ACCESS_TOKEN = ''
    ACCESS_TOKEN_SECRET = ''

