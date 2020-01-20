#!/bin/bash
# This is deploy on VM function of TNFSH absent query Bot
# gnsJhenJie 2020 Copyright
nohup python3 main_send_remind_message.py &> log1.txt &
nohup python3 main_send_to_all.py &>  send_to_all_log.txt &
nohup python3 main_send_to_all_grade3.py &>  send_to_all_log.txt &