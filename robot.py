#!/usr/bin/env python3

import typing
import wpilib

import commands2
import ctre
import math

from robotcontainer import RobotContainer
from deadzone import addDeadzone
import ntcore



class MyRobot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run

    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def output(self, text, value):
        pass
      # print(text + ': ' + str(value))
      # self.container.drive.sd.putValue(text, str(value))

    def robotInit(self) -> None:
        
        """
        This function is run when the robot is first started up and should be used for any
        initialization code.
        """

        # Instantiate our RobotContainer.  This will perform all our button bindings, and put our
        # autonomous chooser on the dashboard.
        # wpilib.CameraServer().launch("vision.py:main")
        self.container = RobotContainer()

        self.driverController = self.container.driverController

        self.leftTalon = self.container.leftTalon
        self.leftTalon2 = self.container.leftTalon2
        self.rightTalon = self.container.rightTalon
        self.rightTalon2 = self.container.rightTalon2

        self.drive = self.container.drive



    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomousCommand = self.container.getAutonomousCommand()
        self.output("ato com", self.autonomousCommand)
        #
        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""
        #write auto code here

    def teleopInit(self) -> None:
        # This makes sure that the autonomous stops running when
        # teleop starts running. If you want the autonomous to
        # continue until interrupted by another command, remove
        # this line or comment it out.
        if self.autonomousCommand:
            self.autonomousCommand.cancel()

        # print("Starting teleop...")
        self.humancontrol = True
        self.speed = 0
        self.direction = 0



    def teleopPeriodic(self):

        self.container.drive.gyroOut.set(self.container.drive.gyro.getYaw())

       
        self.leftX = self.driverController.getLeftX()
        self.leftY = -self.driverController.getLeftY()
        self.rightX = self.driverController.getRightX()
        #There are 2 different ways of programming mecanum, this is the from the first
        #note the direction of the motors on the right must be reversed 
        
        
        # self.speed = addDeadzone(self.driverController.getLeftY()) * -1 # TODO: Clean up
        # self.mag = math.sqrt(self.leftX**2 + self.leftY**2)
        # self.angle = math.atan2(self.leftY, self.leftX)

        # self.frontLeftBackRight = math.sin(self.angle+ .25*math.pi) * self.mag
        # self.frontRightBackLeft = math.sin(self.angle - .25 * math.pi) * self.mag
        # #code that sets the motors to their correct speeds
        # self.leftTalon.set(self.frontLeftBackRight)
        # self.leftTalon2.set(self.frontRightBackLeft)
        # self.rightTalon.set(self.frontRightBackLeft)
        # self.rightTalon2.set(self.frontLeftBackRight)

    #this is from the second
    #note the direction of the motors on the right must be reversed

        self.gyroRad = self.drive.gyro.getYaw() * (math.pi/180)
        self.rotX = self.leftX * math.cos(-self.gyroRad) - self.leftY * math.sin(-self.gyroRad)
        self.rotY = self.leftX * math.sin(-self.gyroRad) + self.leftY * math.cos(-self.gyroRad)

        self.denom = max(abs(self.leftY) + abs(self.leftX) + abs(self.rightX), 1);

        self.frontLeftMotor = (self.rotY + self.rotX + self.rightX) #/ self.denom
        self.backLeftMotor = (self.rotY - self.rotX + self.rightX) #/ self.denom
        self.frontRightMotor = (self.rotY - self.rotX - self.rightX)# / self.denom
        self.backRightMotor = (self.rotY + self.rotX - self.rightX) #/ self.denom

        # self.leftTalon.set(self.frontLeftMotor)
        # self.leftTalon2.set(self.backLeftMotor)
        # self.rightTalon.set(self.frontRightMotor)
        # self.rightTalon2.set(self.backRightMotor)


        
        self.drive.driveCartesian(self.leftX, self.leftY, self.rightX) #self.gyroRad
        
        # if self.driverController.getAButton():
        #     self.leftTalon2.set(1)
        
        # elif self.driverController.getBButton():
        #     self.rightTalon2.set(1)

        # elif self.driverController.getYButton():
        #     self.rightTalon.set(1)
        
        # elif self.driverController.getXButton():
        #     self.leftTalon.set(1)




    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)
