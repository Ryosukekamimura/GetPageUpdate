import requests
from bs4 import BeautifulSoup

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

if __name__ == "__main__":
    if(get_website()):
        print("取得できました")