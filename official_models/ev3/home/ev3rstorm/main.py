#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Ev3rstorm Program
----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://www.lego.com/en-us/themes/mindstorms/buildarobot
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import ImageFile
from pybricks.parameters import Direction, Port, Stop

from drive_util import IRBeaconDriverMixin


class Ev3rstorm(EV3Brick, IRBeaconDriverMixin):
    WHEEL_DIAMETER = 26   # milimeters
    AXLE_TRACK = 102      # milimeters

    def __init__(
            self,
            left_motor_port: Port = Port.B,
            right_motor_port: Port = Port.C,
            shooting_motor_port: Port = Port.A,
            touch_sensor_port: Port = Port.S1,
            color_sensor_port: Port = Port.S3,
            ir_sensor_port: Port = Port.S4,
            ir_beacon_channel: int = 1):
        super().__init__()

        IRBeaconDriverMixin.__init__(
            self,
            left_motor_port=left_motor_port,
            right_motor_port=right_motor_port,
            ir_sensor_port=ir_sensor_port,
            ir_beacon_channel=ir_beacon_channel,
            wheel_diameter=self.WHEEL_DIAMETER,
            axle_track=self.AXLE_TRACK)
        
        self.shooting_motor = Motor(port=shooting_motor_port,
                                    positive_direction=Direction.CLOCKWISE)

        self.touch_sensor = TouchSensor(touch_sensor_port)
        self.color_sensor = ColorSensor(color_sensor_port)

    def shoot_if_touched(self):
        N_ROTATIONS_PER_SHOT = 3
        ROTATIONAL_DEGREES_PER_SHOT = N_ROTATIONS_PER_SHOT * 360

        if self.touch_sensor.pressed():
            if self.color_sensor.ambient() < 15:
                self.speaker.play_file(file='sounds/Up.wav')

                self.shooting_motor.run_angle(
                    speed=2 * ROTATIONAL_DEGREES_PER_SHOT,   # shoot quickly in half a second
                    rotation_angle=ROTATIONAL_DEGREES_PER_SHOT,
                    then=Stop.HOLD,
                    wait=True)

            else:
                self.speaker.play_file(file='sounds/Down.wav')

                self.shooting_motor.run_angle(
                    speed=2 * ROTATIONAL_DEGREES_PER_SHOT,   # shoot quickly in half a second
                    rotation_angle=-ROTATIONAL_DEGREES_PER_SHOT,
                    then=Stop.HOLD,
                    wait=True)


    def main(self):
        while True:
            self.drive_by_ir_beacon()
            self.shoot_if_touched()


if __name__ == '__main__':
    EV3RSTORM = Ev3rstorm()
    EV3RSTORM.main()
