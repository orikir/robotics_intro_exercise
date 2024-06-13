"""
Small script using dronekit
"""
from ardocopter import *

ADDRESS = 'udpin:0.0.0.0:14550'


def main():
    copter = Copter(ADDRESS, 1)
    copter.arm()
    copter.takeoff(10)
    print(copter.get_location())
    copter.fly_to_location(-35.361354, 149.165218, 20)
    print(copter.get_location())
    copter.return_home()
    copter.disconnect()


if __name__ == '__main__':
    main()
