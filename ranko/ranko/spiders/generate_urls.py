import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from datetime  import datetime,date
from dateutil import parser,relativedelta,rrule
import pickle,inspect,os,sys,json,pprint
import numpy as np

def gen_urls(domain):
    '''
    Crawlするurlを生成する。ベースとなるアドレスを1つ用意し、それをもとにカウントアップさせてurlを生成している。
    '''
    def url_assembly(addr_pattern):
        '''
        アドレスパターンに従ってurlを組み立てる。
        '''
        wk_url = []
        wk_addr_pattern1 = []
        wk_addr_pattern1_list = []
        date_list = []
        #アドレスパターンを確認
        #範囲指定があればそのリストを作成。ただし、同一の範囲指定が複数あった場合、最後の分でリストを作成する。
        #ついでにjsonファイルの簡易チェック。
        for ap in addr_pattern:
            wk_addr_pattern1.append(ap)
            if  ap[0] == '固定値':
                pass
            elif  ap[0] == '日付範囲':
                #アドレスパターンに日付範囲指定があれば、その範囲分を定義したリストを生成する。
                if ap[1] == '当日':
                    d_from = date.today()
                elif ap[1] == '前日':
                    d_from = date.today() - datetime.timedelta(days=1)
                else: #西暦8桁指定の場合
                    d_from = parser.parse(ap[1])
                if ap[2] == '当日':
                    d_to = date.today()
                elif ap[2] == '前日':
                    d_to = date.today() - datetime.timedelta(days=1)
                else: #西暦8桁指定の場合
                    d_to = parser.parse(ap[2])
                date_list = list(rrule.rrule(rrule.DAILY, dtstart=d_from, until=d_to))
            elif  ap[0] == '数値範囲':
                #ここで数値範囲で指定された開始、終了、増分値に合わせたリストを作成
                wk_num_range_list = range(ap[1],ap[2]+1,ap[3])       
            else:
                print('=== jsonファイルに不正あり！ ===',ap[0])
                raise 
        date_idx = 0                                                #date_listのインデックス
        wk_addr_pattern1_list = [wk_addr_pattern1]*len(date_list)   #アドレスパターンを日付リスト分複製したリストを生成
        #固定値、日付範囲を整形したリストを生成。数値範囲については、中身を’数値範囲’の固定値に置き換え。
        wk_addr_pattern3_list = []                                  #上記のアドレスパターンの日付範囲を
        for wk_addr_pattern2 in wk_addr_pattern1_list:   #
            wk_addr_pattern3 = []
            for ap in wk_addr_pattern2:
                if  ap[0] == '固定値':
                    wk_addr_pattern3.append(ap[1])
                elif  ap[0] == '日付範囲':
                    wk_addr_pattern3.append(date_list[date_idx].strftime(ap[3]))
                elif  ap[0] == '数値範囲':
                    wk_addr_pattern3.append('数値範囲')
            #アドレスパターンを更に数値範囲の数だけ複製したリストを生成
            wk_addr_pattern3_list.append([wk_addr_pattern3]*len(wk_num_range_list))
            date_idx += 1  #
        #最後に数値範囲に指定された値へ整形したリストを生成
        wk_addr_pattern4_list = []
        wk_url_list = []
        for wk_addr_pattern4 in wk_addr_pattern3_list:
            num_idx = 0
            for wk_addr_pattern5 in wk_addr_pattern4:
                wk_addr_pattern6 = []
                for ap in wk_addr_pattern5:
                    if  ap == '数値範囲':
                        wk_addr_pattern6.append(str(wk_num_range_list[num_idx]).zfill(4))
                    else:
                        wk_addr_pattern6.append(ap)
                num_idx += 1
                wk_url_list.append(''.join(wk_addr_pattern6))   #最終的なurlをリストへ保存。
        
        return wk_url_list
    #########################
    ### gen_urls 処理開始 ###
    #########################
    urls_list = []
    file = open(os.path.dirname(os.path.abspath(__file__))+'/crawl_set.json','r', encoding="utf-8")
    crawl_set = json.loads(file.read(),)
    file.close()
    crawl_info = crawl_set[domain]    #ドメインをkeyにクロールパターンを取得
    for crawl_pattern_type,crawl_pattern in crawl_info.items():
        #今後の課題
        #クロールパターン→基本（前日〜当日）、夜間（前月や当月などの長期間の指定）、等を検討
        #前回実行情報を確認し、今回どのパターンで動かすかを制御できるようにする。
        #アドレスパターンリストより順にアドレスの組み立てを行う。
        for addr_pattern in crawl_pattern['addr_pattern_list']:
            urls_list.extend(url_assembly(addr_pattern))
    print('=== gen_urls 終了時 ===')
    pprint.pprint(urls_list)
    return urls_list