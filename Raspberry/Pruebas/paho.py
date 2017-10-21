from paho.mqtt import client as mqtt                                # be sure to install package paho-mqtt
import ssl
########## You need only modify this section start ##########
# You can generate the SAS with Device Explorer
# Example SharedAccessSignature = "SharedAccessSignature sr=kevinsay.azure-devices.net%2fdevices%2fmygreatdevice&sig=ON2EYJR1hUC84rJSMe%2fCrBdb8lcIr7A%3d&se=15055292"
# SharedAccessSignature = "SharedAccessSignature sr=kevinsayIoT.azure-devices.net%2fdevices%2fpython&sig=ON2EYJR7R7ILlA1ChUC84rJSMWEBe%2fCJrBdb8lcIr7A%3d&se=1505515292"
ConnectionString = "HostName=ValenHub.azure-devices.net;DeviceId=Raspberry01;SharedAccessKey=dop/dAKF//LMLfpIwjLxG1mTnHfofwtVwN2O4nWmfBw="

# download the cer from https://ssl-tools.net/certificates/d4de20d05e66fc53fe1a50882c78db2852cae474.pem
# BaltimoreCyberTrustRootCER = "C:\\Users\\kevinsay\\desktop\\d4de20d05e66fc53fe1a50882c78db2852cae474.cer"


########### You need only modify this section end ###########


# HubName = SharedAccessSignature.split("%2f")[0].split("=")[1]       # extracting the Hub name from the SAS
# devicename = SharedAccessSignature.split("%2f")[2].split("&")[0]    # extracting the device name from the SAS

HubName = ConnectionString.split(';')[0].split('=')[1]
devicename = ConnectionString.split(';')[1].split('=')[1]
signature = ConnectionString.split(';')[2].split('=')[1]

print HubName
print devicename
print signature

def on_connect(client, userdata, flags, rc):
    print ("Connected with result code: " + str(rc))
    client.subscribe("devices/" + devicename + "/messages/devicebound/#")


def on_disconnect(client, userdata, rc):
    print ("Disconnected with result code: " + str(rc))


def on_message(client, userdata, msg):
    print (msg.topic+" "+str(msg.payload))
    # Do this only if you want to send a reply message every time you receive one
    client.publish("devices/" + devicename + "/messages/events/", "{id=1}", qos=1)


def on_publish(client, userdata, mid):
    print ("Sent message")

client = mqtt.Client(client_id=devicename, protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.on_publish = on_publish
#client.username_pw_set(username=HubName + "/" + devicename, password=signature)
client.username_pw_set(username=HubName , password=signature)
#client.username_pw_set(username=HubName + "/" + devicename, password=SharedAccessSignature)
#client.tls_insecure_set(False)
#client.tls_set(ca_certs=BaltimoreCyberTrustRootCER, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1, ciphers=None)
client.connect(HubName, port=8883 )
client.loop_forever()
