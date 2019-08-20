from flask import Flask,jsonify,request
import json
import pprint
import pymysql
import mysql.connector
import random
# coding: utf-8

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

def DBcon():
    con = mysql.connector.connect(host='sakatadb.ch35wwdofme0.ap-northeast-1.rds.amazonaws.com',
                              user='sakata_master',
                              password='Takuya0131',
                              database='sakatayamadaDB')
    return con

@app.route('/all')
def search_api_all():
    result_set = []
    con = DBcon()
    cur = con.cursor()
    sql = "select title,url,overview from input_data"
    cur.execute(sql)
    for row in cur.fetchall():
        result_set1 = 'API名 : ' + row[0]
        result_set2 = '　　URL : ' + row[1]
        result_set3 = '　　概要 : ' + row[2]
        result_set4 = result_set1 + result_set2 + result_set3
        result_set.append(result_set4)
    cur.close()
    con.commit()
    con.close()
    return jsonify(result_set)

@app.route('/<input_str>')
def search_api(input_str):
    '''
    入力された文字列に合致するAPIの情報を検索して、概要・ページ名・URLを返す
    +α 同時に入力された文字列をlistに登録し、検索される回数が多い文字列のデータを保持
    '''
    result_set = []
    con = DBcon()
    cur = con.cursor()
    #件数の確認
    sql = "select count(*) from input_data where keyword like '%%%s%%'" % input_str
    cur.execute(sql)
    count = cur.fetchall()
    if count[0][0] == 0:
        #0件だった場合
        result_set.append('0件です。ランダムで返します!')
        sql = "select max(no) from input_data"
        cur.execute(sql) #SQLの実行
        max_num = cur.fetchall() #カーソルフェッチ
        num = random.randint(1,max_num[0][0])
        sql = "select title,url,overview from input_data where no = %s" % num
    else:
        #0件でなかった場合
        sql = "select title,url,overview from input_data where keyword like '%%%s%%'" % input_str
    cur.execute(sql)
    for row in cur.fetchall():
        result_set1 = 'API名 : ' + row[0]
        result_set2 = '　　URL : ' + row[1]
        result_set3 = '　　概要 : ' + row[2]
        result_set4 = result_set1 + result_set2 + result_set3
        result_set.append(result_set4)
    cur.close()
    con.commit()
    con.close()
    return jsonify(result_set)
    
@app.route('/data_insert',methods=['POST'])
def insert_api():
    '''入力されたapi情報をdictに登録する'''
    post_item = request.get_json() #リクエストの読み込み
    con = DBcon() #DBの接続
    cur = con.cursor() #カーソルの読み込み
    sql = "select max(no) from input_data"
    cur.execute(sql) #SQLの実行
    max_num = cur.fetchall() #カーソルフェッチ
    sql_ins= "insert into input_data(no,title,url,overview,keyword) values(%s,%s,%s,%s,%s)"
    cur.execute(sql_ins,(max_num[0][0]+1,post_item["title"],post_item["url"],post_item["overview"],post_item["keyword"])) #実行
    cur.close()
    con.commit()
    con.close()
    return jsonify(post_item)

#app.run(host='0.0.0.0', port=80, debug=True)
if __name__ == '__main__':
    app.run()
