# -*- coding: utf-8 -*-
""" Created on Sat Jun 24 11:51:40 2017 @author: Flavio Pies """

import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO Define smart_send_email function - recieves a list of images and e-mail them without saving them to directory
# TODO Improve smart_send_email function - send detailed dataframe of credit cards payments
def smart_send_email(fromaddr, password, toaddr, text, attachments):
    fromaddr = fromaddr
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    alladdr = toaddr.split(",")
    msg['Subject'] = "Relatório de despesas"

    for attach in attachments:
        try:
            attachment = open(attach, "rb")
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % attachment)
            msg.attach(part)
        except:
            print("Failed to attach " + attach + " file")

    body = "Caro,\n\nSegue relatório de despesas.\n\n"
    body = body + text
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, password)

    text = msg.as_string()
    server.sendmail(fromaddr, alladdr, text)
    server.quit()


def send_email(fromaddr, password, toaddr, text:
fromaddr = fromaddr
    msg = MIMEMultipart()


msg['From'] = fromaddr
msg['To'] = toaddr
alladdr = toaddr.split(",")
msg['Subject'] = "Relatório de despesas"

filename_attach = filename + "_heatmap" + ".png"
attachment = open(r"Charts\\" + filename_attach, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename_attach)
msg.attach(part)
# TODO Heatmap weeks as initial dates
# TODO Heatmap weeks with better colors

filename_attach = filename + "_barchart_week" + ".png"
attachment = open(r"Charts\\" + filename_attach, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename_attach)
msg.attach(part)
# TODO Better visualization to Barchart weekly

filename_attach = filename + "_barchart_month" + ".png"
attachment = open(r"Charts\\" + filename_attach, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename_attach)
msg.attach(part)
# TODO Better visualization to Barchart monthly

filename_attach = filename + "_heatmap_cat" + ".png"
attachment = open(r"Charts\\" + filename_attach, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename_attach)
msg.attach(part)
# TODO Categories wrapping due to linebreak

body = "Caro,\n\nSegue relatório de despesas.\n\n"
body = body + text
msg.attach(MIMEText(body, 'plain'))

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, password)

text = msg.as_string()
server.sendmail(fromaddr, alladdr, text)
server.quit()
