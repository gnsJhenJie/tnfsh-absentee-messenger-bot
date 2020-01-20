# !/usr/bin/python3
# coding:utf-8
# This is send to all function of TNFSH absent query Bot
# gnsJhenJie 2020 Copyright

import os
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

import sys
import json
from datetime import datetime, timedelta, date
import requests
from flask import Flask, request
import time
import socket
import random

#firebase:
# 引用firebase必要套件
#import firebase
import firebase_admin
#import google_cloud_firestore
from firebase_admin import credentials
from firebase_admin import firestore
#from google_cloud_firestore import firestore
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

total_list_doc_ref = db.collection("total_list").document('total1')
total_docs = total_list_doc_ref.get()
print('hi')
# BlockingScheduler
def send_message(recipient_id, message_text):

    print("sending message to "+recipient_id+": "+message_text)

    params = {
        "access_token": "FACEBOOK_ACCESS_TOKEN"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


@sched.scheduled_job('interval', seconds = 30) #定期執行 使用GMT時區(配合GAE)
def send_to_all_job():
    #print('send_to_all.py start mission') #運行時打印出此行訊息

    #print("sending btn message to all: ")
    transfer_doc_ref = db.collection('transfer').document('send_to_all')
    transfer_docs_dic = transfer_doc_ref.get().to_dict()
    if format(transfer_docs_dic['status']) == 'pending': #發現未發送過的廣播訊息
        
        new_record = transfer_docs_dic
        new_record['status'] = 'sending'
        transfer_doc_ref.set(new_record)

        total_list_doc_ref = db.collection("total_list").document('total1')
        total_docs = total_list_doc_ref.get()
        fb_sender_id_list = format(total_docs.to_dict()['fb_sender_id_list'])
        to_send_list = fb_sender_id_list.split(',')
        
        for recipient_id in to_send_list:
            send_message(recipient_id,transfer_docs_dic['message'].replace('\\'+'n','\n'))
        new_record = transfer_docs_dic
        new_record['status'] = 'done'
        transfer_doc_ref.set(new_record)
try:
    sched.start()
except:
    print('failed')

