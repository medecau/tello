import time
import tello



drone = Drone()
drone.command()
drone.check()
time.sleep(3)
drone.takeoff()
time.sleep(2)
drone.send("time?")
drone.send("battery?")
drone.send("height?")
drone.send("baro?")
drone.up(50)
time.sleep(2)
drone.forward(50)
time.sleep(2)

drone.back_flip()
drone.front_flip()
time.sleep(2)

drone.backward(50)
time.sleep(2)
drone.down(50)
time.sleep(5)
drone.land()
