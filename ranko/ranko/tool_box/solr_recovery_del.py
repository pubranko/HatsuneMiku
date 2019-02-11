#!/usr/bin/python3
import pysolr
from datetime import datetime
import sys, os
#----プロジェクト内モジュールのimport
path = (os.path.dirname(os.path.abspath(__file__))).rsplit('/',1)[0]    #当モジュールの1つ上の絶対パス
sys.path.append(path)                                                   #それをモジュールライブラリに追加。
from env  import MongoEnv,SolrEnv       #プロジェクト内モジュール

def solr_del():
    solr = pysolr.Solr(
        SolrEnv.URL+SolrEnv.CORE,
        timeout=10,
        verify=SolrEnv.VERIFY,
        auth=(SolrEnv.ADD_USER,SolrEnv.ADD_PASS),
        always_commit=True,
    )

    solr.delete(id=[
        'sankei.com@2019-01-04@09:59:11.999310',
        'sankei.com@2019-01-04@09:59:13.008712',
        'sankei.com@2019-01-04@09:59:16.553754',
        'sankei.com@2019-01-04@09:59:17.411767',
        'sankei.com@2019-01-04@09:59:21.314624',
        ])

    solr.always_commit

if __name__ == '__main__':

    solr_del()