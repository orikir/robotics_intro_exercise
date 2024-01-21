# Robotics Intro Exercise 

## Purpose

The purpose of this exercise is to assess candidates' abilities in quickly learning robotic frameworks, designing robotic systems, and integrating them into a multi-robot system. Enjoy the challenge!

In this exercise, you will engage with the following topics:

1. Ardupilot basics - understanding ardupilot code, sitl, mission planner, mavlink, etc.
2. mavlink-python communication.
3. Networking and multirobot architecture and design.

## Prerequisites

1. An Ubuntu 18.04-20.04 computer with an online network connection (or necessary installations available, as per the tutorials).
2. Basic knowledge of Linux commands.

## The Exercise in a Sentence

"Write a code that controls a drone and tracks another drone at a given height above it."

## Important Resources

1. Ardupilot Docs - [https://ardupilot.org/copter/index.html](https://ardupilot.org/copter/index.html)
2. SITL - [https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html](https://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html)
3. Mavlink ICD - [http://mavlink.io/en/messages/common.html](http://mavlink.io/en/messages/common.html)
4. Mission Planner Docs - [https://ardupilot.org/planner/](https://ardupilot.org/planner/)
5. And Most Importantly - The Entire Internet! :)

## Exercise Flow

1. Read the following [tutorial](https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux) and this [one](https://ardupilot.org/dev/docs/building-setup-linux.html#building-setup-linux). Install and run a drone (copter) in sitl.
2. Install Mission Planner using this [tutorial](https://ardupilot.org/planner/docs/mission-planner-installation.html). Connect to sitl following this [tutorial](https://ardupilot.org/dev/docs/using-sitl-for-ardupilot-testing.html).
3. Use Mission Planner docs and tutorials to take off the drone in sitl, sending it to different points on the map.
4. Congratulations! You've successfully completed your first drone flight!
5. Now, let's make it more interesting. Write a Python program that connects to the vehicle via mavlink protocol, arms it, takes it off, and sends it to a given known location (lat, lon, alt). There are no limitations to the solution; feel free to use any framework of your liking to achieve the goal.
6. Cool! It's practically autonomous!
7. Now, add another drone to the game. Ensure you can control both drones independently using Mission Planner (one at a time, without each one influencing or interfering with the other). Both should be visible together on Mission Planner.
8. Here comes the fun part. Develop a program that connects to a drone and, using a configuration file, decides if this drone is the follower or the leader.
   - If it is the leader, send the current position of the drone to the other drone.
   - If it is the follower, receive the position of the leader and send the drone to this location.
   
   Design considerations:
   - These programs ideally run on an onboard computer next to the flight controller (simulated using sitl). They run on different computers and need to communicate somehow between them.
   - You may need to read several messages from the flight controller and simultaneously send commands to it. Your program and design should enable that.


Hope you enjoyed :)
