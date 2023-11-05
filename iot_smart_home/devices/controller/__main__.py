import json

from flask import Flask, request, jsonify, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_mqtt import Mqtt
from loguru import logger

from iot_smart_home.schemas import Device
from iot_smart_home.settings import settings

app = Flask(__name__)
app.config["SECRET"] = "secret"
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["MQTT_BROKER_URL"] = settings.mqtt_broker_host
app.config["MQTT_BROKER_PORT"] = settings.mqtt_broker_port
app.config["MQTT_USERNAME"] = ""
app.config["MQTT_PASSWORD"] = ""
app.config["MQTT_KEEPALIVE"] = 5
app.config["MQTT_TLS_ENABLED"] = False

mqtt_client = Mqtt(app)
bootstrap = Bootstrap(app)
devices: dict[str, Device | None] = {}


def update_devices(message):
    msg_payload = json.loads(message.payload.decode())
    payload = {k: Device(**v) for k, v in msg_payload.items()}
    devices.update(payload)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected successfully")
        mqtt_client.subscribe(f"devices")
    else:
        logger.info("Bad connection. Code:", rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    logger.info(
        f"Received message on topic: {message.topic} with payload: {message.payload.decode()}"
    )
    update_devices(message)


@app.route("/publish", methods=["POST"])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data["topic"], request_data["msg"])
    return jsonify({"code": publish_result[0]})


@app.route("/")
def index():
    return render_template(
        "index.html", devices=devices, reload_every_ms=settings.pub_frequency * 1000
    )


@app.route("/switch_state")
def switch_state():
    name = request.args.get("name")
    state = request.args.get("state")
    if not devices.get(name):
        return jsonify(dict(message=f"Device {name} not found"))
    mqtt_client.publish(f"{devices.get(name).topic}/state", payload=state.encode())
    return redirect("/")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
