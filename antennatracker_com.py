'''This is a program to acquire data from Mavlink for pan and tilt mechanism
for antenna tracker. The contents of this script can be mainly divided into
    (1) Acquiring GPS lat and long of the plane
    (2) Calculating required distances between coordinates
    (3) Calculating pan and tilt angle'''

import os
from pymavlink import mavutil
from math import *
import serial

home = [12.94891, 77.4399]
terrain_alt = 836.4099

def coord_distance(c1, c2):
    R = 6370000.0
    delta_lat = c1[0] - c2[0]
    delta_lon = c1[1] - c2[1]
    alpha = (sin(radians(delta_lat/2)))**2 + (cos(radians(c1[0])) * cos(radians(c2[0])) * (sin(radians(delta_lon/2)))**2)
    beta = 2 * atan2(sqrt(alpha), sqrt(1 - alpha))
    d = R * beta
    return d

def quadrant(plane_q, home_q):
    if (plane_q[0] > home_q[0]) and (plane_q[1] > home_q[1]):
        return 1
    elif (plane_q[0] < home_q[0]) and (plane_q[1] > home_q[1]):
        return 2
    elif (plane_q[0] < home_q[0]) and (plane_q[1] < home_q[1]):
        return 3
    elif (plane_q[0] > home_q[0]) and (plane_q[1] < home_q[1]):
        return 4
    else:
        return -1

def pan(coord):
    hypotenuse = coord_distance(coord, home)
    vertical_coord = [coord[0], home[1]]
    adjacent = coord_distance(home, vertical_coord)
    theta = acos(adjacent/hypotenuse)
    theta_d = degrees(theta)
    ref = quadrant(coord, home)
    if ref == 1:
        return theta_d
    elif ref == 2:
        return 180 - theta_d
    elif ref==3:
        return 180 + theta_d
    elif ref == 4:
        return 360 - theta_d
    else:
        return -1

def tilt(coord, a):
    dist = coord_distance(home, coord)
    phi = atan(a/dist)
    phi_d = degrees(phi)
    return phi_d

connection_str = "127.0.0.1:14550"

mav = mavutil.mavlink_connection("tcp: " + connection_str)
mav.wait_heartbeat()
ser = serial.Serial("COM13")
count = 0
print ser.name
while True:
    c = mav.recv_match(type=["GPS_RAW_INT"], blocking=True, timeout=1)
    head = mav.recv_match(type=["VFR_HUD"], blocking=True, timeout=1)
    if c and head:
        coordinates = [float(c.lat)/(10**7), float(c.lon)/(10**7)]
        print coordinates
        alt = head.alt - terrain_alt
        print c.lat, c.lon, alt
        print pan(coordinates), tilt(coordinates, alt)
        foo = str(pan(coordinates)) + " " + str(tilt(coordinates, alt))
        ser.write(foo)
        count = count + 1
        print count
        print "\n"
ser.close()

os._exit(0)
