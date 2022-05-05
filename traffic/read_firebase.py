# Save data on Firebase
from tracemalloc import Snapshot
import firebase_admin
from firebase_admin import db
from datetime import datetime, timedelta
import re


def __init__():
    # Read info from realtimedatabase from firebase
    url = 'https://traffic-braga-default-rtdb.europe-west1.firebasedatabase.app/'
    db_name = '/traffic_tomtom_braga/'

    try:
        # connect to Firebase
        cred_object = firebase_admin.credentials.Certificate('./traffic-braga-firebase-adminsdk-qyjgx-1aa359d54c.json')
        default_app = firebase_admin.initialize_app(cred_object, {'databaseURL':url })
    except:
        print("Already connected")

def getByDate(date):
    date = date - timedelta(hours=1)
    date = date.strftime("%m-%d-%Y_%H:%M")

    date =  re.split(r"_|-|:", date)
    print("date splited: ", date)

    while int(date[-1]) % 10 != 0:
        date[-1] = int(date[-1]) - 1
      
    date = f"{date[0]}-{date[1]}-{date[2]}_{date[3]}:{date[4]}"
    print("new date: ", date)  
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

#best_sellers = ref.get()

#for key, value in best_sellers.items():
#    print(key)

# __init__()
# print(getByDate(str(datetime.now().strftime("%m-%d-%Y_%H:%M"))))