import re
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns

#new changes
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import itertools

from scipy import stats


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10,5))
    plt.title('visualisation')
    plt.plot(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('visualistion')
    plt.ylabel('values')
    plt.tight_layout()
    graph = get_graph()
    return graph

def get_seaplot():
    df = sns.load_dataset("penguins")
    sns.pairplot(df, hue="species")
    graph = get_graph
    return graph


def get_first(f):
    """########"""
    #Traitement
    rooms = pd.read_csv(f,sep=";")
    #print(rooms)
    #print(rooms.info())

    rooms["Debut.evenement"] = pd.to_datetime(rooms["Debut.evenement"],format='%d/%m/%Y %H:%M')
    rooms["Fin.evenement"] = pd.to_datetime(rooms["Fin.evenement"],format='%d/%m/%Y %H:%M')
    #print(rooms.info())

    date_rng = pd.date_range('2020-01-01', '2021-12-31',freq='12H')
    #print(date_rng)
    occupation=[0 for i in date_rng]

    for i in range(len(rooms["Code.Ressource"])):
        j=0
        while rooms["Fin.evenement"][i] >= date_rng[j] :
            if not (rooms["Fin.evenement"][i]<=date_rng[j] or rooms["Debut.evenement"][i]>date_rng[j+1]):
                occupation[j]+=1
            j+=1
        if i%100==0:
            print(i,end=" ")
    print('fin')

    """
    for i in range(len(date_rng)):
        if occupation[i]!=0:
            print(date_rng[i],occupation[i],end=';   ')
    """

    """########"""
    df = pd.DataFrame({'nb salles':occupation},index=pd.to_datetime(date_rng))
    df.insert(1, 'year', df.index.year)
    df.insert(2, 'month', df.index.month)
    df.insert(3, 'week', df.index.week)
    df.insert(4, 'hour', df.index.hour)
    df.insert(5, 'weekday', df.index.weekday)
    print(df)

    """########"""
    #Graphique
    plt.close()

    fig, axes = plt.subplots()

    df1 = df[( (df['hour']>5) & (df['hour']<21) )]
    df2 = df1[( ((df["year"]==2020) & (df["week"]>33)) | ((df["year"]==2021) & (df["week"]<25)) )]
    df3 = df2.pivot_table(index="weekday",columns=["year","week"],values='nb salles',aggfunc=np.mean)

    plt.title("Nombre moyen de salles occupées par semaine et jour de la semaine")
    sns.heatmap(df3, cmap="Reds", ax=axes)
    axes.yaxis.set_ticklabels(['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi','Samedi','Dimanche'],rotation = 0)
    axes.set_xlabel('année scolaire 2020/2021')
    axes.set_ylabel("jour de la semaine")
    graph = get_graph();
    return graph;
