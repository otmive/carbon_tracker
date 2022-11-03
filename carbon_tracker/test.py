import carbon_tracker
import time

t = carbon_tracker.Tracker()
t.start()
time.sleep(10)
t.stop()

