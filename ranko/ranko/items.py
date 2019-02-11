import scrapy
#このクラスの名前は任意のようだ。明示的に呼び出している所とだけリンクさせれば良いようだ。
#class Sankei_Com(scrapy.Item):
class NewsDB_Item(scrapy.Item):
    _id = scrapy.Field()
    response_time = scrapy.Field()
    #response_last_modified = scrapy.Field()
    url = scrapy.Field()
    response_headers = scrapy.Field()
    response_body = scrapy.Field()

    #ログへの出力時、長くなりすぎないように工夫しているようだ、、、難しいw
    def __repr__(self):
        #print('=== items.py ===')   #pipelinesのprocess_itemより呼び出されているようだ、、、
        p = NewsDB_Item(self)              #当クラスのurl,title,contentを引数に、当クラスのインスタンス化をしているようだ。
        p['response_headers'] = p['response_headers'][:10]
        p['response_body'] = p['response_body'][:10]
        return super(NewsDB_Item,p).__repr__()     #super。クラスの多重継承（？）ができるらしい。初心者には難しいよ〜、、、
