# -*- coding: utf-8 -*-
""" Created on Sat Jun 24 11:51:40 2017 @author: Flavio Pies """

import datetime as dt

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

today = dt.datetime.today()
browser = webdriver.Chrome()


# TODO Hidden browser in scraper


def open_guiabolso():
    # Opens guiabolso page and waits loading time
    browser.get(('https://www.guiabolso.com.br/comparador/#/login?_k=juim0c'))

    delay = 10  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.NAME, 'email')))
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time")


def logar(usernameStr, passwordStr):  # Login in guiabolso and return true or false text
    print("Loading page...")
    try:
        username = browser.find_element_by_name('email')
        username.send_keys(usernameStr)
        password = browser.find_element_by_name('password')
        password.send_keys(passwordStr)
        password.submit()
        print("Login has been successful!")
    except:
        print("Login has failed!")


def wait_infos():
    delay = 90  # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'main-header')))
    except:
        browser.refresh()
    browser.get(('https://www.guiabolso.com.br/extrato'))
    print("Extracting infos...")


def texto_tabela(texto):
    lista = []
    for linha in texto:
        lista.append(str(linha.text))
    return lista


def expand_page_previous_months():
    # expand page for previous months
    previous_months = today.month
    for p_i in range(1, previous_months):
        try:
            previous_button = browser.find_element_by_class_name("previous")
            if previous_button.text.split(" ")[-1] == "2017":
                previous_button.click()
        except:
            continue


def extract_page_info():
    tabela = pd.DataFrame(columns=["Date", "Card", "Description", "Values", "Category"])
    cartoes1 = browser.find_elements_by_class_name("bisa")
    cartoes2 = browser.find_elements_by_class_name("nbnk")

    cartoes = cartoes1 + cartoes2

    month_year = browser.find_element_by_class_name("month").text
    month_year = month_year.split(" ")
    month_list = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro",
                  "Novembro", "Dezembro"]

    for cartao in cartoes[1:]:
        try:
            cartao.click()
            days = texto_tabela(browser.find_elements_by_class_name("date"))
            description = texto_tabela(browser.find_elements_by_class_name("name"))
            values = texto_tabela(browser.find_elements_by_class_name("value-label"))
            categories = texto_tabela(browser.find_elements_by_class_name("category"))

            months = []
            for day_i in range(len(days)):
                if days[day_i] == "Data":
                    month = "Data"
                else:
                    month = month_list.index(month_year[0]) + 1
                    month_delay = days[:day_i].count("Data") - 1
                    # for m_i in range(len(month_separator)):
                    #    if day_i >= month_separator[m_i]:
                    #            month_delay = m_i
                    month = month - month_delay
                months.append(month)
                # dates.append(days[day_i].split(" ")[0] + "/" + str(month) + "/" + month_year[2])

            description = [desc for desc in description if desc != "Transação"]
            days = [day for day in days if day != "Data"]
            months = [month for month in months if month != "Data"]
            categories = [category for category in categories if category != "Categoria"]

            dates = []
            for day_i in range(len(days)):
                dates.append(str(days[day_i].split(" ")[0]) + "/" + str(months[day_i]) + "/" + month_year[2])

            tabela_cartao = pd.DataFrame(columns=["Date", "Card", "Description", "Values", "Category"])
            tabela_cartao["Date"] = dates
            tabela_cartao["Description"] = description
            tabela_cartao["Values"] = values
            tabela_cartao["Card"] = cartao.text
            tabela_cartao["Category"] = categories

            tabela = pd.concat([tabela, tabela_cartao], axis=0)
            del (tabela_cartao, description, days, values, dates, day_i)
        except:
            continue
    del (month_year)
    return tabela
    print("Infos extracted")
    browser.quit()

# TODO Close browser after scraping
