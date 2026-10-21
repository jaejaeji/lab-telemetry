from datetime import datetime, timezone

reading = {      
    "device_id": "LH-01",
    "status": "standby",
    "temperature_c": 37,    # temperature in celcius
    "timestamp": datetime.now(timezone.utc).isoformat(),    # current time in UTC as text so readings from instruments in different time zones sort correctly
}

print(reading)
print(reading["timestamp"])
