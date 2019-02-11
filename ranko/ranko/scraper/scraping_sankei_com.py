from bs4 import BeautifulSoup as bs4
from dateutil import parser,relativedelta

def scraping_article(response_body,key_url,calling_name):
    #取得したレスポンスのbodyより、タイトルと本文の抽出を試みる。
    #print('=== scrape_article start',__name__)
    #htmlの解析
    soup = bs4(response_body,'lxml')

    title = soup.title.text

    #文章タイプ別に調査(hpによってクラス名とかが違った、、、）
    article_case1 = soup.find('p','sentence clearfix')
    article_case2 = ''
    for p in soup.select(".fontMiddiumText p"):
        if p.string:                                    #pタグの文字列を抽出。空白だけのpタグもあるようなので、空白以外の文字があるもの限定。
            article_case2 = article_case2 + p.string    #複数pタグがある場合、全て連結する。
    article_case3 = ''
    for p in soup.select(".post_content p"):
        if p.string:                                    #pタグの文字列を抽出。空白だけのpタグもあるようなので、空白以外の文字があるもの限定。
            article_case3 = article_case3 + p.string    #複数pタグがある場合、全て連結する。

    #本文抽出チェック。ケース別に抽出できたかチェック。抽出できなかったり、複数の条件を同時に満たした場合、エラーとする。
    cnt = 0
    if article_case1:cnt+=1
    if article_case2:cnt+=1
    if article_case3:cnt+=1

    if cnt == 1:
        if article_case1:
            article = article_case1
        elif article_case2:
            article = article_case2
        elif article_case3:
            article = article_case3
    elif cnt > 1:
        print('=== scraper sankei_com:scrape_article  本文抜き出し条件複数満す！ 条件見直し要',key_url)
    else:
        article = ''
        print('=== scraper sankei_com:scrape_article  本文抜き出せず！ 条件見直し要',key_url)
    #print('=== scrape_article 結果:',article)

    #公開日
    publish_date = ''
    for p in soup.select("#__r_publish_date__"):        #idで選択
        #publish_date = p.string    #複数pタグがある場合、全て連結する。
        publish_date = parser.parse(p.string)    #複数pタグがある場合、全て連結する。

    #発行者
    issuer = '産経新聞社'

    return title,article,publish_date,issuer
