import requests
from bs4 import BeautifulSoup
from linebot import LineBotApi
from linebot.models import TextSendMessage

#TODO:gitignoreに
#TODO: LINE_CHANNEL_ACCESS_TOKENを設定
LINE_CHANNEL_ACCESS_TOKEN = ""
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

def get_website():
    url = 'http://gifu-handball.jp/modules/pico/index.php/category0022.html'
    file = 'page.txt'
    res = requests.get(url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    elems = soup.select('.pico_list_contents')
    str_elems = str(elems)
    print(str_elems)

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


def push_line(str):
    #TODO: user_idを設定
    user_id = ""
    messages = TextSendMessage(str)
    line_bot_api.push_message(user_id, messages=messages)


if __name__ == "__main__":
    if(get_website()):
        f = open('page.txt', 'r')
        #LINEに通知
        push_line(f)
        f.close()
