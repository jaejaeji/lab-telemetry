# Part 0. Warm-up: Tracebacks

# You run a script and get this:

# ```
# Traceback (most recent call last):
#   File "C:\Users\wogur\code\lab-telemetry\reading.py", line 12, in <module>
#     print(format_reading(reading))
#   File "C:\Users\wogur\code\lab-telemetry\reading.py", line 8, in format_reading
#     return f"{r['device_id']}: {r['temprature_c']} C"
# KeyError: 'temprature_c'
# ```

# 1. Which line do you read first, and what does it tell you?
# KeyError: `temperature_c`, temperature_c isn't a valid key

# 2. Which line of *your* code would you open to fix it, and why that one and not line 12?
# I would change line 8 to match the key from the dict. line 12 just points to the format_reading dict and changing it won't fix the KeyError


# Part 1. Concept: Why a class?

# Week 1 needs N devices, each with its own status, progress and temperature that change over time.
# A **Class** bundles a device's data (attributes) with code allowed to read and change it (methods).
# Same idea as validated instrument method in lab.

# **Class**: blueprint (like instrument model number)
# **Instance / object**: one actual thing built from it (like serial-numbered balance)
# **`__init__`**: runs automatically once
# **`self`**: *this* Python passes it in
# **Attribute**: a variable that belongs to an instance
# **Method**: function defined inside class. First parameter is `self`


# Part 2. Challege: `simulator.py` with a `Device` class

from datetime import datetime, timezone

class Device:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = "idle"
        # self.run_progress = 0
        run_progress = 0
        self.temperature_c = 37
        self.error_code = 0     # No error


    def reading(self):

        if(self.run_progress > 100 or self.run_progress < 0):
            raise ValueError(f"Value must be between 0 and 100. Input: {self.run_progress}. Device status unchanged. Current status: {self.status}")

        return {
            "device_id": self.device_id,
            "status": self.status,
            "run_progress": self.run_progress,
            "temperature_c": self.temperature_c,
            "error_code": self.error_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def advance(self, percent):

        # self.run_progress = percent
        # self.run_progress = max(0, min(100, self.run_progress))   # Conflicts with ValueError line 
        # min(100, x) - can't be more than 100 (values over 100 stay at 100)
        # max(0, x) - can't be less than 0 (values less than 0 stay at 0)

        if(percent > 100 or percent < 0):
            raise ValueError(f"Value must be between 0 and 100. Input: {percent}. Device status unchanged. Current status: {self.status}")
        
        self.run_progress = percent
        self.status = "operating"

d1 = Device("LR-01")
# d1.run_progress = 250
d2 = Device("LR-02")

print(d1.reading())

d1.advance(-30)
d2.advance(500)


print(d1.reading())
print(d2.reading())
print(d1.status, d2.status)

# When someone calls `advance(500)`, **Reject**: raise an error and leave progress unchanged
# This is so the user is aware of that the progress range is 0-100
# a run reporting something like 130% means something upstream is broken in many cases and raises concerns

# If `__init__` accepts a starting `run_progress` argument, someone can write `Device("LH-01", run_progress=250)`. Either don't accept it as an argument (always start at 0), or apply the same rule there. If you apply the rule in two places, how could you avoid writing it twice?
# Idk

# What would break if you wrote run_progress = 0 instead of self.run_progress = 0 in __init__, and when would you find out?
# the reading function will break since it cannot read self.run_progress

# Why does reading() return the dict instead of printing it?
# It should return the dict instead of printing it so it can be coded to print or use a key value from within the dict

# Why did you choose clamp vs. reject?
# I just reject so the user is aware that the input value is outside progress range

# What value did you pick for "no error" in error_code, and why?
# I chose 0 for no error to mean it has zero errors

# Time: 1hr 55min