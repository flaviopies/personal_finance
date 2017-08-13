# -*- coding: utf-8 -*-
""" Created on Sat Jun 24 11:51:40 2017 @author: Flavio Pies """
import datetime as dt
import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn

today = dt.datetime.today()
filename = str(today.year) + str(today.month) + str(today.day) + "_Fatura"


def report_clean(tabela):
    print("report_clean")
    print("Data cleansing")
    tabela.index = tabela.reset_index().index
    tabela.index = range(len(tabela))
    for i in tabela.index:
        tabela.Values[i] = tabela.Values[i].replace("R$", "")
        tabela.Values[i] = tabela.Values[i].replace("\n(estimado)", "")
        tabela.Values[i] = tabela.Values[i].replace(".", "")
        tabela.Values[i] = tabela.Values[i].replace(",", ".")
        tabela.Values[i] = tabela.Values[i].replace(" ", "")
        tabela.Description[i] = tabela.Description[i].replace("\n+ Descrição e #tags", "")
    tabela.Values = tabela.Values.apply(float)
    tabela.Values = tabela.Values * -1

    month_dict = {"Janeiro": "1", "Fevereiro": "2", "Março": "3", "Abril": "4", "Maio": "5", "Junho": "6", "Julho": "7",
                  "Agosto": "8",
                  "Setembro": "9", "Outubro": "10", "Novembro": "11", "Dezembro": "12"}

    tabela.Date = tabela.Date.replace(month_dict, regex=True)
    tabela.Date = pd.to_datetime(tabela.Date, dayfirst=True)
    print(tabela.Date.max())
    tabela = tabela.rename(columns={"Date": "Data despesa", "Description": "Despesa", "Values": "R$", "Card": "Cartão",
                                    "Category": "Categoria"})
    tabela["Financiador"] = "Próprio"
    return tabela


def report_fp(tabela):
    print("report_fp")
    tabela = tabela[["Data despesa", "Cartão", "Despesa", "R$"]]
    cards = ["Mastercard", "Visa"]

    for i, card in enumerate(tabela["Cartão"].unique()):
        tabela.loc[tabela["Cartão"] == card, "Cartão"] = cards[i]

    tabela["Banco"] = "Itaú"
    tabela["Financiador"] = "Mirow & Co."
    tabela.loc[tabela["Cartão"] == "Mastercard", "Financiador"] = "Próprio"
    tabela.loc[tabela["Despesa"] == "PAGAMENTO EFETUADO", "Financiador"] = "Pagamentos"
    print(tabela["Data despesa"].max())
    return tabela


def old_information_fp(tabela):
    # In[]: - Summarizing with old infos, excluding duplicates with old infos and concatenating the relevant information
    print("old_information_fp")
    fatura = pd.read_excel(r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\Cartão de Crédito.xlsx",
                           sheetname="Fatura")
    # tabela = tabela.rename(columns={"Date": "Data despesa", "Description": "Despesa", "Values": "R$", "Card": "Cartão"})

    tabela = pd.concat([fatura, tabela], axis=0)

    tabela.drop_duplicates(["Data despesa", "Despesa", "R$", "Banco", "Cartão"], inplace=True)

    tabela = tabela[tabela["Categoria"].astype(str) == "nan"]
    fatura = pd.concat([fatura, tabela], axis=0)
    dfs = [fatura, tabela]
    print(fatura["Data despesa"].max())
    return dfs


def export_excel(tabela):
    # In[]: - Summarizing in Pandas Dataframe and exporting to excel
    print("Exporting to excel")
    today = dt.datetime.today()
    filename = str(today.year) + str(today.month) + str(today.day) + "_Fatura"
    writer = pd.ExcelWriter(
        r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\04_Consultas\\" + filename + ".xlsx",
        engine="xlsxwriter")
    try:
        tabela.to_excel(writer, sheet_name="Dados")
        del (writer)
        print("Exported to excel")
        print("Success!")
    except:
        print("Failed to export")


def report_prep(fatura):
    # FIXME filtro errado aqui
    fatura["Ano"] = fatura["Data despesa"].dt.year
    fatura["Semana"] = fatura["Data despesa"].dt.week
    fatura["Mes"] = fatura["Data despesa"].dt.month
    fatura["Dia semana"] = ((fatura["Data despesa"].dt.weekday + 1) % 7) + 1
    fatura["Cat_grupo"] = "Rotina"
    fatura.loc[fatura.Categoria == "Férias", "Cat_grupo"] = "Férias"
    # fatura.loc[fatura["Dia semana"] == 7, "Semana"] = fatura[fatura["Dia semana"] == 7].Semana - 1
    fatura = fatura[(fatura.Financiador == "Próprio") & (fatura.Ano == 2017) & (
    fatura.Semana <= dt.datetime.today().isocalendar()[1])]
    print("Relatório considera até semana " + str(dt.datetime.today().isocalendar()[1]))
    print(fatura["Data despesa"].max())
    return fatura


def charts(fatura):
    # TODO Separate charts function in 4+ charts functions
    myDirname = os.path.normpath(r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\04_Consultas\\")

    plt.figure()
    pt = fatura[(fatura["R$"] > 0)].pivot_table(values="R$", index=["Mes", "Semana"], columns="Dia semana",
                                                aggfunc="sum")
    sns_heatmap = seaborn.heatmap(pt, annot=True, fmt='.0f', cmap="YlGnBu", linewidth=0.3, annot_kws={"size": 8})
    sns_heatmap.set_yticklabels(labels=pt.index.sort_values(ascending=False), rotation=0)
    sns_heatmap = sns_heatmap.get_figure()
    sns_heatmap.savefig(os.path.join(myDirname, filename + "_heatmap"))

    # sns_heatmap = seaborn.heatmap(fatura[(fatura["R$"] > 0)].pivot_table(values="R$",index=["Mes","Semana"],columns="Dia semana",      #     aggfunc="sum"),annot=True,fmt = '.0f',cmap="YlGnBu",linewidth=0.3).get_figure()
    # sns_heatmap.savefig(os.path.join(myDirname,filename +"_heatmap"))

    plt.figure()
    sns_barchart_week = seaborn.barplot(x=fatura[fatura.Ano == 2017].Semana, y=fatura["R$"], estimator=sum, ci=None,
                                        palette="GnBu_d", hue=fatura["Cat_grupo"]).get_figure()
    sns_barchart_week.savefig(os.path.join(myDirname, filename + "_barchart_week"))

    plt.figure()
    # sns_heatmap_cat = seaborn.heatmap(fatura[(fatura["R$"] > 0)].pivot_table(values="R$",index="Categoria",columns="Mes",#aggfunc="sum"),annot=True,fmt = '.0f',cmap="YlGnBu",linewidth=0.3).get_figure()
    # plt.yticks(rotation=0)
    # sns_heatmap_cat.savefig(os.path.join(myDirname,filename +"_heatmap_cat"))

    seaborn.set(font_scale=0.8)
    pt_cat = fatura[(fatura["R$"] > 0)].pivot_table(values="R$", index="Categoria", columns="Mes", aggfunc="sum")
    sns_heatmap_cat = seaborn.heatmap(pt_cat, annot=True, fmt='.0f', cmap="YlGnBu", linewidth=0.3)
    sns_heatmap_cat.set_yticklabels(labels=pt_cat.index.sort_values(ascending=False), rotation=0)
    sns_heatmap_cat = sns_heatmap_cat.get_figure()
    sns_heatmap_cat.savefig(os.path.join(myDirname, filename + "_heatmap_cat"))

    plt.figure()
    plt.yticks(rotation=0)
    sns_barchart_month = seaborn.barplot(x=fatura[fatura.Ano == 2017].Mes, y=fatura["R$"], estimator=sum, ci=None,
                                         palette="GnBu_d", hue=fatura["Cat_grupo"]).get_figure()
    sns_barchart_month.savefig(os.path.join(myDirname, filename + "_barchart_month"))
    print(fatura["Data despesa"].max())
    # TODO Create new charts
    attachments = [os.path.join(myDirname, filename + "_barchart_month.png"),
                   os.path.join(myDirname, filename + "_heatmap_cat.png"),
                   os.path.join(myDirname, filename + "_barchart_week.png"),
                   os.path.join(myDirname, filename + "_heatmap.png")
                   ]


def smart_charts(fatura):
    chart_sns_heatmap(fatura)
    chart_sns_barchart_week(fatura)
    chart_sns_barchart_month(fatura)
    chart_sns_heatmap_cat(fatura)


def chart_sns_heatmap(fatura):
    myDirname = os.path.normpath(r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\04_Consultas\\")

    plt.figure()
    pt = fatura[(fatura["R$"] > 0)].pivot_table(values="R$", index=["Mes", "Semana"], columns="Dia semana",
                                                aggfunc="sum")
    sns_heatmap = seaborn.heatmap(pt, annot=True, fmt='.0f', cmap="YlGnBu", linewidth=0.3, annot_kws={"size": 8})
    sns_heatmap.set_yticklabels(labels=pt.index.sort_values(ascending=False), rotation=0)
    sns_heatmap = sns_heatmap.get_figure()
    sns_heatmap.savefig(os.path.join(myDirname, filename + "_heatmap"))


def chart_sns_barchart_week(fatura):
    myDirname = os.path.normpath(r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\04_Consultas\\")
    plt.figure()
    sns_barchart_week = seaborn.barplot(x=fatura[fatura.Ano == 2017].Semana, y=fatura["R$"], estimator=sum, ci=None,
                                        palette="GnBu_d", hue=fatura["Cat_grupo"]).get_figure()
    sns_barchart_week.savefig(os.path.join(myDirname, filename + "_barchart_week"))


def chart_sns_heatmap_cat(fatura):
    myDirname = os.path.normpath(r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\04_Consultas\\")
    plt.figure()
    seaborn.set(font_scale=0.8)
    pt_cat = fatura[(fatura["R$"] > 0)].pivot_table(values="R$", index="Categoria", columns="Mes", aggfunc="sum")
    sns_heatmap_cat = seaborn.heatmap(pt_cat, annot=True, fmt='.0f', cmap="YlGnBu", linewidth=0.3)
    sns_heatmap_cat.set_yticklabels(labels=pt_cat.index.sort_values(ascending=False), rotation=0)
    sns_heatmap_cat = sns_heatmap_cat.get_figure()
    sns_heatmap_cat.savefig(os.path.join(myDirname, filename + "_heatmap_cat"))


def chart_sns_barchart_month(fatura):
    myDirname = os.path.normpath(r"C:\Users\Flavio Pies\Dropbox (Pessoal)\01_Pessoal\Bancos\02_Cartão\04_Consultas\\")

    plt.figure()
    plt.yticks(rotation=0)
    sns_barchart_month = seaborn.barplot(x=fatura[fatura.Ano == 2017].Mes, y=fatura["R$"], estimator=sum, ci=None,
                                         palette="GnBu_d", hue=fatura["Cat_grupo"]).get_figure()
    sns_barchart_month.savefig(os.path.join(myDirname, filename + "_barchart_month"))
    print(fatura["Data despesa"].max())

# TODO Create new charts
