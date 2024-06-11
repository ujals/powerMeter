import paho.mqtt.client as mqtt
import json
import time
import random

# Define the MQTT server settings
MQTT_BROKER = "206.189.141.214"  # You can use any public MQTT broker or your own
MQTT_PORT = 1883
MQTT_TOPIC = "/Device"

# Define the on_connect callback
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker")
    else:
        print("Connection failed with code", rc)

# Define the on_publish callback
def on_publish(client, userdata, mid):
    print(f"Message {mid} published.")

def publish_device_data(client, device_id):
    # Create a JSON message for the device
    message = {
        "deviceName": f"energy-meter-{device_id}",
        "deviceType":"Single-Phase",
        "Voltage": round(random.uniform(210, 230),2),  # Simulate varying voltage
        "Current": round(random.uniform(10, 30),2),   # Simulate varying current
        "Energy": round(random.uniform(0.1, 0.5),2)   # Simulate varying energy
    }

    # Convert the dictionary to a JSON string
    json_message = json.dumps(message)

    # Publish the JSON message
    result = client.publish(MQTT_TOPIC, json_message)
    
    # Check if the publish was successful
    if result.rc == mqtt.MQTT_ERR_SUCCESS:
        print(f"Published: '{json_message}' to topic '{MQTT_TOPIC}'")
    else:
        print(f"Failed to publish message: {result.rc}")

def main():
    # Create an instance of the client
    client = mqtt.Client()

    # Assign the on_connect and on_publish callback functions
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to the broker
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Start the loop
    client.loop_start()

    try:
        while True:
            for device_id in range(1, 16):  # Loop through 15 devices
                publish_device_data(client, device_id)
            # Wait for 5 minutes before sending the next set of messages
            time.sleep(5*60)
    except KeyboardInterrupt:
        print("Stopped by user")

    # Stop the loop and disconnect
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
