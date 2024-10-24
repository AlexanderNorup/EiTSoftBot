import random
import time
import os
import shutil
import configPrint
import sdfPrint
import spawner
import json
from paho.mqtt import client as mqtt_client

broker = 'hosting.alexandernorup.com'
port = 1883
topic = 'eit'
username = 'eit'
password = input("Input mqtt password: ").strip()
client_id = f'eit-mir-sim-{random.randint(0, 1000)}'

# Change path below
mainPath = "../../../../catkin_ws/src/mir_robot/mir_gazebo"
#mainPath = "./temp"


def connect_mqtt():
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print("Recieved message")
        data = json.loads(msg.payload.decode())
        handle_payload(data)

    client.subscribe(topic)
    client.on_message = on_message


def handle_payload(payload):
    i = 0
    for box in payload:
        i += 1
        write_box(i, box)
    # Uncomment below to make the script load boxes into simulator. With this still commented, it only creates the files
    load_into_simulation(i)
    return

def write_box(i, box):
    if os.path.isdir(mainPath + "/sdf/box" + str(i)):
        shutil.rmtree(mainPath + "/sdf/box" + str(i))
    os.makedirs(mainPath + "/sdf/box" + str(i)) # add own path
    configPrint.writeConfig(mainPath + "/sdf/box" + str(i) + "/model.config",i)

    w = box['Weight']

    s0_data = box['SizeX']
    s1_data = box['SizeY']
    s2_data = box['SizeZ']
    s = [s0_data,s1_data,s2_data]

    p0_data = box['X']
    p1_data = box['Y']
    p2_data = box['Z']
    p = [p0_data,p1_data,p2_data]

    mu1=0.54 #0.54
    mu2=0.32

    sdfPrint.writeSdf(mainPath + "/sdf/box" + str(i) + "/model.sdf",p,w,s,mu1,mu2)
    return

def load_into_simulation(i):
    if os.path.isfile(mainPath + "/launch/includes/spawn_box.launch.xml"):
        os.remove(mainPath + "/launch/includes/spawn_box.launch.xml")
    
    print('Program will now open simulation')
    spawner.spawnBox(mainPath + "/launch/includes/spawn_box.launch.xml", i)
    os.system("roslaunch mir_gazebo mir_empty_world.launch")
    return


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
        


if __name__ == '__main__':
    run()