from django.shortcuts import get_object_or_404, render
#from django.template import loader
#from django.http import HttpResponse, HttpResponseRedirect
#from django.http import Http404
#from django.urls import reverse
#from .models import Question
import os,sys
from datetime import datetime
from dateutil import parser

#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.abspath(__file__)))+'/view_tool' #当モジュールディレクト直下のview_toolフォルダ
sys.path.append(path)                               #それをモジュールライブラリに追加。
from solr_search  import solr_search_news       #プロジェクト内モジュール

def saikutu(request):
    '''
    地中にある情報を採掘する！
    '''
    page_controll = {}
    page_count = 1
    
    if len(request.GET)==0:     #初画面表示
        results = {'results_count':0,'results':[],'page_controll_list':[]}
        context = {'results':results}
        return render(request, 'saikutu/saikutu.html', context)     #これはrenderでHTTPレスポンスにしている。  リクエスト、使用するテンプレート、引数（辞書型）

    else:
        #solrで検索した結果を格納
        results = solr_search_news(request)

        #ページ関係の情報の作成
        page_max_lines = int(request.GET['page_max_lines'])             #1ページに表示する最大件数
        page_max = results['results_count'] // page_max_lines           #検索結果をページ当たりの表示件数で割った商をページ数（最大）とする。
        if (results['results_count'] % page_max_lines) > 0:page_max+=1  #余りがあればカウントアップ
        page_num = int(request.GET['page_num'])                         #今回表示するページ数
        page_info = {'page_num':page_num,'page_max':page_max,'page_max_lines_save':page_max_lines}

        #ページコントローラーの作成
        #今回表示するページより前後のページを求める。
        #今回のページ±2ページ分表示する。
        page_controll_list = []
        start_page_num =  1 if page_num - 2 < 1 else  page_num - 2
        end_page_num = page_max if page_num + 2 > page_max else  page_num + 2
        page_controll_list.append({'page_value':'<<','page_num':1})
        for num in range(start_page_num,end_page_num+1):
            page_controll_list.append({'page_value':num,'page_num':num})

        page_controll_list.append({'page_value':'>>','page_num':page_max})

        #今回のクエリーをhtml上に埋め込む（save)するのに使う。
        #クライアント側でページ移動の際に、この情報をもとにクエリーを作成する。
        sch_query_save = request.GET['sch_query']
        context = {'results':results,'page_controll_list':page_controll_list,'page_info':page_info,'sch_query_save':sch_query_save}

        next_window = request.GET['next_window']
        if next_window == 'new':    #新しいタブで開く場合
            return render(request, 'saikutu/kaisyuu.html', context)     #これはrenderでHTTPレスポンスにしている。  リクエスト、使用するテンプレート、引数（辞書型）
        else:
            return render(request, 'saikutu/results_arrange.html', context)     #これはrenderでHTTPレスポンスにしている。  リクエスト、使用するテンプレート、引数（辞書型）
'''
def kaisyuu(request):

    results = {'results_count':0,'results':[]}
    if len(request.GET)==0:
        results = {'results_count':0,'results':[],'page_controll_list':[]}
        context = {'results':results}

    else:
        results = solr_search_news(request)

    context = {'results':results}
    return render(request, 'saikutu/kaisyuu.html', context)     #これはrenderでHTTPレスポンスにしている。  リクエスト、使用するテンプレート、引数（辞書型）
'''
