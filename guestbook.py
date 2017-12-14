 #coding: utf-8

import shelve
from datetime import datetime
from flask import Flask, request, render_template, redirect,escape,Markup


application = Flask(__name__)

DATA_FILE = 'guestbook.dat'


def save_data(name,comment,creat_at):

     """投稿データの保存"""
     #shelveモジュールでデータベースファイルを開く
     database = shelve.open(DATA_FILE)
     #データベースにgreeting_listがなければ、新しくリストを作成
     if 'greeting_list' not in database:
        greeting_list = [ ]
     else:
         #データベースからデータを取得
        greeting_list = database['greeting_list']
     #リストの先頭に投稿データを追加
     greeting_list.insert(0,{
        'name': name,
        'comment': comment,
        'creat_at': creat_at ,
     })

     #データベースを更新します
     database['greeting_list'] = greeting_list
     #データベースファイルを閉じる
     database.close()


def load_data():
     """投稿されたデータを返す"""

     #shelveモジュールでデータベースファイルを開く
     database = shelve.open(DATA_FILE)
     #greething_listを返す。データがなければ空のリストを返す。
     greeting_list = database.get('greeting_list',[])
     database.close()
     return greeting_list


@application.route('/')

def index():
     """トップページテンプレートを利用してページを表示します。"""
     
     #投稿データを読み込む
     greeting_list = load_data()
     

     return render_template('index.html', greeting_list = greeting_list)


@application.route('/post',methods=[ 'POST' ])

def post():
     """投稿用URL"""
     name = request.form.get('name') 
     comment = request.form.get('comment')
     creat_at = datetime.now() #投稿日時
     # preserve data 
     save_data(name,comment,creat_at)
     #redirect Top_page after preserve data 
     return redirect('/')

@application.template_filter('n12br')

def n12br_filter(s):
     """改行文字をbrタグに置き換えるテンプレートフィルタ"""
     return escape(s).replace('\n',Markup('<br>'))

@application.template_filter('datetime_fmt')

def datetime_fmt_filter(dt):
     """datetimeオブジェクトを見やすい表示にするテンプレートフィルタ"""
     return dt.strftime('%Y/%m/%d %H:%M:%S')



if __name__ == '__main__':
     #IPアドレス127.0.0.1の8000番ポートでアプリケーションを実行。
     application.run('127.0.0.1',8000,debug=True)

     

     
     
