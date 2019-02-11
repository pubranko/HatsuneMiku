from pymongo import MongoClient
import pickle
from bs4 import BeautifulSoup as bs4
from dateutil import parser
from datetime import datetime
import os,sys
import pysolr
#from ranko.env  import MongoEnv,SolrEnv
#from ranko.scraper import scraping_control
#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.abspath(__file__))).rsplit('/',1)[0]    #当モジュールの1つ上の絶対パス
sys.path.append(path)                                                   #それをモジュールライブラリに追加。
from env  import MongoEnv,SolrEnv       #プロジェクト内モジュール
from scraper import scraping_control    #プロジェクト内モジュール
#-----

def scraping(key_url,key_response_time):
    print('=== solr_add  queue_recieved start: ',key_url,key_response_time)
    '''
    MongoDB：コネクション作成。引数のurlが存在するかチェック。
    '''
    client = MongoClient(MongoEnv.CLIENT, MongoEnv.PORT)
    client[MongoEnv.DB].authenticate(MongoEnv.USER,MongoEnv.PASS)
    db = client[MongoEnv.DB]
    collection = db[MongoEnv.COLLECTION]

    doc = collection.find_one({'url' : key_url,'response_time':key_response_time})
    if  doc == None:
        print('=== solr_add  MongoDBにurlが無いぞ',key_url)
        raise 
    
    '''
    urlがMongoDBに存在した場合、MongoDBよりurl、各レスポンスを取得する。
    '''
    mongo_id = doc['_id']
    url = doc['url']
    response_time = doc['response_time']
    #response_last_modified = doc['response_last_modified']
    response_headers = pickle.loads(doc['response_headers'])
    response_body = pickle.loads(doc['response_body'])

    #本文の抽出
    #title,article = scrape_article(response_body,key_url,__name__)
    #title,article = scraping_control.controller(response_body,url,__name__)
    title,article,publish_date,issuer = scraping_control.controller(response_body,url,__name__)

    #件名、本文、公開日、発行者の抽出チェック
    if  title == '':
        print('=== solr_add  MongoDBから件名(title)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
        return
    if  article == '':
        print('=== solr_add  MongoDBから本文(article)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
        return
    if  publish_date == '':
        print('=== solr_add  MongoDBから公開日(publish_date)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
        return
    if  issuer == '':
        print('=== solr_add  MongoDBから発行者(issuer)が抜き出しできなかった → 異常を検知 → 登録回避',key_url)
        return

    '''
    solr重複チェック：url,title,articleが完全一致するものがあれば登録しない。
    '''
    solr = pysolr.Solr(
        SolrEnv.URL+SolrEnv.CORE,
        timeout=10,
        verify=SolrEnv.VERIFY,
        auth=(SolrEnv.ADD_USER,SolrEnv.ADD_PASS),
        always_commit=True,
        )

    results = solr.search(['url:"'+url+'"'],**{
        'sort': 'response_time desc,',      #ソートのやり方。 desc降順 asc昇順。 %20は空白に置き換えること。
        })

    for result in results:                              #複数の検索結果を1つづつ処理
        #print('=== queue_recieved solrのresults: ',result)
        solr_chk_flg = True         #不一致無し＝True、不一致有り＝False
        #if result['url']!=url:
        #    solr_chk_flg = False
        if result['title']!=title:
            solr_chk_flg = False

        try:    #articleが正常にスクレイピングされていない場合がありうる。
            if result['article']!=article:
                solr_chk_flg = False
        except:
            solr_chk_flg = False

        if result['publish_date']!=publish_date:
            solr_chk_flg = False
        if result['issuer']!=issuer:
            solr_chk_flg = False

        #if result['url']==url and result['title']==title and result['article']==article:
        if solr_chk_flg:
            print('=== solr_add : solrの登録タイトル＆本文が完全一致。登録を回避する。','\n    ',url)
            #raise 
            return

    #print('=== queue_recieved solr.addの手前: ',mongo_id,url,title)
    solr.add([
    {
        "id":mongo_id,
        "url": url,
        "title": title,
        "article": article,
        "response_time" : response_time,
        "publish_date" : publish_date,
        "issuer" : issuer,
        "update_count" : 0,
    },
])