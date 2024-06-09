import time
from dronekit import connect, VehicleMode, LocationGlobalRelative


class Copter:
    def _connect(self, address):
        """
        Connect to the Vehicle.
        """
        print("Connecting to vehicle on: %s" % (address,))
        self.vehicle = connect(address, wait_ready=True)

    def __init__(self, address):
        self._connect(address)

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
        Take ff - fly to target altitude.
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

    def fly_to_location(self, latitude, longitude, altitude):
        """
        Fly to the given location.
        """
        print("Going towardspoint for 30 seconds ...")
        point1 = LocationGlobalRelative(latitude, longitude, altitude)
        self.vehicle.simple_goto(point1)

        # sleep so we can see the change in map
        time.sleep(30)

    def return_home(self):
        """
        Return to start point
        """
        print("Returning to Launch")
        self.vehicle.mode = VehicleMode("RTL")
