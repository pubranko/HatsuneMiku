#!/usr/bin/python3
'''
スクレイピングのテスト用ロジック。
'''
def scraping_control_test():
    import urllib.request,urllib.error
    import os,sys
    path = (os.path.dirname(os.path.abspath(__file__))).rsplit('/',1)[0]    #当モジュールの1つ上の絶対パス
    sys.path.append(path)                                                   #それをモジュールライブラリに追加。
    from scraper import scraping_control    #プロジェクト内モジュール

    url = 'https://www.sankei.com/politics/news/180430/plt1804300012-n1.html'
    response = urllib.request.urlopen(url)
    #print('=== response.read : ',response.read())
    title,article,publish_date,issuer = scraping_control.controller(response.read(),url,__name__)
    print('=== 結果 title:',title)
    print('=== 結果 article:',article)
    print('=== 結果 publish_date:',publish_date)
    print('=== 結果 issuer:',issuer)

def queue_recieved_test():
    import urllib.request,urllib.error
    import os,sys
    path = (os.path.dirname(os.path.abspath(__file__))).rsplit('/',1)[0]    #当モジュールの1つ上の絶対パス
    sys.path.append(path)                                                   #それをモジュールライブラリに追加。
    
    from queue_recieved import solr_add
    from datetime import datetime
    
    url='https://www.sankei.com/column/news/190113/clm1901130002-n1.html'
    response_time = datetime(2019,1,16,23,18,15,961068)
    
    solr_add.scraping(url,response_time) 


if __name__ == '__main__':

    #scraping_control_test()
    queue_recieved_test()

'''
def elastic_test():
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import connections,Search   #Keyword,Integer
    from elasticsearch import xpack.security.SecurityClient

    esc = SecurityClient({"username": "elasticsearch","roles": ["admin",],})



    #client['sankei_com'].authenticate('USER_sankei_com', 'tekitouDA852')

    client = Elasticsearch(hosts=['localhost:9200'], timeout=20)
    #client = Elasticsearch(
    #    { 'host' : 'localhost' , 'port' : 9200 , 'url_prefix' : 'es' , 'use_ssl' : True, 'timeout' : 20 },
    #)
    print(client.info)

    #UnoTenniMakase673

    #s = Search(using=client,index='news-v0.0.2').query('match_phrase', url='https://www.sankei.com/politics/news/130101/plt1301010001-n1.html')
    #for hit in s:
    #    print(hit.url,'\n',hit.title)
'''
