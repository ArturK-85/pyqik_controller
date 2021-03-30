# pyqik_controller
Python Library Pololu Qik Motor Controller

## Table of contest
* [General info](#general-info)
* [Technologies & Libraries](#technologies&libraries)
* [Setup](#setup)
* [Usage](#usage)
* [License](#license)

## Genral Info
This project is a Python library for Pololu motor controller Qik it was uses pololu_crc7.so library as dependencies

## Technologies & Libraries
* pololu_crc7 
https://github.com/ArturK-85/pololu_crc7.git

## Setup

## Usage
Simple exapmple program:
```
import time
import pyqik_controller as pyqik

pyqik_init = pyqik.ControllerInit('/dev/ttyUSB0', 38400)   # 38400kbps is the max speed for this controller

pyqik_init.get_conf()                                      # getting configuration of controller

controll = pyqik.MotorController(pyqik_init)               

controll.motor_run(0, 'Fwd', 0x40)                         # run motor forward in half speed
time.sleep(1)
controll.motor_stop()                                      # stop motor

pyqik_init.port_close()                                    # port close
```


## License
Distributed under the MIT License. See `LICENSE` for more information.

