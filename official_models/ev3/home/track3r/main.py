#!/usr/bin/env pybricks-micropython

"""
Example LEGO® MINDSTORMS® EV3 Track3r Program
----------------------------------------------

This program requires LEGO® EV3 MicroPython v2.0.
Download: https://education.lego.com/en-us/support/mindstorms-ev3/python-for-ev3

Building instructions can be found at:
https://www.lego.com/en-us/themes/mindstorms/buildarobot
"""

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, InfraredSensor
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.robotics import DriveBase
from pybricks.parameters import Button, Direction, Port, Stop


class RemoteControlledTank:
    """
    This reusable mixin provides the capability of driving a robot with a Driving Base by the IR beacon
    """
    def __init__(
            self,
            wheel_diameter: float, axle_track: float,   # both in milimeters
            left_motor_port: Port = Port.B, right_motor_port: Port = Port.C,
            ir_sensor_port: Port = Port.S4, ir_beacon_channel: int = 1):
        self.driver = DriveBase(left_motor=Motor(port=left_motor_port,
                                                 positive_direction=Direction.CLOCKWISE),
                                right_motor=Motor(port=right_motor_port,
                                                  positive_direction=Direction.CLOCKWISE),
                                wheel_diameter=wheel_diameter,
                                axle_track=axle_track)

        self.ir_sensor = InfraredSensor(port=ir_sensor_port)
        self.ir_beacon_channel = ir_beacon_channel
    
    
    def drive_by_ir_beacon(
            self,
            speed: float = 1000,     # mm/s
            turn_rate: float = 90   # rotational speed deg/s
        ):
        ir_beacon_button_pressed = set(self.ir_sensor.buttons(channel=self.ir_beacon_channel))

        # forward
        if ir_beacon_button_pressed == {Button.LEFT_UP, Button.RIGHT_UP}:
            self.driver.drive(
                speed=speed,
                turn_rate=0)

        # backward
        elif ir_beacon_button_pressed == {Button.LEFT_DOWN, Button.RIGHT_DOWN}:
            self.driver.drive(
                speed=-speed,
                turn_rate=0)

        # turn left on the spot
        elif ir_beacon_button_pressed == {Button.LEFT_UP, Button.RIGHT_DOWN}:
            self.driver.drive(
                speed=0,
                turn_rate=-turn_rate)

        # turn right on the spot
        elif ir_beacon_button_pressed == {Button.RIGHT_UP, Button.LEFT_DOWN}:
            self.driver.drive(
                speed=0,
                turn_rate=turn_rate)

        # turn left forward
        elif ir_beacon_button_pressed == {Button.LEFT_UP}:
            self.driver.drive(
                speed=speed,
                turn_rate=-turn_rate)

        # turn right forward
        elif ir_beacon_button_pressed == {Button.RIGHT_UP}:
            self.driver.drive(
                speed=speed,
                turn_rate=turn_rate)

        # turn left backward
        elif ir_beacon_button_pressed == {Button.LEFT_DOWN}:
            self.driver.drive(
                speed=-speed,
                turn_rate=turn_rate)

        # turn right backward
        elif ir_beacon_button_pressed == {Button.RIGHT_DOWN}:
            self.driver.drive(
                speed=-speed,
                turn_rate=-turn_rate)

        # otherwise stop
        else:
            self.driver.stop()


class Track3r(RemoteControlledTank, EV3Brick):
    WHEEL_DIAMETER = 26   # milimeters
    AXLE_TRACK = 140      # milimeters


    def __init__(
            self,
            left_track_motor_port: Port = Port.B, right_track_motor_port: Port = Port.C,
            medium_motor_port: Port = Port.A,
            ir_sensor_port: Port = Port.S4, ir_beacon_channel: int = 1):
        super().__init__(
            wheel_diameter=self.WHEEL_DIAMETER, axle_track=self.AXLE_TRACK,
            left_motor_port=left_track_motor_port, right_motor_port=right_track_motor_port,
            ir_sensor_port=ir_sensor_port, ir_beacon_channel=ir_beacon_channel)

        self.medium_motor = Motor(port=medium_motor_port,
                                  positive_direction=Direction.CLOCKWISE)

 
    def main(self):
        """
        Track3r's main program performing various capabilities
        """
        while True:
            self.drive_by_ir_beacon(speed=1000)


class Track3rWithBlastingBazooka(Track3r):
    """
    Track3r blasts his bazooka when the Beacon button is pressed
    (inspiration from LEGO Mindstorms EV3 Home Edition: Track3r: Tutorial #2)
    """
    def blast_bazooka_by_ir_beacon(
            self, 
            speed: float = 1000   # degrees per second
        ):
        if Button.BEACON in self.ir_sensor.buttons(channel=self.ir_beacon_channel):
            self.medium_motor.run_angle(
                speed=speed,
                rotation_angle=3 * 360,   # about 3 rotations for 1 shot
                then=Stop.HOLD,
                wait=True) 

            self.speaker.play_file(file=SoundFile.LAUGHING_1)
               
            while Button.BEACON in self.ir_sensor.buttons(channel=self.ir_beacon_channel):
                pass

        else:
            self.medium_motor.stop()


    def main(self):
        self.screen.load_image(ImageFile.PINCHED_MIDDLE)
            
        while True:
            self.drive_by_ir_beacon()
            self.blast_bazooka_by_ir_beacon()


if __name__ == '__main__':
    TRACK3R = Track3rWithBlastingBazooka()
    TRACK3R.main()
