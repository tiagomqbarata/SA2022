import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
from datetime import datetime, timedelta
import re
import firebase_admin
from firebase_admin import db

# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

def __init__():
    # Read info from realtimedatabase from firebase
    url = 'https://traffic-braga-default-rtdb.europe-west1.firebasedatabase.app/'
    db_name = '/traffic_tomtom_braga/'

    try:
        # connect to Firebase
        key = {
                "type": "service_account",
                "project_id": "traffic-braga",
                "private_key_id": "1aa359d54c246f2a167a3e0e56ae10c758a834be",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCgmIzABA9EEqkC\nPmIO8RhBfths/qXhT1zg9GU4bsFytkT3dlB2qT7ej0sgry7dcqLEiXBwM3me9dqi\nTsLj+lkZu2K+v04n+HprWFbZD02841i+8A9zgFxs/qto7fTStokxx0PPIJexbgJD\n3zWSFjaelBswjAgfgPkau99/zP49k3emJvsYIYYTmrfJjtKOwsOV7JUcoYXuLqsp\nWspP1vjmR48vugT2U76/zb2g4j8HKS3+iiiuALaoimxMA+/gyJqfEy46CWVdtR84\neigVHc/FEVvDbwDnRAZRxY8q0DStpNm5/TZybRfrsTCrSPvtysfAtLKQ+Kkh+s27\nlA4ROR1BAgMBAAECggEAFYiprtbx2RXgyv05wXkl4HpgDiq4bBVr2yTKLHP6xSVC\n6s+sNbe3R2PSwLzcvYgxN8XvaWFtmG6s9Ks3n2wikGcQ9DTLXQ6zaOYSgc53L7G9\nuknkOH+TZRtiOT1XC6i64rguaSfx+dz0uXcaRCQYX3vKiDWZTT10/tcG6VMVGtpk\nggwzXzdHq2kaSLXNq+x6xGdNk6/TkjVuT4NbD9DGpKt95TzIhBuVIRxPbViGhQgR\ntcia6te/fTdc86yrvXus4xltEx4hpSWqx984DM/pa4gqQXbMKGH4GsefOtwPDKLe\nkIhpRv8nYyF9m6XbEl1/0Ik0HcYEBeCnko96xAG3ZQKBgQDPsrqwCOefeJ+cEoqa\nlRs2Qmeo1wGf1KeyylZn2ohVYT68cU6uC9T7V7fUFNfObVV6idFD5Fd7x+Izpqw8\n3xN4klHQmVV7bR3z/pMJx0EmhYiS+3XBZSvtSFK1awnYzuPArtLNFI4SSyGdzR/r\nOSCjHKZ8vp5Y6RQUZMHmA1jrNwKBgQDF8ZihEsfad2rsvZaGy1IoEVbvKAPXoUL7\nI+smRF7fBddjvYkILRPmtCo2DpdYIifyoyOrlFIlQ0qxnAWOGhubkJstvR6hWtWm\nGQ1K/ceo+5d+B7tTNKiEzXH58fDk08sdAOb8opmND+Lv2i9bLe7hC2Kf7gsjpORt\ny1YuhFmnRwKBgAH2MzM0clOcRQ2pUyvQmrgxel8q4LYMwSS8KoLCmqULzRbkjxSv\nwew50N+s7rjhaXxFzvcwMe9WXPmV6myMwtdRsnog6KDI0A6c6fCetCvT+Q1CWMNh\n3D9afoV+JFKq6ZXJUO5k8k6T7RZbeKC1ImzH+X6WIlK+qNTkerxcbbuTAoGAD7uh\nLwRIIEQnmoODKFmWwRqHt2CN1aC6qy1yrkr243EaapIRBzZWA5tEU6GbQ+ULGcz/\ns86JLO8JS86j3mSS1y2KN/t1KMwIeTg6h0Bekz7UDq9co0NnNY8CxSQGyplO5pJA\nycm+vKiLmBbWdr/S4c4+24lXF1Eu2s8znWTln1cCgYEAic+hjzQRz4KfnFh78Ddj\n76/bqSUSU7z15Iaj6dv7d8xYDN73EKBAY+KyuEKzzkQFkFkWN5GA5sjEmqEz3pQz\nbRBV85AqG5eunmu8sfyJ79WxIoYxVTc/700sl2tRhLnaJi8EUQxpRrTxZV6K2piF\nozdRr8S5X877BFSFYKdbGuM=\n-----END PRIVATE KEY-----\n",
                "client_email": "firebase-adminsdk-qyjgx@traffic-braga.iam.gserviceaccount.com",
                "client_id": "105716446062720664266",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-qyjgx%40traffic-braga.iam.gserviceaccount.com"
                }
        cred_object = firebase_admin.credentials.Certificate(key)
        default_app = firebase_admin.initialize_app(cred_object, {'databaseURL':url })
    except:
        print("Already connected")

def getByDate(date = datetime.now()):
    date = date - timedelta(hours=1)
    date = date.strftime("%m-%d-%Y_%H:%M")

    date =  re.split(r"_|-|:", date)

    while int(date[-1]) % 10 != 0:
        date[-1] = int(date[-1]) - 1
      
    date = f"{date[0]}-{date[1]}-{date[2]}_{date[3]}:{date[4]}"
    ref = db.reference('traffic_tomtom_braga/')
    dados = ref.order_by_key().start_at(date).limit_to_first(10).get()

    if dados == None:
        return {}
    else:
        return dados

def getByDate_AllDay(date):
    date = date - timedelta(hours=1)
    date = date.strftime("%m-%d-%Y")

    ref = db.reference('traffic_tomtom_braga/')
    dados = ref.order_by_key().start_at(date).limit_to_first(1440).get()

    if dados == None:
        return {}
    else:
        return dados

def getByDate_AllWeek(date):
    date = date - timedelta(hours=1)
    date = date.strftime("%m-%d-%Y")

    ref = db.reference('traffic_tomtom_braga/')
    dados = ref.order_by_key().start_at(date).limit_to_first(1440).get()

    if dados == None:
        return {}
    else:
        return dados

def load_data(date = datetime.now()):
    dados = getByDate(date)
    datetime = []
    lat = []
    lon = []
    
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
    dados = getByDate_AllDay(date)

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

def load_data_week(date = datetime.now(), citiesNotShow = set()):
    dados = {}

    for i in range(7):
        dados.update(getByDate_AllDay(date - dt.timedelta(days=i)))

    if len(dados) == 0:
        return pd.DataFrame()

    df = pd.DataFrame.from_dict(dados, orient='index')
    df["transito"] = ((1 - (df.currentSpeed / df.freeFlowSpeed + df.freeFlowTravelTime / df.currentTravelTime)/2) * df.confidence) * 100

    def date_timeToRecord_date(value):
            # 2019-02-13 23:00:00
            return dt.datetime.strptime(value,'%m-%d-%Y_%H:%M:%S')

    df["time_record"] = df["date_time"].map(lambda x: date_timeToRecord_date(x))
    df.drop("date_time", axis=1, inplace=True)
    df.time_record = pd.to_datetime(df.time_record)
    df["day_week"] = df.time_record.dt.day_name(locale='pt')

    df.drop("time_record", axis=1, inplace=True)

    diasDaSemana = {}

    colunas = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado',  'Domingo']
    colunas = colunas[int(date.strftime("%w")):] + colunas[:int(date.strftime("%w"))]

    for i in range(0, len(colunas)):
        diasDaSemana[colunas[i]] = str(i+1)
        colunas[i] = str(i+1) + " - " + colunas[i]
        

    dicionario = {}
    for local in np.sort(df.local.unique()):
        df_local = df[df.local == local]
        aux_df = pd.DataFrame(columns=colunas, index=["Transito"])
        for day in df.day_week.unique():
            aux_df[diasDaSemana[day] + ' - ' + day] = df_local[df.day_week == day].transito.mean()
        dicionario[local] = aux_df.T


    return dicionario


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

def filterdata(date_selected):
    return load_data(date_selected)

def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

__init__()

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


st.header("Trânsito Semanal", anchor="byWeek")

date3 = st.date_input(
     "Dia final da semana",
     datetime.date(datetime.now()))

if st.button('Esta semana'):
    date3 = datetime.date(datetime.now())

dateInit = (date3 - dt.timedelta(days=6)).strftime("%d/%m/%Y")
st.subheader(date3.strftime(f"Em visualização {dateInit} - %d/%m/%Y"))

row3_1, row3_2 = st.columns((2,6))

barData = load_data_week(date3)

tuppleLocals = tuple(barData.keys())

with row3_1:
    localChoosed = st.radio(
     "Escolhe o local",
     tuppleLocals)

with row3_2:
    st.bar_chart(barData[localChoosed])