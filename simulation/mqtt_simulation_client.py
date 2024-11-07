import random
from typing import List
import json
from paho.mqtt import client as mqtt_client
from helperObjects import Box, Waypoint
from threading import Thread
import signal

broker = 'hosting.alexandernorup.com'
port = 1883
topic = 'eit'
response_topic = 'eit_response'
client_id = f'eit-mir-sim-{random.randint(0, 1000)}'
client_response_id = f'eit-mir-sim-{random.randint(0, 1000)}'

username = 'eit'
password = input("Input mqtt password: ").strip()


def connect_mqtt(client_id):
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
        if 'MessageName' not in data:
            print("Message does not contain MessageName")
            return
        
        if data['MessageName'] == 'PingRequest':
            # Cannot publish with the same client while we "loop_forever", as that would block consuming events, or something along those lines. 
            # Therefore we do a different thread and use a different client. 
            # This also blocks (because of join()) but python is weird like that. This works
            thread = Thread(target=publishPing, args=(data,))
            thread.start()
            thread.join()
        elif data['MessageName'] == 'SimulationStartRequest':
            handle_payload(client, data)

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
        print(f"Sent `{msg}` to topic `{response_topic}`")
    else:
        print(f"Failed to send message to topic {response_topic}")
    client.disconnect()
    return
    


def publishMission(client: mqtt_client, waypoints: List[Waypoint], maxAcceleration: float):
    jsonWaypoints = [serializeWaypoint(waypoint) for waypoint in waypoints]
    data = {
        "MaxAcceleration": maxAcceleration,
        "Waypoints": jsonWaypoints
    }
    msg = json.dumps(data)
    result = client.publish(response_topic, msg)
    status = result[0]
    if status == 0:
        print(f"Sent `{msg}` to topic `{response_topic}`")
    else:
        print(f"Failed to send message to topic {response_topic}")


def handle_payload(client: mqtt_client, payload):
    boxes = [deserializeBox(jsonBox) for jsonBox in payload['Boxes']['$values']]
    #waypoints = [deserializeWaypoint(jsonWaypoint) for jsonWaypoint in payload['Waypoints']['$values']]

    print(boxes)

    
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
        jsonWaypoint['Id'],
        jsonWaypoint['Name'],
        jsonWaypoint['X'],
        jsonWaypoint['Y'],
        jsonWaypoint['Rotation'],
        jsonWaypoint['Speed']
    )


def run():
    client = connect_mqtt(client_id)

    def closing(signum, frame):
        print("Goodbye ):")
        client.disconnect()
        exit(1)
    
    signal.signal(signal.SIGINT, closing)

    subscribe(client)
    client.loop_forever()
        


if __name__ == '__main__':
    run()