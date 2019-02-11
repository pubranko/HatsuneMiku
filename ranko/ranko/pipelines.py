from scrapy.exceptions import DropItem
from pymongo import MongoClient
from redis import Redis
from rq import Queue
import pickle
import os,sys

#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.abspath(__file__))) #当モジュールディレクトリの絶対パス
sys.path.append(path)                               #それをモジュールライブラリに追加。
from scraper import scraping_control
from env  import MongoEnv,RedisEnv


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class MongoPipeline(object):
    def open_spider(self,spider):                                   #spider開始時にmongodbへ接続する。
        print('=== MongoPipeline > open_spider ===')

        self.client = MongoClient(MongoEnv.CLIENT, MongoEnv.PORT)           #コネクション作成
        self.client[MongoEnv.DB].authenticate(MongoEnv.USER,MongoEnv.PASS)  #コネクションから、指定したデータベースに認証。
        self.db = self.client[MongoEnv.DB]                                  #コネクションから指定データベースを取得
        self.collection = self.db[MongoEnv.COLLECTION]                      #指定データベースからitemsコレクションを取得。なければ新規作成

        '''
        重要！！！！！！  コレクションの中身を初期化したい場合のみ、この行を有効にする。
        '''
        #print('=== MongoPipeline > open_spider mongoDBのコレクションを初期化モードがONになっています！===')
        #self.collection.remove()

    def close_spider(self,spider):                                  #spider終了時にmongodbへの接続を切断。
        print('=== MongoPipeline > close_spider ===')
        self.client.close()

    def process_item(self,item,spider):                             #Itemコレクションに追加する。
        #print('=== MongoPipeline > process_item ===',item)

        #クロール中のレスポンスよりタイトルと本文を抽出。
        title,article,publish_date,issuer = scraping_control.controller(pickle.loads(item['response_body']),item['url'],__name__)

        #スクレイピングにより対象のデータを抜き出しできたかチェック
        if title == False:
            raise DropItem('=== MongoPipeline クロールしたがタイトル抜き出しができなかった → 異常を検知 → 登録回避',item['url'])
        if article == False:
            raise DropItem('=== MongoPipeline クロールしたが本文抜き出しができなかった → 異常を検知 → 登録回避',item['url'])
        if publish_date == False:
            raise DropItem('=== MongoPipeline クロールしたが公開日抜き出しができなかった → 異常を検知 → 登録回避',item['url'])

        #まだDBに登録されていない新規のurlの場合、mongodbへ追加。
        if self.collection.find({'url' : item['url']}).count() == 0:    
            self.collection.insert_one(dict(item))  #dict：keyのリストと値のリストを辞書形式へ変換。これで、items.pyで短縮したヘッダーやボディーが元に戻る、、、
            print('=== MongoPipeline > process_item でmongodbへ追加 ===',item['url'])
            return item     #ここでitemを返さないと、後続のpipelineでitemが見れなくなることが分かった。                        

        #既に同一urlの登録があった場合、MongoDBよりクロール中のurlと同じurlのドキュメントの有無をチェック。
        for doc in self.collection.find({'url' : item['url']}):

            #今回のurlからMongoDBを参照。登録されているbodyからタイトル、本文、公開日を抽出。
            db_title,db_article,db_publish_date,db_issuer = scraping_control.controller(pickle.loads(doc['response_body']),doc['url'],__name__)
            if db_title == False:
                raise DropItem('=== MongoPipeline : 重複チェック先のDBからタイトル抜き出しができなかった → 異常を検知 → 登録回避',item['url'])
            if db_article == False:
                raise DropItem('=== MongoPipeline : 重複チェック先のDBから本文抜き出しができなかった → 異常を検知 → 登録回避',item['url'])
            if db_publish_date == False:
                raise DropItem('=== MongoPipeline : 重複チェック先のDBから公開日抜き出しができなかった → 異常を検知 → 登録回避',item['url'])

            #クロール中のurl、タイトル、本文、公開日が一致するデータがMongoDBに存在した場合、登録しないよう回避。
            if item['url']==doc['url'] and title==db_title and article==db_article and publish_date==db_publish_date:   
                raise DropItem('=== MongoPipeline : MongoDBの登録タイトル＆本文が完全一致。登録を回避する。','\n    ',item['url'])

        self.collection.insert_one(dict(item)) #同一urlの登録はあるが、タイトルか本文が更新されている。新しい情報を別に保存する。
        return item         #ここでitemを返さないと、後続のpipelineでitemが見れなくなることが分かった。

class RQPipeline:
    def open_spider(self,spider):
        conn = Redis(RedisEnv.CLIENT,RedisEnv.PORT, db=RedisEnv.DB)        #redisに接続
        self.queue = Queue(RedisEnv.WORKER,connection=conn)  
    def process_item(self,item,spider):
        #print('=== RQPipeline process_item ',item)
        #self.queue.enqueue('ranko.scraper.sankei_com_sc1.scrape_v1',item['url'],result_ttl=0)
        self.queue.enqueue(RedisEnv.SCRIPT,item['url'],item['response_time'],result_ttl=0)
        return item
