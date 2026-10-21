# from datetime import datetime, timezone   # import the tools for working with time

# sample = {                                 # {} creates a dict
#     "sample_id": "S-0042",                 # key "sample_id" maps to a string value
#     "solvent": "acetonitrile",
#     "volume_ml": 2.5,                      # a float; the unit lives in the key name
#     "is_filtered": True,                   # a boolean
#     "prepared_at": datetime.now(timezone.utc).isoformat(),  # current time in UTC, as text
# }
# print(sample)                              # print the whole dict
# print(sample["volume_ml"])                 # look up a single value by its key

# Challenge: Build one fake reading as a dict with device ID, status, temperature and timestamp, and print it.
# Choose your own key names and units, because you’ll have to defend them. 
# Then run it from the terminal with python reading.py.


from datetime import datetime, timezone     # import tools for working with time

reading = {      # {} creates a dict, variable name is reading because this dict is a reading from the device
    "device_id": "LH-01",     # key: value, value reflects real instrument IDs
    "status": "standby",
    "temperature_c": 37,    # key changed from "temperature", so there's one standard unit and no confusion
    # "temp_unit": "C",       # C is used in place of °C because ° is a non-ASCII character which can come out garbled in reports
    "timestamp": datetime.now(timezone.utc).isoformat(),    # current time in UTC as text so readings from instruments in different time zones sort correctly
}

print(reading)
print(reading["timestamp"])
print(reading["timestamp_c"])
