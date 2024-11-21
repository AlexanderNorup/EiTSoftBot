import random
import time
import os
from typing import List
import json
from paho.mqtt import client as mqtt_client
from helperObjects import Box, Mission, Waypoint
from threading import Thread
import signal

broker = 'hosting.alexandernorup.com'
port = 1883
topic = 'eit'
response_topic = 'eit_response'
client_id = f'eit-mir-sim-{random.randint(0, 1000)}'
client_response_id = f'eit-mir-sim-{random.randint(0, 1000)}'

username = 'eit'
password = input('Input mqtt password: ').strip()


def connect_mqtt(client_id):
    def on_connect(client, userdata, flags, rc, properties):
        if rc == 0:
            print('Connected to MQTT Broker!')
        else:
            print('Failed to connect, return code %d\n', rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        data = json.loads(msg.payload.decode())
        if 'MessageName' not in data:
            print(f'Received a message without MessageName: {data}')
            return
        
        if data['MessageName'] == 'PingRequest':
            # Cannot publish with the same client while we 'loop_forever', as that would block consuming events, or something along those lines. 
            # Therefore we do a different thread and use a different client. 
            # This also blocks (because of join()) but python is weird like that. This works
            print('Received ping.')
            thread = Thread(target=publishPing, args=(data,))
            thread.start()
            #thread.join()
        elif data['MessageName'] == 'SimulationStartRequest':
            print('Received simulation start request.')
            thread = Thread(target=handle_payload, args=(client,data))
            thread.start()
            #thread.join()
            #handle_payload(client, data)

    client.subscribe(topic)
    client.on_message = on_message


def publishPing(data):
    client = connect_mqtt(client_response_id)
    data = {
        '$type':'EiTSoftBot.Dto.Responses.PingResponse, EiTSoftBot.Dto',
        'MessageName': 'PingResponse',
        'PingId': data['PingId'],
        'Source': 'Simulation'
    }
    msg = json.dumps(data)
    result = client.publish(response_topic, msg)
    status = result[0]
    if status == 0:
        print(f'Responded to ping on topic `{response_topic}`')
    else:
        print(f'Failed to respond to ping on topic {response_topic}')
    client.disconnect()
    return
    


def publishMission(client: mqtt_client, mission: Mission, maxAcceleration: float):
    jsonMission = serializeMission(mission)
    data = {
        '$type': 'EiTSoftBot.Dto.Responses.SimulationEndResponse, EiTSoftBot.Dto',
        'MessageName': 'SimulationEndResponse',
        'Mission': jsonMission,
        'MaxAcceleration': maxAcceleration
        
    }
    msg = json.dumps(data)
    result = client.publish(response_topic, msg)
    status = result[0]
    if status == 0:
        print(f'Published {msg[0:20]}... to {response_topic}')
    else:
        print(f'Failed to publish message to {response_topic}')


def handle_payload(client: mqtt_client, payload):
    try:
        boxes = [deserializeBox(jsonBox) for jsonBox in payload['Boxes']]
        mission = deserializeMission(payload['Mission'])
    except:
        print('Unable to unpack JSON')
        return

    print(f'Received:\n{boxes}\n\n{mission}')


    
    # Load these into simulation
    # Get result of simulation (update waypoints and get max acceleration)
    maxAcceleration = int(random.random() * 60 + 40)
    mission = dummy_scramble(mission)

    time.sleep(5)

    publishMission(client, mission, maxAcceleration)
    return


def dummy_scramble(mission: Mission) -> Mission:
    for waypoint in mission.waypoints:
        waypoint.speed = random.random() * 0.9 + 0.1
    return mission


def deserializeMission(jsonMission):
    waypoints = [deserializeWaypoint(jsonWaypoint) for jsonWaypoint in jsonMission['Waypoints']]
    return Mission(
        id=jsonMission['Id'],
        name=jsonMission['Name'],
        waypoints=waypoints
    )


def serializeMission(mission: Mission):
    jsonWaypoints = [serializeWaypoint(waypoint) for waypoint in mission.waypoints]

    return {
        '$type': 'EiTSoftBot.Dto.Entities.Mission, EiTSoftBot.Dto',
        'Id': mission.id,
        'Name': mission.name,
        'Waypoints': jsonWaypoints
    }


def deserializeWaypoint(jsonWaypoint) -> Waypoint:
    return Waypoint(
        id=jsonWaypoint['Id'],
        name=jsonWaypoint['Name'],
        x=jsonWaypoint['X'],
        y=jsonWaypoint['Y'],
        rotation=jsonWaypoint['Rotation'],
        speed=jsonWaypoint['Speed']
    )


def serializeWaypoint(waypoint: Waypoint):
    return {
        '$type': 'EiTSoftBot.Dto.Entities.Waypoint, EiTSoftBot.Dto',
        'Id': waypoint.id,
        'Name': waypoint.name,
        'X': waypoint.x,
        'Y': waypoint.y,
        'Rotation': waypoint.rotation,
        'Speed': waypoint.speed,
    }


def deserializeBox(jsonBox) -> Box:
    return Box(
        x=jsonBox['X'],
        y=jsonBox['Y'],
        z=jsonBox['Z'],
        sizeX=jsonBox['SizeX'],
        sizeY=jsonBox['SizeY'],
        sizeZ=jsonBox['SizeZ'],
        weight=jsonBox['Weight'],
    )


def run():
    client = connect_mqtt(client_id)

    def closing(signum, frame):
        print('Goodbye ):')
        client.disconnect()
        os._exit(0)
    
    signal.signal(signal.SIGINT, closing)

    subscribe(client)
    client.loop_forever()
        


if __name__ == '__main__':
    run()