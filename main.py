"""
Small script using dronekit
"""
from ardocopter import *

ADRESS = 'udpin:0.0.0.0:14550'

def main():
    copter = Copter(ADRESS)
    copter.arm()
    copter.takeoff(10)
    copter.fly_to_location(-35.361354, 149.165218, 20)
    copter.return_home()
    copter.disconnect()


if __name__ == '__main__':
    main()
