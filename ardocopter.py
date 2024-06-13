import threading
import time
import socket

from dronekit import connect, VehicleMode, LocationGlobalRelative


def is_leader(config_file_path):
    """
    Read configuration file to determine leader or follower mode
    """
    with open(config_file_path, "r") as file:
        mode = file.readline().strip()

    # Assuming configuration file contains a single line: "leader" or "follower"
    if mode == "leader":
        return True
    elif mode == "follower":
        return False
    else:
        return None


class Copter:
    def _connect(self, address):
        """
        Connect to the Vehicle.
        """
        print("Connecting to vehicle on: ", address)
        self.vehicle = connect(address, wait_ready=True)

    def __init__(self, address, is_leader):
        self._connect(address)

        # self.is_leader = is_leader("config.txt")
        self.is_leader = is_leader
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.follower_address = ('127.0.0.1', 12345)  # Follower's address

        if self.is_leader:
            pass

        elif not self.is_leader:
            print("Start binding...")
            self.socket.bind(self.follower_address)  # Bind for receiving

    def print_info(self):
        """
        Get some vehicle attributes (state)
        """
        print("Get some vehicle attribute values:")
        print(" GPS: ", self.vehicle.gps_0)
        print(" Battery: ", self.vehicle.battery)
        print(" Last Heartbeat: ", self.vehicle.last_heartbeat)
        print(" Is Armable?: ", self.vehicle.is_armable)
        print(" System status: ", self.vehicle.system_status.state)
        print(" Mode: ", self.vehicle.mode.name)

    def disconnect(self):
        """
        Close vehicle object
        """
        self.vehicle.close()

    def arm(self):
        """
        Arms vehicle.
        """
        print("Basic pre-arm checks")
        # Don't try to arm until autopilot is ready
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        # Copter should arm in GUIDED mode
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        # Confirm vehicle armed
        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

    def takeoff(self, target_altitude):
        """
        Take off - fly to target altitude.
        """
        print("Taking off!")
        self.vehicle.simple_takeoff(target_altitude)  # Take off to target altitude

        # Wait until the vehicle reaches a safe height before processing the goto
        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            # Break and return from function just below target altitude.
            if self.vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def fly_to_location(self, latitude, longitude, altitude, delay=30):
        """
        Fly to the given location.
        """
        print(f"Going to location: {latitude} {longitude} {altitude} for {delay} seconds")
        point = LocationGlobalRelative(latitude, longitude, altitude)
        self.vehicle.simple_goto(point)

        # sleep so we can see the change in map
        time.sleep(delay)

    def get_location(self):
        """
        Get current location
        :return: latitude longitude and altitude
        """
        global_frame = self.vehicle.location.global_relative_frame
        return global_frame.lat, global_frame.lon, global_frame.alt

    def send_position_to_follower(self):
        while True:
            # Get current position of the leader drone
            lat, lon, alt = self.get_location()

            # Send position to follower
            message = f"Position: {lat}, {lon}, {alt}"
            self.socket.sendto(message.encode(), self.follower_address)
            print("message was sent: " + message)

            # Sleep for some time before sending the next position
            time.sleep(1)

    def navigate_to_leader_position(self):
        # self.arm()
        # self.takeoff(5)

        while True:
        #     if self.vehicle.mode.name != "GUIDED":
        #         print("User has changed flight modes - aborting follow-me")
        #         break

            data, _ = self.socket.recvfrom(1024)  # Adjust buffer size as needed
            leader_position = data.decode().split(":")[1].strip()  # Extract leader position from message
            print("message was received" + leader_position)
            # Convert leader position to our format
            leader_lat, leader_lon, leader_alt = map(float, leader_position.split(","))

            self.fly_to_location(leader_lat, leader_lon, leader_alt, 2)

    def return_home(self):
        """
        Return to start point
        """
        print("Returning to Launch")
        self.vehicle.mode = VehicleMode("RTL")
