import bs4
import requests
import urllib.request, urllib.error
import sys, os, re
import argparse
import json

def main(args):
    """
    Scraping images:
    """
    parser = argparse.ArgumentParser(description='Scraping Google images')
    parser.add_argument('-s', '--search', type=str, default=None, help='Serch Word')
    parser.add_argument('-n', '--num', type=int, default=10, help='Num of images')
    parser.add_argument('-d', '--directory', type=str, default=None, help='output directory')

    args = parser.parse_args()
    
    try:
        num = args.num
        print(f'保存枚数　 : {num}\n検索ワード : ', end='')
        ## join multi search words
        keyword = '+'.join(args.search.split())
        print(f'{keyword}\n保存先　　 : ', end='')
        directory = args.directory.split()[0]
        print(f'{directory}')
    except AttributeError:
        print('<Error> 正しいOptionを入力してください (--helpで表示)')

    ## 確認
    try:
        _ = input("========\n条件はこちらでいいですか？\nPress any key to start or Ctr+C to exit: ")
    except KeyboardInterrupt:
        print('\n終了しました')
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    ## Scraping
    # url = f'https://www.google.co.jp/search?q={keyword}&source=lnms&tbm=isch'
    url = f'https://search.yahoo.co.jp/image/search?p={keyword}&fr=top_ga1_sa&ei=UTF-8'
    header = {'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"}
    soup = bs4.BeautifulSoup(urllib.request.urlopen(urllib.request.Request(url, headers=header)), 'html.parser')
    
    Images = []
    for a in soup.find_all('img',{"alt":f'「{keyword}」の画像検索結果'}):
        # src="data:image/gif;base64,R0lGODlhAQABAIAAAP//.." ## GOOGLElこうなる...dataURI decodeできん ## 省略が厄介
        link, Type = a["src"], "jpg"
        Images.append((link, Type))

    for i, (img, Type) in enumerate(Images[0:num]):
        try:
            Type = Type if len(Type) > 0 else 'jpg'

            raw_img = urllib.request.urlopen(img).read()

            f = open(os.path.join(directory, f'img_{str(i)}.{Type}'), 'wb')
            f.write(raw_img)
            f.close()
        except Exception as e:
            print('could not download :', img)
            print(e)


if __name__ == "__main__":
    from sys import argv
    try:
        main(argv)
    except KeyboardInterrupt:
        pass
    sys.exit()
