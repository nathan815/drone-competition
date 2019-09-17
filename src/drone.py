from time import sleep
import tellopy

def handler(event, sender, data, **args):
    drone = sender
    if event is drone.EVENT_FLIGHT_DATA:
        print("Drone Data: ", data)

def test():
    drone = tellopy.Tello()
    drone.subscribe(drone.EVENT_FLIGHT_DATA, handler)
    drone.connect()
    drone.wait_for_connection(60.0)

    height = 5
    run = True


    try:
        for i in range(0, 3):
            print("Run  ", i)
            print("takeoff...")
            drone.takeoff()

            sleep(5)
            print("up...")
            drone.up(height)

            sleep(2)
            print("down...")
            drone.down(height)

            sleep(1)
            print("land...")
            drone.land()

            sleep(5)
    except Exception as ex:
        print("Exception: ", ex)

    drone.quit()
if __name__ == '__main__':
    test()
