# 2DOF Vectoring (Antenna Tracker)

Reads the real-time GPS position of an autonomous vehicle and calculates pan and tilt angles for a 2-DOF antenna tracker placed at specified coordinates.

This code was developed so that a unidirectional antenna placed on the antenna tracker would constantly point towards a moving UAV. However, no content of this repository actually pertains to an antenna -- this pan and tilt positioning setup can be used for any 2DOF vectoring application, such as filming, BVLOS indication, and so on. 

The program was tested in the Eastern Hemisphere (east of the UK) and the Northern Hemisphere (north of the Equator). Due to sign conventions, however, the program should work in all 4 possible combinations of east/west and north/south hemispheres of the globe. 

## Setup

* Tested on a UAV running ArduPlane 3.8

* MAVLink Communication protocol (`pymavlink`)

* The coordinates are pushed either through a COM port or a router IP

* Another subsystem consists of a WiFi/USB capable board and an IMU in order to convert these pan and tilt angles into PWM signals for 2 servos 

## Theory

The program computes a pan and tilt (i.e. azimuth and elevation) based on two parameters:

- **The home position**, which is the GPS position and altitude above mean sea level of the antenna tracker.

- **The UAV position**, which this program reads (at 5Hz) from the MAVLink messages between the Ground Control Station and the UAV. 

The pan and tilt angles are derived using simple trigonometry involving distances of a right angle triangled subtended by the two positions. However, since the globe isn't cartesian, the distance between 2 points coordinates (latitude and longitude) is calculated using the [Haversine formula](https://en.wikipedia.org/wiki/Haversine_formula).

$$
d = 2R \cdot \text{atan2} \left( \dfrac{\sqrt \alpha}{\sqrt{1 - \alpha}} \right)
$$

Where $R$ is the Radius of the Earth and $\alpha$ is given by:

$$
\alpha = \sin ^2 (\Delta x/2) + (\cos(x_1) \cdot \cos(x_2)) + \sin^2(\Delta y/2)
$$

Where $(x_1, y_1)$ and $(x_2, y_2)$ are the two GPS coordinates and $\Delta x = x_1 - x_2$ and $\Delta y = y_1 - y_2$. These numbers are converted into radians for the math to be correct!

## References

Van Brummelen, Glen. Heavenly Mathematics: The Forgotten Art of Spherical Trigonometry. United Kingdom: Princeton University Press, 2013.
