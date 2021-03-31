# pyqik_controller
Python Library Pololu Qik Motor Controller

## Table of contest
* [General info](#general-info)
* [Technologies & Libraries](#technologies&libraries)
* [Setup](#setup)
* [Documentation](#documentation)
* [Usage](#usage)
* [License](#license)

## Genral Info
This project is a Python library for Pololu motor controller Qik it was uses pololu_crc7.so library as dependencies

## Technologies & Libraries
* Python 2.7
* pololu_crc7 
https://github.com/ArturK-85/pololu_crc7.git

## Setup

Build from source:
```
python setup.py build
```
And install:
```
python setup.py install
```

## Documentation
All functions uses cyclic redundancy check

* MotorController(port_name, baud_rate)
  * error_check()  Prints error name
  * get_conf()  Prints configuration parameters list
  * set_conf(id, pwm, err, timeout)  Setting parameters : #id 0-255, #pwm 0 or 1, #err 0 or 1, #timeout 0-255
  * motor_coast(motor_number)  Setting motor coast: #motor_number 0 or 1
  * motor_run(motor_number, direction, speed) #direction 'Fwd' or 'Rev', #speed: 0 - 255
  * motor_stop() #stops motor
  
## Usage
Simple exapmple program:
```
import time
import pyqik_controller as pyqik

controller = pyqik.MotorController('/dev/ttyUSB0', 38400)   # 38400kbps is the max speed for this controller

controller.get_conf()                                      # getting configuration of controller              

controller.motor_run(0, 'Fwd', 0x40)                         # run motor forward in half speed
time.sleep(1)
controller.motor_stop()                                      # stop motor

controller.port_close()                                    # port close
```

## License
Distributed under the MIT License. See `LICENSE` for more information.

