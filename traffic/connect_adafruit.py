# Import standard python modules
import time

# import Adafruit Blinka
import digitalio
# import Adafruit IO REST client.
from Adafruit_IO import Client, Feed, RequestError

import script_web as sw

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = "aio_Idsh23lTnefURk6rzAwxZuhSdBxU"

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = "tiagomqbarata"

# Create an instance of the REST client.
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

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

sw.__init__()
dicionario = sw.getByDate()

for key in dicionario.keys():
    aio.send_data(localsKey[dicionario[key]["local"]], "20")