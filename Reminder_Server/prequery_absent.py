# !/usr/bin/python3
# coding:utf-8
# This is prequery absent function of TNFSH absent query Bot
# gnsJhenJie 2020 Copyright

import urllib.request, urllib.parse, urllib.error
from datetime import datetime, timedelta, date
#firebase:
# 引用firebase必要套件
import firebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# 引用私密金鑰
# path/to/serviceAccount.json 請用自己存放的路徑
cred = credentials.Certificate('Firebase_Cred_Json_PATH')
# 初始化firebase，注意不能重複初始化
firebase_admin.initialize_app(cred)
# 初始化firestore
db = firestore.client()
#firebase 參數
total_list_collection_name = 'total_list'
total_list_collection_path = 'total_list'
total_list_collection_ref = db.collection(total_list_collection_path)
user_info_collection_name = "user_info"
user_info_path = "user_info"
user_info_collection_ref = db.collection(user_info_path)

def absent_query_recent(tnfsh_class, tnfsh_number, day):  #Query single day
    url = 'https://sp.tnfsh.tn.edu.tw/attend/index.php/attend/search?begin='+day+'&end='+day+'&class='+tnfsh_class+'&num='+tnfsh_number
    html = urllib.request.urlopen(url).read()
    count = 0
    count += str(html).count('btn-danger')
    count += str(html).count('btn-warning')
    count += str(html).count('btn-info')
    return count

def pass_absent_dictionary():
    total_list_doc_ref = db.collection("total_list").document('total1')
    total_docs = total_list_doc_ref.get()
    dayOfWeek = datetime.now().weekday() + 1
    today_list = 'fb_sender_id_list_week' + str(dayOfWeek)
    fb_sender_id_list = format(total_docs.to_dict()[today_list])
    to_send_list = fb_sender_id_list.split(',')

    query_dict = dict()
    tmp1, tmp2, tmp3 = 0,0,0
    for target in to_send_list:
        date_today = datetime.now().date().strftime("%Y-%m-%d")
        date_p1 = (datetime.now() + timedelta(days = -1)).strftime("%Y-%m-%d")
        date_p2 = (datetime.now() + timedelta(days = -2)).strftime("%Y-%m-%d")
        user_info_doc_ref = user_info_collection_ref.document(target)
        user_info_docs = user_info_doc_ref.get()
        user_info_dict = user_info_docs.to_dict()
        tnfsh_class = format(user_info_dict['tnfsh_class'])
        tnfsh_number = format(user_info_dict['tnfsh_number'])
        tmp1, tmp2, tmp3 = absent_query_recent(tnfsh_class,tnfsh_number,date_today),absent_query_recent(tnfsh_class,tnfsh_number,date_p1),absent_query_recent(tnfsh_class,tnfsh_number,date_p2)
        if tmp1 or tmp2 or tmp3:
            query_dict[target] = [tmp1,tmp2,tmp3]
    return query_dict