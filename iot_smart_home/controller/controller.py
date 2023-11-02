from fastapi import FastAPI, HTTPException

app = FastAPI()

# Sample sensor data (simulated sensors)
sensors = {
    "temperature": 25.0,
    "humidity": 50.0,
}

# Sample device status (simulated devices with on/off functionality)
devices = {
    "light": True,
    "fan": False,
}


# Get sensor data
@app.get("/sensors/{sensor_name}")
async def read_sensor(sensor_name: str):
    if sensor_name in sensors:
        return {"sensor": sensor_name, "value": sensors[sensor_name]}
    raise HTTPException(status_code=404, detail="Sensor not found")


# Update sensor data (for demonstration purposes)
@app.put("/sensors/{sensor_name}")
async def update_sensor(sensor_name: str, value: float):
    if sensor_name in sensors:
        sensors[sensor_name] = value
        return {"sensor": sensor_name, "value": value}
    raise HTTPException(status_code=404, detail="Sensor not found")


# List available sensors
@app.get("/sensors/")
async def list_sensors():
    return {"sensors": list(sensors.keys())}


# Get device status
@app.get("/devices/{device_name}")
async def read_device(device_name: str):
    if device_name in devices:
        return {"device": device_name, "status": devices[device_name]}
    raise HTTPException(status_code=404, detail="Device not found")


# Update device status
@app.put("/devices/{device_name}")
async def update_device(device_name: str, status: bool):
    if device_name in devices:
        devices[device_name] = status
        return {"device": device_name, "status": status}
    raise HTTPException(status_code=404, detail="Device not found")
