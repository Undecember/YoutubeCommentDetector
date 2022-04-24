import smtplib, json
from datetime import datetime, timezone, timedelta
from email.message import EmailMessage

async def report(comment):
    with open('config.json', 'r') as fp:
        config = json.load(fp)

    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(config['SMTP_EMAIL'], config['SMTP_PASSWORD'])

    with open('resources/report.html', 'r') as fp: html = fp.read()
    html = html.format(
        commentURL = f'https://www.youtube.com/watch?v={config["VideoId"]}&lc={comment["id"]}',
        authorURL = comment['authorChannelUrl'],
        authorAvatar = comment['authorProfileImageUrl'],
        authorName = comment['authorDisplayName'],
        content = comment['textOriginal'],
        when = datetime.utcfromtimestamp(comment['publishedAt']) \
            .astimezone(timezone(timedelta(hours = 9))) \
            .strftime('%Y년 %m월 %d일 %H시 %M분 %S초 GMT+9'))

    msg = EmailMessage()
    msg['Subject'] = f'[댓글 알림] 이 댓글 이후로 {config["interval"]}초 동안 댓글이 없었습니다!'
    msg['From'] = config['SMTP_EMAIL']
    msg['To'] = config['ReportTo']
    msg.add_alternative(html, subtype = 'html')
    smtp.send_message(msg)

    smtp.quit()
