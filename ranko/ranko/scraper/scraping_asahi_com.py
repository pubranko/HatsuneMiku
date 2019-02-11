from bs4 import BeautifulSoup as bs4
from dateutil import parser,relativedelta

def scraping_article(response_body,key_url,calling_name):
    print('=== scraper ',__file__,'scrape_article start ',key_url)
    #取得したレスポンスのbodyより、タイトルと本文の抽出を試みる。
    #print('=== scrape_article start',__name__)
    #htmlの解析
    soup = bs4(response_body,'lxml')

    title = soup.title.text

    #文章タイプ別に調査(hpによってクラス名とかが違った、、、）
    article_case1 = ''
    
    for p in soup.select(".ArticleText p"):
        if p.string:                                    #pタグの文字列を抽出。空白だけのpタグもあるようなので、空白以外の文字があるもの限定。
            article_case1 = article_case1 + p.string    #複数pタグがある場合、全て連結する。

    #本文抽出チェック。ケース別に抽出できたかチェック。抽出できなかったり、複数の条件を同時に満たした場合、エラーとする。
    cnt = 0
    if article_case1:cnt+=1
    #if article_case2:cnt+=1
    #if article_case3:cnt+=1

    if cnt == 1:
        if article_case1:
            article = article_case1
        #elif article_case2:
        #    article = article_case2
        #elif article_case3:
        #    article = article_case3
    elif cnt > 1:
        print('=== scraper ',__file__,'scrape_article  本文抜き出し条件複数満す！ 条件見直し要',key_url)
    else:
        article = ''
        print('=== scraper ',__file__,'scrape_article  本文抜き出せず！ 条件見直し要',key_url)
    #print('=== scrape_article 結果:',article)

    #公開日
    publish_date = ''
    #class=LastUpdatedのtimeタグを検索し、datetime属性の値を取得する。
    #     例）<time datetime="2019-1-24T18:11" class="LastUpdated">2019年1月24日18時11分</time>
    s_find = soup.find('time',attrs={'class':'LastUpdated'})
    s_find2 = s_find['datetime']
    #print('=== scraper ',__file__,'scrape_article 調査1 ===\n',key_url,'\n   ',s_find,'\n   ',s_find2)
    publish_date = parser.parse(s_find2)

    #発行者
    issuer = '朝日新聞社'

    return title,article,publish_date,issuer
