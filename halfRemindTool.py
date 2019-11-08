#-*- coding: UTF-8 -*-
import requests
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.header import Header

DAILY_MATCH_URL = "https://live.500.com/static/info/bifen/xml/livedata/zqdc/{}Full.txt?_={}"
SINGLE_MATCH_URL = "https://live.500.com/json/odds.php?fid={}&cid=3"
MATCH_INFO_URL = "https://ews.500.com/score/zq/baseinfo?fid={}"
ANALYSIS_URL = "http://odds.500.com/fenxi/shuju-{}.shtml"


def format_url(i):
    month = str(datetime.datetime.now().month)
    date = "19"+month+"0"+str(i)
    now = str(time.time()).split(".")[0]
    url = DAILY_MATCH_URL.format(date, now)
    return url


def send_email(subject, msg):
    mail_host = "smtp.qq.com"
    mail_user = "249132529@qq.com"
    mail_pass = "wtlxdirwjunlbidj"

    sender = '249132529@qq.com'
    receiver = '249132529@qq.com'

    message = MIMEText(msg, 'plain', 'utf-8')
    message['From'] = Header("fresh", 'utf-8')
    message['To'] = Header("test", 'utf-8')

    subject = subject
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL()
        smtpObj.connect(mail_host, 465)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receiver, message.as_string())
    except smtplib.SMTPException as e:
        print (e)


if __name__ == '__main__':
    print("Remind Tool Start!")
    for i in range(5, 0, -1):
        r0 = requests.get(format_url(i))
        if r0.reason == 'Not Found':
            continue
        elif r0.reason == 'OK':
            break
    match_list = r0.text.split('\r\n')[1:-2]
    for match in match_list:
        match = eval(match[:-1])
	
        match_timestamp = time.mktime(time.strptime(match[4], '%Y-%m-%d %H:%M:%S'))
        if  0 <= match_timestamp - time.time() <= 1200:
            r1 = requests.get(SINGLE_MATCH_URL.format(match[0]))
            instant_level = eval(r1.text)[0][1]
            if instant_level[1] == u"半球" or instant_level[1] == u'受半球':
                r2 = requests.get(MATCH_INFO_URL.format(match[0]))
                r2_dict = eval(r2.text).get('data')
                home_team = r2_dict.get('homesxname')
                away_team = r2_dict.get('awaysxname')
                league = r2_dict.get('simpleleague')
                subject = league + ": " + home_team + " VS "+away_team
                message = str(instant_level[0]) + " " + str(instant_level[1]) + " " + str(instant_level[2]) + '\n' + ANALYSIS_URL.format(match[0])
                send_email(subject, message)
                print("Send Email Success With ID:" + str(match[0]))

    print("Remind Tool End!")

