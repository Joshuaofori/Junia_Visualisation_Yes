
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
import itertools
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import seaborn as sns

#Booléen
bool_percent=False
bool_smooth=True

bool_weekend=False

bool_annee=False
bool_mois=True
choix_mois=9
choix_annee=2020 if choix_mois>=9 else 2021
bool_semaine=False
choix_semaine=38
amphi = pd.read_csv("/home/joshua/Downloads/csv_amphi.csv",sep=";",encoding="cp1252")

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

amphi["date"] = pd.to_datetime(amphi["date"],format='%d/%m/%Y')
amphi["Debut.evenement"] = pd.to_datetime(amphi["Début.Événement"],format='%d/%m/%Y %H:%M')
amphi["Fin.evenement"] = pd.to_datetime(amphi["Fin.Événement"],format='%d/%m/%Y %H:%M')

nb_places = amphi["Nombre de places.Ressource"][0]
#print(amphi.info())

date_rng = pd.date_range(min(amphi["Debut.evenement"]), max(amphi["Fin.evenement"]),freq='0.5H')
#print(date_rng)

# associe à chaque demi-heure le nombre d'élèves dans la salle
# temps de chargement : 4 min
nb_eleves=[0 for i in date_rng]

for i in range(len(amphi["Fin.evenement"])):
    j=0
    while j<len(date_rng):
        if not (amphi["Fin.evenement"][i]<=date_rng[j] or amphi["Debut.evenement"][i]>date_rng[j]):
            nb_eleves[j]=max(nb_eleves[j],amphi["Nombre d'apprenants inscrits.Intervention"][i])
        j+=1
    if i%int(len(amphi["Code.Ressource"])/10)==0:
        print(round(i/len(amphi["Code.Ressource"]),1),end=" ")
print('fin')

df_eleves = pd.DataFrame({'nb_eleves':nb_eleves},index=pd.to_datetime(date_rng))
df_eleves.insert(1, 'year', df_eleves.index.isocalendar().year)
df_eleves.insert(2, 'month', df_eleves.index.month)
df_eleves.insert(3, 'week', df_eleves.index.isocalendar().week)
df_eleves.insert(4, 'weekday', df_eleves.index.weekday)
df_eleves.insert(5, 'time', df_eleves.index.time)
print(df_eleves)


def get_graph2():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_util2_first():
    df_eleves_graphe=df_eleves.copy()
    df_eleves_graphe=df_eleves_graphe.resample('1D').apply(lambda x : max(x))
    plt.close()
    fig, ax = plt.subplots()

    if bool_weekend:
      df_eleves_graphe=df_eleves_graphe[ ((df_eleves_graphe["weekday"]!=6) & (df_eleves_graphe["weekday"]!=5)) ]


    if bool_percent:
        df_eleves_graphe["nb_eleves"]=df_eleves_graphe["nb_eleves"]/nb_places*100
        cap=100
        ax.set_ylabel("Pourcentage d'élèves dans la salle")
    else:
        cap=150
        ax.set_ylabel("nombre d'élèves dans la salle")

    if bool_annee:

        plt.plot(df_eleves_graphe.index,df_eleves_graphe["nb_eleves"], color="black")
        ax.axhline(cap, color="red", ls="--")
        if bool_smooth:
            y_smooth=smooth(df_eleves_graphe["nb_eleves"],30)
            plt.plot(df_eleves_graphe.index, y_smooth, color="#68A3E6" )
            plt.fill_between(df_eleves_graphe.index, y_smooth, color = '#97BDE7')

        ax.set_xlabel('année scolaire 2020/2021')
        plt.title("Capacité de l'amphi C304 ("+str(nb_places)+" places) sur l'année 2020/21, par jour")

    elif bool_mois:
        df_eleves_mois = df_eleves[ (df_eleves["month"]==choix_mois) ]
        plt.plot(df_eleves_mois.index,df_eleves_mois["nb_eleves"], color="black")
        ax.axhline(cap, color="red", ls="--")
    if bool_smooth:
        y_smooth=smooth(df_eleves_mois["nb_eleves"],60)
        plt.plot(df_eleves_mois.index, y_smooth, color="#68A3E6" )
        plt.fill_between(df_eleves_mois.index, y_smooth, color = '#97BDE7')

    ax.set_xlabel('mois de '+calendar.month_name[choix_mois])
    plt.title("Capacité de l'amphi C304 ("+str(nb_places)+" places)")
    graph = get_graph2()
    return graph




