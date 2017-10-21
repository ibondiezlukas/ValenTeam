#!/usr/bin/python

import time
import ssl
import serial

from paho.mqtt import client as mqtt
#from paho.mqtt import client as mqtt


#

########## You need only modify this section start ##########
# You can generate the SAS with Device Explorer Example SharedAccessSignature = "SharedAccessSignature
#sr=kevinsay.azure-devices.net%2fdevices%2fmygreatdevice&sig=ON2EYJR1hUC84rJSMe%2fCrBdb8lcIr7A%3d&se=15055292" SharedAccessSignature = "SharedAccessSignature
#sr=ValenHub.azure-devices.net&sig=B7Hs6nZos4veopgl8OdP%2FHZdUK35GUEht3DD6V8c%2F%2F8%3D&se=1540115522&skn=iothubowner"

SharedAccessSignature = "SharedAccessSignature sr=ValenHub.azure-devices.net%2Fdevices%2FRaspberry01&sig=ueFtRoaew0HPO6lJgowKe00eL%2FGDlwfBEHnEUK9o6q4%3D&se=1540119980"

# download the cer from https://ssl-tools.net/certificates/d4de20d05e66fc53fe1a50882c78db2852cae474.pem
BaltimoreCyberTrustRootCER = "iot.cer"
########### You need only modify this section end ###########
hubName = SharedAccessSignature.split("%2F")[0].split("=")[1]
deviceName = SharedAccessSignature.split("%2F")[2].split("&")[0]
#deviceName = "raspberry01"

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)

print "HUB NAME:" + hubName
print "DEVICE NAME:" + deviceName

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))
    client.subscribe("devices/" + deviceName + "/messages/devicebound/#")

def on_disconnect(client, userdata, rc):
    print ("Disconnected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print (msg.topic+" "+str(msg.payload))
    # Do this only if you want to send a reply message every time you receive one
    client.publish("devices/" + deviceName + "/messages/events/", "{id=1}", qos=1)

def on_publish(client, userdata, mid):
    print ("Sent message")

def readSerial():
        out = ""
        while ser.inWaiting() > 0:
                 out += ser.read(1)
        return out

def jsonize(installation):
        # installation is an string containing the values received by the serial link $hum:36$temp:26$lleno:0$fire:0 $type:paper$pos:40.446;79.982

        status = {}
        default = {"Identificator": "NULL", "Type":"NULL", "Temperature" :"NULL", "Distance":"NULL", "Humidity" : "NULL", "Fire" : "NULL", "Location":"NULL"}
        fields = installation.split('$')
        print ("json nodo: " + installation)

        # $id:02$hum:40$temp:26$lleno:0$fire:0
        # $id:02$type:paper$pos:40.446;79.982

        for element in fields:
                print "current element: " + element
                current = element.split(':')
                if current[0] == "id":
                        default["Identificator"] = current[1]
                elif current[0] == "hum":
                        default["Humidity"] = current[1]
                elif current[0] == "temp":
                        default["Temperature"] = current[1]
                elif current[0] == "lleno":
                        default["Distance"] = current[1]
                elif current[0] == "fire":
                        default["Fire"] = current[1]
                elif current[0] == "type":
                        default["Type"] = current[1]
                elif current[0] == "pos":
                        default["Location"] = current[1]

        print repr(default)

        return repr(default)

def on_log(client, userdata, level, buf):
        print("log: ",buf)


def loop_forever():
        while True:
                time.sleep(1)
                message = readSerial()
                print ">>" + message
                if message != "":
                        print message
                        message = jsonize(message)
                        print message
                        client.publish("messages/events", message)
                        #client.send_event_async(message, send_confirmation_callback, 1)

client = mqtt.Client(client_id=deviceName, protocol=mqtt.MQTTv311)
client.on_log = on_log
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish
client.loop_forever = loop_forever
client.username_pw_set(username=hubName + "/" + deviceName, password=SharedAccessSignature)
#client.tls_insecure_set(False)
client.tls_set(ca_certs=BaltimoreCyberTrustRootCER, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
client.tls_insecure_set(False)
client.connect(hubName, port=8883)
client.loop_forever()
