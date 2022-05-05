from pyparsing import empty
import read_firebase as db
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk
import datetime as dt
from datetime import datetime
import re


db.__init__()


# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

def load_data(date = datetime.now()):
    dados = db.getByDate(date)
    datetime = []
    lat = []
    lon = []
    
    print(type(dados))

    for key in dados.keys():
        # gera um valor para o trânsito com base numa expressão matemática
        number = (1 - (float(dados[key]["currentSpeed"])/ float(dados[key]["freeFlowSpeed"]) + float(dados[key]["freeFlowTravelTime"])/float(dados[key]["currentTravelTime"]))/2 * float(dados[key]["confidence"])) * 100

        number = int(number)

        for i in range(-1,number):
            # coloca a date_time no formato pretendido de dados
            datetime.append(dt.datetime.strptime(dados[key]["date_time"],'%m-%d-%Y_%H:%M:%S'))
            lat.append(dados[key]["latitude"])
            lon.append(dados[key]["longitude"])
        
        
    data = pd.DataFrame()

    data["date/time"] = datetime
    data["lat"] = lat
    data["lon"] = lon

    return data

def load_data_allDay(date = datetime.now(), citiesNotShow = set()):
    dados = db.getByDate_AllDay(date)

    if len(dados) == 0:
        return pd.DataFrame()


    df = pd.DataFrame.from_dict(dados, orient='index')
    df["transito"] = ((1 - (df.currentSpeed / df.freeFlowSpeed + df.freeFlowTravelTime / df.currentTravelTime)/2) * df.confidence) * 100
    def date_timeToRecord_date(value):
        # 2019-02-13 23:00:00
        return dt.datetime.strptime(value,'%m-%d-%Y_%H:%M:%S').strftime("%H:%M")

    df["time"] = df["date_time"].map(lambda x: date_timeToRecord_date(x))
    df.drop("date_time", axis=1, inplace=True)


    df = df.set_index(df.time)

    data = pd.DataFrame(index=df.time.unique().sort())


    for local in df.local.unique():
        data[local] = df[df.local == local].transito

    for elem in citiesNotShow:
        data = data.drop(elem, axis=1)

    return data

# FUNCTION FOR AIRPORT MAPS
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["lon", "lat"],
                    radius=100,
                    elevation_scale=2,
                    elevation_range=[0, 200],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

# TODO
def filterdata(date_selected):
    return load_data(date_selected)

def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

st.title("Tráfego em Braga")

st.header("Trânsito em tempo real", anchor="map")

date = st.date_input(
    "Dia a ver o tráfego?",
    datetime.date(datetime.now()))

time = st.time_input('Hora a ver o tráfego?', datetime.time(datetime.now()))

hour_selected = dt.datetime.combine(date,time)

if st.button('Agora'):
    hour_selected = datetime.now()

st.subheader(hour_selected.strftime("Em visualização %d/%m/%Y %H:%M"))
midpoint = (41.54, -8.42)
map(filterdata(hour_selected), midpoint[0], midpoint[1], 13)

############################################################################################3

st.header("Trânsito diário", anchor="byDay")

date2 = st.date_input(
     "Dia",
     datetime.date(datetime.now()))

if st.button('Hoje'):
    date2 = datetime.date(datetime.now())

st.subheader(date2.strftime("Em visualização %d/%m/%Y"))

citiesNotShow = set()

row2_1, row2_2 = st.columns((8,2))

with row2_2:
    check = {}
    for city in load_data_allDay().columns.sort_values():
        check[city] = st.checkbox(city, value=True)

    for key in check.keys():
        if not check[key]:
            citiesNotShow.add(key)
        else:
            try:
                citiesNotShow.remove(key)
            except:
                pass
            

with row2_1:
    st.line_chart(load_data_allDay(date2, citiesNotShow))
