import yfinance as yahoo
import warnings
import os
import json
import requests
import datetime
#import schedule
import time

BRAND_NAME_JSON = r'C:\Users\b8759\Desktop\Python\株価通知アプリ\brand_name.json'
TOKEN = 'HrHYXA5u/d2Vxi5A+W6V6HuIA828L0sL3v0NP1GXHDMpJq/MHDjZg56wQ1kTl0+ilHBaGMidjb/33Iq6IfOzHJxySUSzvzUUCIhbl/dbBtTwQ6t4HA6x4ivl90BGkB2en21n0CdgnOQ10nkDH/JB3AdB04t89/1O/w1cDnyilFU='
#TOKEN = 'lqsHGJFJ2qUayJ2aeppSAr2Eel+FeLnFgUKWC5dVrR5qfBPQAvfpbGYb03EDxFXl7q0/4citnlWyK9MhykwnDHP8o5OVKzonX7/ZfAJkKqctfV0NSgGFBbmy+QEvs7DXm4myjVicg4H3ss+Zzp5BZQdB04t89/1O/w1cDnyilFU='
API_URL = 'https://api.line.me/v2/bot/message/push'
USER_ID = 'U0b7e03952b35d3288a55070e63f5edaf'
#USER_ID =  'U27b8337b2a1b8941e2a86c4203db725b'
LINE_SEP = '\n'
T = '.T'
TOKEN_INF = { 'Authorization': 'Bearer' + ' ' + TOKEN,
          'Content-Type': 'application/json'}

new_brand_lines = None
#-----------------------------------
#メソッド名:_stock_price_enumerate
#処理概要:登録済みの銘柄の情報を計算して通知する
#-----------------------------------
class _stock_price_enumerate():
        exit_return = None
        key_list = None
        value_list = None
#-----------------------------------
#メソッド名:_get_list
#処理概要:テキストファイルの内容をリストに出力する
#引数:なし
#戻り値:
#----------------------------------
        def _get_list(self):

          #空の辞書とリストを設定
          dict_data = {}
          key_list = []
          value_list = []

          #JSONファイルを読み込んでkeyとvalueをそれぞれリストに格納
          if os.path.isfile(BRAND_NAME_JSON):
               with open (BRAND_NAME_JSON,'r',encoding='utf-8')as f:

                    #ファイルを変数に代入
                    dict_data = json.load(f)

               #リストにkeyを格納し、クラス変数に値を入れる
               for data in dict_data.keys():
                    key_list.append(data)
                    self.key_list = key_list

               #リストにvalueを格納し、クラス変数に値を入れる   
               for data in dict_data.values():
                    value_list.append(data)
                    self.value_list = value_list
#-----------------------------------
#メソッド名:_get_calculation
#処理概要:登録されている銘柄の値を計算する
#引数:なし
#戻り値:msg_list
#----------------------------------
        def _get_calculation(self):
             i = 0
             msg_list = []
             for data in self.key_list:

               #ヤフーファイナンスからデータ取得
               rcv = yahoo.Ticker(data)

               #株価取得
               rcv_pri = rcv.info.get('currentPrice')
               
               #例外処理は表示しない   
               warnings.simplefilter('ignore')

               if not rcv_pri == None:
                    fin_pri = int(float(rcv_pri))

               #情報が取れない時は情報無し
               else:
                    fin_pri = '情報無し'


               #前日の株価を取得して前日比を出す
               rcv_lpri = rcv.info.get('previousClose')
               
               #例外処理は表示しない   
               warnings.simplefilter('ignore')

               if not rcv_lpri == None and not fin_pri == None:   
                    res = fin_pri / rcv_lpri
                    price_change = int(round(res * 100, 0))

               #情報が取れない時は情報無し
               else:
                    price_change = '情報無し'

               #PER取得
               rcv_per = rcv.info.get('trailingPE')

               #例外処理は表示しない   
               warnings.simplefilter('ignore')

               if not rcv_per == None:
                    fin_per = round(float(rcv_per), 1)

               #情報が取れない時は情報無し
               else:
                    fin_per = '情報無し'

               #取得した情報を通知で飛ばすためのメッセージの準備
               rcv_msg = ('■{0}の情報'.format(self.value_list[i]) + LINE_SEP + 
                          '株価:{0}'.format(fin_pri) + LINE_SEP + 
                          '前日比:{0}%'.format(price_change) + LINE_SEP +
                          'PER:{0}'.format(fin_per))
               msg_list.append(rcv_msg)
               i = i + 1
             return msg_list
#-----------------------------------
#メソッド名:_push_info
#処理概要:LINE通知を飛ばす
#引数:msg_list
#戻り値:
#----------------------------------
        def _push_info(self,msg_list):
            
            #時間と日付を取得
            dt_now = datetime.datetime.now()
            date = dt_now.strftime('%m月%d日 %H:%M')

            #メッセージ内容
            msg_hed = ('【{0}の株価情報】'.format(date))
            msg = LINE_SEP.join(msg_list)
            msg_final = msg_hed + LINE_SEP + msg

            msg_inf = {'to':USER_ID,
	                     'messages':[{
                          'type':'text',
                          'text':msg_final}
                         ]}

            requests.post(API_URL, headers=TOKEN_INF,json = msg_inf)
            print('実行完了')
#-----------------------------------
#メイン処理
#-----------------------------------
        def _main(self):
            _get_list = self._get_list()
            _get_calculation = self._get_calculation()
            _push_info = self._push_info(_get_calculation)
#-----------------------------------
#処理実行
#-----------------------------------
if __name__ == '__main__':

     #インスタンス作成
     _stock_price_enumerate = _stock_price_enumerate()
     _stock_price_enumerate = _stock_price_enumerate._main()
