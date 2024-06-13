"""
Small script using dronekit
"""
from ardocopter import *

ADDRESS = 'udpin:0.0.0.0:14550'
ADDRESS2 = 'udpin:0.0.0.0:14560'


def main():
    follower_copter = Copter(ADDRESS2, False)

    leader_copter = Copter(ADDRESS, True)
    # leader_copter.arm()
    # leader_copter.takeoff(10)
    # leader_copter.fly_to_location(-35.361354, 149.165218, 20)

    navigate_thread = threading.Thread(target=follower_copter.navigate_to_leader_position)
    navigate_thread.daemon = True
    navigate_thread.start()

    navigate_thread = threading.Thread(target=leader_copter.send_position_to_follower())
    navigate_thread.daemon = True
    navigate_thread.start()


if __name__ == '__main__':
    main()
