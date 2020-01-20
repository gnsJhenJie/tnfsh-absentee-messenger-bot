# !/usr/bin/python3
# coding:utf-8
#This is send to all function of TNFSH absent query Bot
#gnsJhenJie 2020 Copyright

import os
from apscheduler.schedulers.blocking import BlockingScheduler

import prequery_absent
import send_remind_message

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
#firebase_admin.initialize_app(cred)
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

prequery = dict()

params = {
    "access_token": "FACEBOOK_ACCESS_TOKEN"
}
headers = {
    "Content-Type": "application/json"
}
total_list_doc_ref = db.collection("total_list").document('total1')
total_docs = total_list_doc_ref.get()
dayOfWeek = datetime.now().weekday() + 1
today_list = 'fb_sender_id_list_week' + str(dayOfWeek)
fb_sender_id_list = format(total_docs.to_dict()[today_list])
to_send_list = fb_sender_id_list.split(',')

def prequery_job():
    global prequery, total_docs, dayOfWeek, today_list, fb_sender_id_list, to_send_list
    prequery = prequery_absent.pass_absent_dictionary()
    print('clock.py start mission: prequery_job()') #運行時印出此行訊息

    total_docs = total_list_doc_ref.get()
    dayOfWeek = datetime.now().weekday() + 1
    today_list = 'fb_sender_id_list_week' + str(dayOfWeek)
    fb_sender_id_list = format(total_docs.to_dict()[today_list])
    to_send_list = fb_sender_id_list.split(',')

def send_remind_job(start,end_not_included):
    send_remind_message.send_remind_message(to_send_list[start:end_not_included],prequery)
def send_remind_job_without_end(start):
    send_remind_message.send_remind_message(to_send_list[start:],prequery)

sched = BlockingScheduler()
sched.add_job(func=prequery_job, trigger='cron', hour=9, minute=58) #9:58
send_per_job = 60
send_job_amount =  6 #將會+1 為了最後不足的
for i in range(0,send_job_amount):
    sched.add_job(func=send_remind_job, args=(i*send_per_job,(i+1)*send_per_job,), trigger='cron', hour=10, minute=18)
sched.add_job(func=send_remind_job_without_end, args=(send_job_amount*send_per_job,), trigger='cron', hour=10, minute=18)

try:
    sched.start()
except:
    print('failed')

