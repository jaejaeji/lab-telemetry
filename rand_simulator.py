from datetime import datetime, timezone
import random

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
            print(f"Device temperature_c: {round(self.temperature_c, 2)}")

        if self.status == "operating":
            if self.run_progress >= 100:
                self.status = "complete"


    def check_failed(self):
        if self.status == "failed":
            print(f"ERROR {self.error_code}: {ERROR_CODES.get(self.error_code)}")
            print(f"Current progress: {self.run_progress}")
            return True
        elif self.status == "complete":
            print(f"Run complete. Progress: {self.run_progress}%")
            return True

        return False

    def run_device(self):
        self.step()
        print(self.reading())


    def reset(self):
        self.status = "idle"
        self.run_progress = 0
        self.temperature_c = random.uniform(ROOM_TEMP_MIN, ROOM_TEMP_MAX)
        self.error_code = None


        
random.seed(42)

d1 = Device("LR-01")
d2 = Device("LR-02")

for _ in range (30):
    if d1.check_failed():
        break
    d1.run_device()

for _ in range (30):
    if d2.check_failed():
        break
    d2.run_device()


    
print(d1.status, d2.status)


# 1. Your seeded run gives the same output twice. Name one situation in this project where that will save you time.
# You are able to check if the errors are repeatable. A device fails at step 17, you change one line and see if you still see step 17 fail.

# 2. What does random.random() < 0.02 mean in plain words? Over 1,000 steps, about how many failures do you expect, and would you be surprised by 35?
# It means a randomly generated number under 0.02 would be true. In other words, a 2% chance of error, or 20 failures for 1000 steps.
# A failure at 35 would most likely mean a bug that should be investigated

# 3. How does step() stop advance() from overshooting? If advance() raised during a simulation run, what would that tell you?
# step() sets a max value for step_size so that the self.run_progress doesn't exceed 100 (100 - self.run_progress) so it doesn't overshoot. Advance() raises ValueError when the updated progress is outside of the 1-100 range

# 4. Your failed-run decision: what happens to status and run_progress, and why? How many readings show the failure before the device recovers (if it does)?
# The status stays at failed and run progress stays at the failed position. The user should be able to check the error and the device should not continue to run with an error
# There's one reading that shows failure.

# 5. Back to Day 2's follow-up: now that 101, 102, 201 and 301 mean real faults, is 0 still the right "no error" value, or would None be clearer? One sentence either way.
# error_code = None makes more sense than 0

# 6. Why did the old loop stop after one step?
# The loop stopped after one step because it always returned a boolean at the end of function, instead of returning it when certain conditions were met.

# Time spent: 1hr 7min + 3hr 27min