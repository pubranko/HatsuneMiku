from datetime import datetime
from dateutil import parser
import pysolr,os,sys

#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.dirname(__file__))).rsplit('/',2)[0]+'/koushin/koushin'    #当モジュールディレクトリの2つ上の絶対パス
sys.path.append(path)          #それをモジュールライブラリに追加。
#from env  import SolrEnv       #プロジェクト内モジュール

'''
引数で渡されたrequest内のsolrサーチ用の情報より、検索を実行し結果を返す。
'''
def solr_search_news(request):

    '''
    solr = pysolr.Solr(
        SolrEnv.URL+SolrEnv.CORE,
        timeout=10,
        #verify=SolrEnv.VERIFY,
        auth=(SolrEnv.READ_USER,SolrEnv.READ_PASS),
    )
    '''
    #環境変数からsolrの情報を取得するように変更
    solr = pysolr.Solr(
        os.environ['SOLR_URL']+os.environ['SOLR_CORE'],
        timeout=10,
        #verify=SolrEnv.VERIFY,
        auth=(os.environ['SOLR_READ_USER'],os.environ['SOLR_READ_PASS']),
    )

    sch_query = request.GET['sch_query']
    page_num = int(request.GET['page_num'])
    page_max_lines = int(request.GET['page_max_lines'])

    start_line = ((page_num - 1) * page_max_lines)     #start_line は、0=1件目となる。
    #print('start_line',start_line)
    #results = solr.search(['url:"'+url+'"'],**{
    #    'sort': 'response_time desc,',      #ソートのやり方。 desc降順 asc昇順。 %20は空白に置き換えること。
    #    })
    results = solr.search([sch_query],**{
        'rows':page_max_lines,
        'start':start_line,
    })

    ''' resultsの内部構造は以下の通り。
    [('__class__', <class 'pysolr.Results'>), 
     ('__delattr__',
     <method-wrapper '__delattr__' of Results object at 0x7f5726ce7a20>),
     ('__dict__',
     {'raw_response': {'responseHeader': {'status': 0, 'QTime': 1, 'params': {'q': '((title:政府 OR article:政府))', 'wt': 'json'}},
                       'response': {'numFound': 4350, 'start': 0, 'docs':〜ここからは実際に取得したレコード〜
    '''
    #import inspect
    #print(type(results))
    #print(inspect.getmembers(results))
    #print(results['raw_response']['responseHeader'])
    #print(results.raw_response['response']['numFound'])

    #results_count = len(results)
    results_count = results.raw_response['response']['numFound']
    set_results = []
    for result in results:                              #複数の検索結果を1つづつ処理
        #resultチェック。スクレイピングに失敗しているものは除外する。
        try:
            result['url']
            result['title']
            result['article']
            result['publish_date']
            result['issuer']
            result['update_count']
        except:
            print('=== solr_search.py スクレイピングに失敗しているものを発見\n',result['url'])
            set_results.append({
                'result_title':'データの取得に失敗。ごめんなさい。こちらのurlは正しく表示できない状態です。',
                'result_article':'',
                'result_url':result['url'],
                'result_publish_date':'',
                'result_issuer':'',
                'result_update_count':'',
            })
        else:
            #本文は一部のみ表示する。（全文やってしまうと無断転載になる）
            article_part_len = len(result['article']) // 3  #3で割って整数部のみ取得
            if article_part_len > 50:                       #本文の3割以下＆最大50文字
                wk_results_article = result['article'][0:50]
            else:
                wk_results_article = result['article'][0:article_part_len]

            set_results.append({
                'result_title':result['title'],
                'result_article':wk_results_article,
                'result_url':result['url'],
                'result_publish_date':datetime.strftime(parser.parse(result['publish_date']),'%Y-%m-%d %H:%M'),
                'result_issuer':result['issuer'][0],
                'result_update_count':result['update_count'],
            })

    results = {'results_count':results_count,'set_results':set_results}
    return results