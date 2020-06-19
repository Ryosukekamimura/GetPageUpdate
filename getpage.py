import requests
import re
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage
import schedule
import time

import access_token

#LINEトークン設定
LINE_CHANNEL_ACCESS_TOKEN = access_token.AccessToken.CHANNEL_ACCESS_TOKEN
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


#Websiteの要素を抜き出す関数
def get_website():
    url = 'http://gifu-handball.jp/modules/pico/index.php/category0022.html'
    file = 'page.txt'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    #.pico_list_contentsクラスから取得
    elems = soup.select('.pico_list_contents')
    str_elems = str(elems)


    #old_elemsを読み取る
    try:
        f = open(file)
        old_elems = f.read()
    except:
        old_elems = ''

    if(str_elems == old_elems):
        return False
    else:
        f = open(file, 'w')
        f.writelines(str_elems)
        f.close()
        return True

#LINEに通知する関数
def push_line(str):
    #TODO: user_idを設定
    user_id = access_token.AccessToken.USER_ID
    messages = TextSendMessage(str)
    line_bot_api.push_message(user_id, messages=messages)

#パターンを判定する関数
def pattern_matching(str):
    #<aから始まって、<a 任意の1文字、0回以上の繰り返し、が0または1回、>
    html = re.sub('<a.*?>|</a>','', str)
    pattern = '<li.*?>(.*?)</li>'
    results = re.findall(pattern, html, re.S)
    return results

def main():
    if(get_website()):
        f = open('page.txt')
        data = f.read()
        f.close()
        pattern_matching(data)
        results = pattern_matching(data)

        send_messages = ''
        for result in results:
            send_messages += result
        #LINEに通知
        #すべてのメッセージをLINEに送信
        push_line(send_messages)
    else:
        push_line('更新はないです。')
        print('All code is done.')

#毎日15時に実行する
schedule.every().day.at("15:00").do(main)
while True:
    schedule.run_pending()
    time.sleep(1)