from urllib.parse import urlparse
from importlib import  import_module,find_loader
import os,sys

def controller(response_body,key_url,__name__):

    a = urlparse(key_url).netloc            #ドメインを抽出
    d = a[4:] if a[:4] == 'www.' else a     #頭にwww.があれば除去
    domain = d.replace('.','_',)            #ドメインの.を_へ置き換え   www.sankei.com -> sankei_com となる。

    #----プロジェクト内モジュールのimport
    path = (os.path.dirname(os.path.abspath(__file__))) #当モジュールディレクトリの絶対パス
    sys.path.append(path)                               #それをモジュールライブラリに追加。
    m = import_module('scraping_'+domain)               #ドメイン名より生成したモジュール名をインポート

    return m.scraping_article(response_body,key_url,__name__)
