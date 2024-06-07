"""
Small script using dronekit
"""
from ardocopter import *


def main():
    copter = Copter(ADRESS)
    copter.arm()
    copter.takeoff(10)
    copter.fly_to_location(-35.361354, 149.165218, 20)
    copter.return_home()
    copter.disconnect()


if __name__ == '__main__':
    main()
