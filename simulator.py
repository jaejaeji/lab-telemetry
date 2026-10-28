from datetime import datetime, timezone
import random
import json
import time
import sys
import argparse

ROOM_TEMP_MIN = 20.0
ROOM_TEMP_MAX = 25.0
START_PROB = 0.1
FAILURE_PROB = 0.02
ERROR_CODES = {
    101: "tip pickup failure",
    102: "liquid level not detected",
    201: "gripper collision",
    301: "over temperature",
}



class Device:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = "idle"
        self.run_progress = 0
        self.temperature_c = random.uniform(ROOM_TEMP_MIN, ROOM_TEMP_MAX)
        self.error_code = None
        

    def reading(self):

        return {
            "device_id": self.device_id,
            "status": self.status,
            "run_progress": self.run_progress,
            "temperature_c": round(self.temperature_c, 2),
            "error_code": self.error_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    def advance(self, value):

        new_progress = self.run_progress + value

         # Reject rather than clamp: >100% means something upstream is broken; raises error and leaves progress unchanged
        if not 0 <= new_progress <= 100:
            raise ValueError(f"New progress after input would be: {new_progress}. Value must be between 0 and 100.")

        self.run_progress = new_progress
        self.status = "operating"

    def step(self): # one tick of simulated time
               
        if self.status == "idle" and random.random() < START_PROB:
            self.status = "operating"

        elif self.status == "operating":
            step_size = min(random.randint(2,8), 100 - self.run_progress)
            self.advance(step_size)
            self.temperature_c += random.uniform(-0.1, 0.3)

            if random.random() < FAILURE_PROB:
                self.status = "failed"
                self.error_code = random.choice(list(ERROR_CODES))

        if self.temperature_c >= 80:
            self.status = "failed"
            self.error_code = 301

        if self.status == "operating":
            if self.run_progress >= 100:
                self.status = "complete"



    def run_device(self):
        self.step()
        print(json.dumps(self.reading()))

    def reset(self):
        self.status = "idle"
        self.run_progress = 0
        self.temperature_c = random.uniform(ROOM_TEMP_MIN, ROOM_TEMP_MAX)
        self.error_code = None




def make_devices(n):
    device_list = []

    for i in range(1, n + 1):
        device_list.append(Device(f"LR-{i:02d}"))
    return device_list

def main():

    parser = argparse.ArgumentParser(description="Stream simulated lab device readings as JSON")
    parser.add_argument("--devices", type=int, default=5, help="number of devices")
    parser.add_argument("--interval", type=float, default=2, help="loop interval in seconds")
    parser.add_argument("--seed", type=int, default=42, help="seed number for randomized values")
    args = parser.parse_args()



    random.seed(args.seed)
    devices = make_devices(args.devices)
    try:
        count = 0
        while True:    
            count += 1
            print(f"Step {count}", file=sys.stderr)

            for d in devices:
                d.run_device()

            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("Stopped.", file=sys.stderr)


if __name__ == "__main__":
    main()

