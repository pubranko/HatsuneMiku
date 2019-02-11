from scrapy.spiders import SitemapSpider
from datetime  import datetime
import pickle,os,sys

#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.abspath(__file__))) #当モジュールディレクトリの絶対パス
sys.path.append(path)                               #それをモジュールライブラリに追加。
#from generate_urls import gen_urls
from ranko.items import NewsDB_Item

class AsahiComCrawlSpider(SitemapSpider):

    def parse(self, response):
        '''
        CallBack関数として使用。取得したレスポンスより、次のurlを生成し追加している。
        '''
        print('=== ',__file__,' parse_news:',response.url)

        now = datetime.now()
        yield NewsDB_Item(
            url=response.url,
            response_time=now,
            response_headers=pickle.dumps(response.headers),
            response_body=pickle.dumps(response.body),
            _id=(str(self.allowed_domains[0])+'@'+str(now).replace(' ','@',)),
        )   #ヘッダーとボディーは文字列が長くログが読めなくなるため、items.pyのsankei_comに細工して文字列を短縮。

    ### AsahiComCrawlSpider スタート ###

    name = 'asahi_com_crawl'
    allowed_domains = ['asahi.com']

    sitemap_urls = ['https://www.asahi.com/robots.txt',]    

    #sitemap_follow = []    #サイトマップを限定したい場合、r'post-2015-'のように、正規表現で指定できる。

    sitemap_rules = [(r'/articles/AS','parse'),] #実際のサイトへのリンクを絞り込み。

'''
政治
https://www.asahi.com/articles/ASM1R6GVVM1RUHBI033.html?iref=comtop_8_01
https://www.asahi.com/articles/ASM1R6GVVM1RUHBI033.html
社会
https://www.asahi.com/articles/ASM1R5J2KM1ROIPE01N.html
経済／マネー
https://www.asahi.com/articles/ASM1R4SPSM1RTIPE018.html
国際
https://www.asahi.com/articles/ASM1R55SPM1RUTIL02D.html
https://www.asahi.com/articles/ASM1R5FKYM1RUHBI027.html

産経新聞のように法則性はないようだ、、、

サイトマップ
robots.txtには以下のファイルがあった。
sitemap: http://www.asahi.com/sitemap.xml
sitemap: http://www.asahi.com/xml-sitemap-business.xml
sitemap: http://www.asahi.com/xml_sitemap_politics.xml
sitemap: http://www.asahi.com/and_M/sitemap.txt
sitemap: http://www.asahi.com/and_w/sitemap.txt
sitemap: http://www.asahi.com/ad/sitemap.xml
'''