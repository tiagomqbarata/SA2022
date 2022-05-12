# importing the required libraries
import requests
# Save data on Firebase
import firebase_admin
from firebase_admin import db
from datetime import datetime
# Import standard python modules
import time

# import Adafruit Blinka
import digitalio
# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError


# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = "aio_Idsh23lTnefURk6rzAwxZuhSdBxU"

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = "tiagomqbarata"

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)


# Pontos de Braga de onde foi feita a recolha de informação sobre o trânsito 
# coordenadas: latitude  , longitude     | descrição local
#
#              41.5556929, -8.3992663    | Meliá
#              41.557563 , -8.4072979    | Braga Parque
#              41.5436167, -8.432434     | Rotunda Santos da Cunha
#              41.5488151, -8.4336238    | Estação de Comboios
#              41.5416698, -8.4022779    | Centro comercial Minho Center
#              41.5465807, -8.4201942    | Avenida da Liberdade
#              41.5351848, -8.437027     | Bosh
#              41.5498311, -8.4285616    | Sé de Braga
#              41.5278372, -8.417844     | Hospital Privado de Braga
#              41.5593592, -8.4462021    | Real Taberna


locais_Braga = {
  "Meliá": (41.5556929, -8.3992663),
  "Braga Parque": (41.557563, -8.4072979),
  "Rotunda Santos da Cunha": (41.5436167, -8.432434),
  "Estação de Comboios": (41.5488151, -8.4336238),
  "Centro comercial Minho Center": (41.5416698, -8.4022779),
  "Avenida da Liberdade": (41.5465807, -8.4201942),
  "Bosh": (41.5351848, -8.437027 ),
  "Sé de Braga": (41.5498311, -8.4285616 ),
  "Hospital Privado de Braga": (41.5278372, -8.417844),
  "Real Taberna": (41.5593592, -8.4462021)
}

localsKey = {'Avenida da Liberdade' : 'traffic.avenidaliberdade',
             'Bosh' : 'traffic.bosh',
             'Braga Parque' : 'traffic.bragaparque',
             'Centro comercial Minho Center' : 'traffic.minhocenter',
             'Estação de Comboios' : 'traffic.estacao',
             'Hospital Privado de Braga' : 'traffic.hospitalprivado',
             'Meliá' : 'traffic.melia',
             'Real Taberna' : 'traffic.realtaberna',
             'Rotunda Santos da Cunha' : 'traffic.santosdacunha',
             'Sé de Braga' : 'traffic.sedebraga'}


# Enter the api key of tomtom here
api_key = "k3sBSruXiXGh9TdVtOL5qQfC4FgIHwKA"
# Base url for the tomtom api
root_url = 'https://api.tomtom.com/traffic/services/4/flowSegmentData/reduced-sensitivity/10/json?' 


# Save info into realtimedatabase from firebase
url = 'https://traffic-braga-default-rtdb.europe-west1.firebasedatabase.app/'
db_name = '/traffic_tomtom_braga/'

# connect to Firebase
cred_object = firebase_admin.credentials.Certificate('./traffic-braga-firebase-adminsdk-qyjgx-1aa359d54c.json')
default_app = firebase_admin.initialize_app(cred_object, {
    'databaseURL':url })

ref = db.reference(db_name)

for local, coordenadas in locais_Braga.items():
    print("\nlocal: ", local, "\nlatitude: ", coordenadas[0], "\nlongitude: ", coordenadas[1])
    latitude = coordenadas[0]
    longitude = coordenadas[1]
    # Building the final url for the API call
    url = f'{root_url}key={api_key}&point={latitude},{longitude}'
    # sending a get request at the url
    r = requests.get(url)
    # displaying the json weather data returned by the api
    print(r.json())
    data = r.json()

    currentSpeed = data['flowSegmentData']['currentSpeed']
    freeFlowSpeed = data['flowSegmentData']['freeFlowSpeed']
    currentTravelTime = data['flowSegmentData']['currentTravelTime']
    freeFlowTravelTime = data['flowSegmentData']['freeFlowTravelTime']
    confidence = data['flowSegmentData']['confidence']

    now = datetime.now()
    date_time = now.strftime("%m-%d-%Y_%H:%M:%S")
    id_registo = date_time + "_" + local

    # enviar novo registo para o Firebase
    ref.child(id_registo).set(
        {
            
                'currentSpeed': currentSpeed,
                'freeFlowSpeed': freeFlowSpeed,
                'currentTravelTime': currentTravelTime,
                'freeFlowTravelTime': freeFlowTravelTime,
                'confidence':confidence,
                'date_time':date_time,
                'local':local,
                'latitude':latitude,
                'longitude':longitude 
            
        }
    )

    transito = ((1 - (int(currentSpeed) / int(freeFlowSpeed) + int(freeFlowTravelTime) / int(currentTravelTime))/2) * int(confidence)) * 100

    aio.send_data(localsKey[local], str(transito))

    




