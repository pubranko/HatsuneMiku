#!/bin/python3
import pymongo
from pymongo import MongoClient
import pysolr
from bs4 import BeautifulSoup as bs4
from dateutil import parser
from datetime import datetime
import pickle
import sys, os
#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.abspath(__file__))).rsplit('/',1)[0]    #当モジュールの1つ上の絶対パス
sys.path.append(path)                                                   #それをモジュールライブラリに追加。
from env  import MongoEnv,SolrEnv       #プロジェクト内モジュール
from scraper import scraping_control    #プロジェクト内モジュール
from queue_recieved import solr_add     #プロジェクト内モジュール
#-----

def sync_check(mongo_select):
    '''
    1.mongodbにあるのにsolrに無もの全件チェック
    2.指定期間のレスポンスタイムのmongodbに限定チェック
    3.mongodbの接続先を、サーバーと自端末の切り替えできるようにする。
    4.
    '''
    
    client = MongoClient(MongoEnv.CLIENT, MongoEnv.PORT)
    client[MongoEnv.DB].authenticate(MongoEnv.USER,MongoEnv.PASS)
    db = client[MongoEnv.DB]
    collection = db[MongoEnv.COLLECTION]

    solr = pysolr.Solr(
        SolrEnv.URL+SolrEnv.CORE,
        timeout=10,
        verify=SolrEnv.VERIFY,
        auth=(SolrEnv.ADD_USER,SolrEnv.ADD_PASS),
        always_commit=True,
    )

    col_cnt = collection.find(mongo_select).count()     #mongodbの全件の件数
    #col_cnt = collection.find({'_id':{'$regex':'2019-01-20'}}).count()     #mongodbの全件の件数
    #col_cnt = collection.find({"_id" : "sankei.com@2019-01-20@19:24:59.014960"}).count()     #mongodbの全件の件数
    
    print('=== select対象件数 =',col_cnt)
    one_time = 100                          #一回に取得する件数。
    col_cnt = col_cnt + one_time            #最後の１回のループを動かすために加算
    asynchronous = []                       #非同期リスト初期化

    for cnt in range(0,col_cnt,one_time):     #一回分ごとにループ。
        print('=== cnt = ',cnt)

        #for doc in collection.find(mongo_select).skip(cnt - one_time).limit(one_time).sort('response_time',1):
        for doc in collection.find(mongo_select).skip(cnt).limit(one_time):

            mongo_id = doc['_id']
            url = doc['url']
            response_time = doc['response_time']
            #response_last_modified = doc['response_last_modified']
            #response_headers = pickle.loads(doc['response_headers'])
            response_body = pickle.loads(doc['response_body'])
            title,article,publish_date,issuer = scraping_control.controller(response_body,url,__name__)

            #本文の抽出チェック
            if  article == '':
                print('=== solr_recovery  MongoDBから件名(title)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
                raise 
            if  article == '':
                print('=== solr_recovery  MongoDBから本文(article)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
                raise 
            if  publish_date == '':
                print('=== solr_recovery  MongoDBから公開日(publish_date)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
                raise 
            if  issuer == '':
                print('=== solr_recovery  MongoDBから発行者(issuer)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
                raise 

            results = solr.search(['id:"'+mongo_id+'"'],)                                               
            if results:
                result = results.docs[0]                     #イテレータ的なものであるため、それの要素を単独にしている。

                chk_flg = True
                if result['url']!=url:
                    chk_flg = False
                if result['title']!=title:
                    chk_flg = False

                try:    #articleが正常にスクレイピングされていない場合がありうる。
                    if result['article']!=article:
                        chk_flg = False
                except:
                    chk_flg = False

                #if result['url']==url and result['title']==title and result['article']==article:
                if chk_flg:
                    pass #print(doc['url'],'OK')
                else:
                    #print(doc['url'],'solrのデータを改竄されたかも！')
                    asynchronous.append([mongo_id,url,response_time,'solrのデータを改竄？'])
            else:
                #print(doc['url'],'solrにまだ登録されていない')
                asynchronous.append([mongo_id,url,response_time,'solr未登録'])

    return asynchronous

def  recovery(lists):
    '''
    1.指定されたmongodbの_idを、solrへ流し込む。
    2.sync_checkから受け取ったリストをもとに行うことが可能。
    3.main関数から直接指定が可能。
    '''
    #lists = sync_check()
    for lst in lists:
        solr_add.scraping(lst[1],lst[2])

if __name__ == '__main__':
    '''
    mongo_select = {
        '$and': [
            {'publish_date':{ '$gte' : datetime(2018,3,1,0,0,0,0)}},
            {'publish_date':{ '$lt'  : datetime(2018,3,2,0,0,0,0)}}    
        ]
    }
    mongo_select = {'_id':{'$regex':'2019-01-20'}}
    '''

    '''
    mongo_select = {'_id':{'$regex':'asahi'}}

    lists = sync_check(mongo_select)
    #非同期リストをファイルに保存。（時間かかるのでリストをファイルに保存し、再実行をやりやすくする。）
    file = open('asynchronous.list','wb')
    pickle.dump(lists, file)
    file.close
    '''

    file = open('asynchronous.list','rb')
    lists = pickle.load(file)
    file.close
    
    #lists = file

    for lst in lists:
        print('=== lstの中身 ',lst)
    
    recovery(lists)


