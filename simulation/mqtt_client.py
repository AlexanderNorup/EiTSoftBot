import random
import time
import os
import shutil
from typing import List
import configPrint
import sdfPrint
import spawner
import json
from paho.mqtt import client as mqtt_client
from helperObjects import Box, Waypoint

broker = 'hosting.alexandernorup.com'
port = 1883
topic = 'eit'
username = 'eit'
password = input("Input mqtt password: ").strip()
client_id = f'eit-mir-sim-{random.randint(0, 1000)}'


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
        handle_payload(client, data)

    client.subscribe(topic)
    client.on_message = on_message


def publishMission(client: mqtt_client, waypoints: List[Waypoint], maxAcceleration: float):
    jsonWaypoints = [serializeWaypoint(waypoint) for waypoint in waypoints]
    data = {
        "MaxAcceleration": maxAcceleration,
        "Waypoints": jsonWaypoints
    }
    msg = json.dumps(data)
    result = client.publish(topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")


def handle_payload(client: mqtt_client, payload):
    boxes = [deserializeBox(jsonBox) for jsonBox in payload['Boxes']]
    waypoints = [deserializeWaypoint(jsonWaypoint) for jsonWaypoint in payload['Waypoints']]

    # Load these into simulation
    # Get result of simulation (update waypoints and get max acceleration)
    # publishMission(client, waypoints, maxAcceleration)
    return


def serializeWaypoint(waypoint: Waypoint):
    return {
        "UUID": waypoint.uuid,
        "X": waypoint.x,
        "Y": waypoint.y,
        "Speed": waypoint.speed
    }


def deserializeBox(jsonBox) -> Box:
    return Box(
        jsonBox['X'],
        jsonBox['Y'],
        jsonBox['Z'],
        jsonBox['SizeX'],
        jsonBox['SizeY'],
        jsonBox['SizeZ'],
        jsonBox['Weight'],
    )


def deserializeWaypoint(jsonWaypoint) -> Waypoint:
    return Waypoint(
        jsonWaypoint['UUID'],
        jsonWaypoint['X'],
        jsonWaypoint['Y'],
        jsonWaypoint['Speed']
    )


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()
        


if __name__ == '__main__':
    run()