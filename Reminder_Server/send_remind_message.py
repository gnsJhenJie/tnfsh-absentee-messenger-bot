# !/usr/bin/python3
# coding:utf-8
# This is send remind message function of TNFSH absent query Bot
# gnsJhenJie 2020 Copyright

import random
import requests
import json

params = {
    "access_token": "FACEBOOK_ACCESS_TOKEN"
}
headers = {
    "Content-Type": "application/json"
}
def send_remind_message(recipient_list,prequery):
    for recipient_id in recipient_list:
        radm_subtitle = random.randint(1,2) #Random subtitle
        if radm_subtitle == 1:
            subtitle_to_send = '今天過得好嗎?'
        elif radm_subtitle == 2:
            subtitle_to_send = '還活著吧?'
        if recipient_id in prequery:
            if prequery[recipient_id][2]:
                subtitle_to_send = '前天共有'+str(prequery[recipient_id][2])+'筆異常紀錄\n' + subtitle_to_send
            if prequery[recipient_id][1]:
                subtitle_to_send = '昨天共有'+str(prequery[recipient_id][1])+'筆異常紀錄\n' + subtitle_to_send
            if prequery[recipient_id][0]:
                subtitle_to_send = '今天共有'+str(prequery[recipient_id][0])+'筆異常紀錄\n' + subtitle_to_send
            subtitle_to_send = u'🚨' + u'🚨' + u'🚨' + '\n' + subtitle_to_send
        radm_pic_no = str(random.randint(1,12))
        data = json.dumps({
            "recipient":{
                "id":recipient_id
            },
            "message":{
                "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                    {
                        "title":"Good Night~ 記得檢查一下ㄛ!",
                        "image_url":"https://tnfsh-absentee.web.app/pics/messenger/"+radm_pic_no+".jpg",
                        "subtitle":subtitle_to_send,
                        "default_action": {
                        "type": "web_url",
                        "url": "https://tnfsh-absentee.web.app/pics/messenger/"+radm_pic_no+"o.jpg",
                        "webview_height_ratio": "tall",
                        },
                        "buttons":[
                        {
                            "type":"postback",
                            "title":"查詢最近缺席",
                            "payload":"q"
                        },{
                            "type":"postback",
                            "title":"查詢本週缺席",
                            "payload":"qw"
                        }              
                        ]      
                    }
                    ]
                    }
                }
            },
            "tag": "CONFIRMED_EVENT_UPDATE"
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)       
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)    

def send_message(recipient_list,message_text):
    for recipient_id in recipient_list:
        data = json.dumps({
            "recipient": {
                "id": recipient_id
            },
            "message": {
                "text": message_text
            },
            "tag": "CONFIRMED_EVENT_UPDATE"
        })
        r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
        if r.status_code != 200:
            print(r.status_code)
            print(r.text)