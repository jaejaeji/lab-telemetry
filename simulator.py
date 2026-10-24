from datetime import datetime, timezone

class Device:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = "idle"
        self.run_progress = 0
        self.temperature_c = 37
        self.error_code = 0     # No error


    def reading(self):

        return {
            "device_id": self.device_id,
            "status": self.status,
            "run_progress": self.run_progress,
            "temperature_c": self.temperature_c,
            "error_code": self.error_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def advance(self, percent):

        new_progress = self.run_progress + percent

        # Reject rather than clamp: >100% means something upstream is broken; raises error and leaves progress unchanged

        if(new_progress > 100 or new_progress < 0):
            raise ValueError(f"Value must be between 0 and 100. New progress after input: {new_progress}. Device progress unchanged: {self.run_progress}.")

        self.run_progress = new_progress
        self.status = "operating"

d1 = Device("LR-01")
d2 = Device("LR-02")
d3 = Device("LR-03")


# try/except allows bad calls to be rejected without stopping the script
try:
    d1.advance(-30)
except ValueError as err:
    print(f"Rejected: {err}")
print(d1.reading())

try:
    d2.advance(500)
except ValueError as err:
    print(f"Rejected: {err}")
print(d2.reading())


try:
    d3.advance(60)
except ValueError as err:
    print(f"Rejected: {err}")
print(d3.reading())

print(d1.status, d2.status, d3.status)