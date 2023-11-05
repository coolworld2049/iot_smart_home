import json
import uuid

from flask import Flask, request, jsonify, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_mqtt import Mqtt
from loguru import logger

from iot_smart_home.crypt import PayloadEncryptor
from iot_smart_home.schemas import Device
from iot_smart_home.settings import settings

app = Flask(__name__)
app.config["SECRET"] = "secret"
app.config[
    "MQTT_CLIENT_ID"
] = f"MQTTv5-{settings.mqtt_broker_host}-{settings.mqtt_broker_port}-{uuid.uuid4()}"
app.config["MQTT_BROKER_URL"] = settings.mqtt_broker_host
app.config["MQTT_BROKER_PORT"] = settings.mqtt_broker_port
app.config["MQTT_USERNAME"] = settings.mqtt_broker_username
app.config["MQTT_PASSWORD"] = settings.mqtt_broker_password
app.config["MQTT_KEEPALIVE"] = 5

mqtt = Mqtt(app, connect_async=True)
bootstrap = Bootstrap(app)
devices: dict[str, Device | None] = {}
encryptor = PayloadEncryptor(settings.shared_aes_key)


def update_devices(message):
    try:
        msg_payload = json.loads(message.payload.decode())
        device = Device(**msg_payload)
        devices[device.name] = device
    except:
        pass


@mqtt.on_connect()
def mqtt_handle_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected successfully")
        mqtt.subscribe(f"{settings.sensor_topic}/#")
    else:
        logger.info("Bad connection. Code:", rc)


@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    message.payload = encryptor.decrypt_payload(message.payload)
    logger.info(
        f"Received message on topic '{message.topic}' payload {message.payload}"
    )
    update_devices(message)


@app.route("/")
def index():
    logger.info(devices)
    return render_template(
        "index.html",
        devices=devices,
        reload_every_ms=settings.pub_frequency * 2 * 1000,
    )


@app.route("/switch_device_state")
def switch_device_state():
    name = request.args.get("name")
    state = request.args.get("state")
    if not devices.get(name):
        return jsonify(dict(message=f"Device {name} not found"))
    payload = encryptor.encrypt_payload(state.encode())
    topic = f"{devices.get(name).topic}/state"
    mqtt.publish(topic, payload=payload)
    return redirect("/")


@app.route("/delete_device")
def delete_device():
    name = request.args.get("name")
    if not devices.get(name):
        return jsonify(dict(message=f"Device {name} not found"))
    try:
        del devices[name]
    except:
        pass
    return redirect("/")


def main():
    app.run(host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
