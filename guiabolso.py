# -*- coding: utf-8 -*-
""" Created on Sat Jun 24 11:51:40 2017 @author: Flavio Pies """
import datetime as dt

import mailsender
import reportmaker
import scraper

# TODO Define logic to MS and FP - use guiabolso as controller

today = dt.datetime.today()
usernameStr = ''
passwordStr = ''

scraper.open_guiabolso()
scraper.logar(usernameStr, passwordStr)
scraper.wait_infos()
scraper.expand_page_previous_months()
tabela = scraper.extract_page_info()

tabela = reportmaker.report_clean(tabela)
tabela = reportmaker.report_fp(tabela)
fatura = reportmaker.old_information_fp(tabela)[0]
reportmaker.export_excel(fatura)

fatura = reportmaker.report_prep(fatura)
reportmaker.charts(fatura)

filename = str(today.year) + str(today.month) + str(today.day) + "_Fatura"
mailsender.send_email(usernameStr, str(""), filename)

# tabela = reportmaker.old_information_fp(tabela)[1]
# reportmaker.export_excel(tabela)
del (tabela, fatura)
