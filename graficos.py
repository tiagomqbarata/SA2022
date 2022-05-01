# -*- coding: utf-8 -*-
"""
Created on Sun May  1 16:14:24 2022

@author: tiago
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import datetime as dt


df = pd.read_csv("data.csv")

# def date_timeToRecord_date(value):
#     # 2019-02-13 23:00:00
#     value = re.split("_|-|:", value)
#     return dt.datetime.strptime(value[2] + '-' + value[0] + '-' + value[1] + ' ' + value[3] + ':' + value[4],'%Y-%m-%d %H:%M')
     

# df["record_date"] = df["date_time"].map(lambda x: date_timeToRecord_date(x))
# df.drop("Index", axis=1, inplace=True)

df.transito = df.transito * df.confidence

df.to_csv("data.csv", index=False)

df.record_date = pd.to_datetime(df.record_date)
df["day_week"] = df["record_date"].dt.day_name(locale='pt')


# Divisão por Localizações
dfsByLocal = {}

for local in df.local.unique():
    dfsByLocal[local] = df[df["local"] == local]


def makeGraphic(data, local):
    # Change the style of plot
    plt.style.use('seaborn-darkgrid')
     
    # Create a color palette
    palette = plt.get_cmap('Set1')
    
    plt.plot(data["record_date"], data["transito"], marker='', color=palette(1), linewidth=1, alpha=0.9)
    
    # Add legend
    plt.legend(loc=2, ncol=2)
     
    # Add titles
    plt.title(local, loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("DateTime")
    plt.ylabel("Traffic")

    plt.savefig('Gráficos/Trafico_' + local + '.png')
 

for local in dfsByLocal.keys():
    makeGraphic(dfsByLocal[local], local)



########################################################################
toGraphic = {}

for local in dfsByLocal.keys():
    toGraphic[local] = ([], [])
    for day_week in df.day_week.unique():
        toGraphic[local][0].append(re.split("-", day_week)[0])
        toGraphic[local][1].append(dfsByLocal[local][dfsByLocal[local]["day_week"] == day_week].transito.mean())
    

def makeGraphic1(data, local):
    # Change the style of plot
    plt.style.use('seaborn-darkgrid')
     
    # Create a color palette
    palette = plt.get_cmap('Set1')
    
    y_pos = np.arange(len(data[0]))
    
    plt.bar(y_pos, data[1], color=palette(1))

    plt.xticks(y_pos, data[0])
    
    plt.legend(loc=2, ncol=2)
     
    # Add titles
    plt.title(local, loc='left', fontsize=12, fontweight=0, color='orange')
    plt.xlabel("Dia da Semana")
    plt.ylabel("Média do Transito")
    
    plt.savefig('Gráficos/TraficoDW_' + local + '.png')
 
for local in dfsByLocal.keys():
    makeGraphic1(toGraphic[local], local)