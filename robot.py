#!/usr/bin/env python3

import typing
import wpilib
import commands2
import ctre


from robotcontainer import RobotContainer
from deadzone import addDeadzone

class MyRobot(commands2.TimedCommandRobot):
    """
    Our default robot class, pass it to wpilib.run

    Command v2 robots are encouraged to inherit from TimedCommandRobot, which
    has an implementation of robotPeriodic which runs the scheduler for you
    """

    autonomousCommand: typing.Optional[commands2.Command] = None

    def output(self, text, value):
      # print(text + ': ' + str(value))
      self.container.drive.sd.putValue(text, str(value))

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
        self.operatorController = self.container.operatorController

        self.leftTalon = self.container.leftTalon
        self.leftVictor = self.container.leftVictor
        self.rightTalon = self.container.rightTalon
        self.rightVictor = self.container.rightVictor

        self.liftArm = self.container.liftArm
        self.rotateArm = self.container.rotateArm

        self.rotateEncoder = self.container.rotateEncoder
        self.liftEncoder = self.container.liftEncoder

        self.liftArmUpLimitSwitch = self.container.liftArmUpLimitSwitch
        self.liftArmDownLimitSwitch = self.container.liftArmDownLimitSwitch
        self.rotateArmBackLimitSwitch = self.container.rotateArmBackLimitSwitch
        self.rotateArmRobotLimitSwitch = self.container.rotateArmRobotLimitSwitch

        self.intake = self.container.intake
        self.outtake = self.container.outtake
        self.snowveyor = self.container.snowveyor

        self.drive = self.container.drive



    def disabledInit(self) -> None:
        """This function is called once each time the robot enters Disabled mode."""

    def disabledPeriodic(self) -> None:
        """This function is called periodically when disabled"""

    def autonomousInit(self) -> None:
        """This autonomous runs the autonomous command selected by your RobotContainer class."""
        self.autonomousCommand = self.container.getAutonomousCommand()
        self.output("ato com", self.autonomousCommand)

        if self.autonomousCommand:
            self.autonomousCommand.schedule()

    def autonomousPeriodic(self) -> None:
        """This function is called periodically during autonomous"""

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
        self.intake = 0
        self.outtake = 0
        self.climbMode = False
        self.direction = 0



    def teleopPeriodic(self):
        self.output("current brake mode", self.container.climb.rotateArm.getIdleMode())
        self.output("liftencoder value new", self.container.climb.liftEncoder.getPosition())
        self.output("newdriveencodervalueleft", self.container.drive.leftTalon.getSelectedSensorPosition())
        self.output("newdriveencodervalueright", self.container.drive.rightTalon.getSelectedSensorPosition())
        self.output("climb mode",self.climbMode)
        if self.driverController.getLeftBumper():
            self.output("straight mode", True)
            self.direction = 0
        else:
            self.output("straight mode", False)
            self.direction = self.driverController.getLeftX()

        self.speed = addDeadzone(self.driverController.getLeftY()) * -1 # TODO: Clean up

        if self.operatorController.getStartButtonPressed():
            # self.output("")
            self.climbMode = not self.climbMode
            if self.climbMode:
                self.container.bindClimbMode()
            else:
                self.container.unbindClimbMode()

        if self.climbMode:
            dir = self.operatorController.getPOV()
            self.speed = 0.5
            if dir == 0:
                self.direction = 0
            elif dir == 90:
                self.speed = 0
                self.direction = 0.7
            elif dir == 180:
                self.speed *= -1
                self.direction = 0
            elif dir == 270:
                self.speed = 0
                self.direction = -0.7
            else:
                self.speed = 0
            self.output("endgame dir",dir)
            self.output("endgame drive speed",self.speed)
            self.drive.arcadeDrive(self.speed, self.direction)
            return


        if self.driverController.getAButton():
            self.speed *= 0.6
            self.direction *= 0.6
        elif self.driverController.getBButton():
            self.speed *= 0.75
            self.direction *= 0.75
        elif self.driverController.getYButton():
            self.speed *= 0.85
            self.direction *= 0.85
        elif self.driverController.getXButton():
            self.speed *= 0.5
            self.direction *= 0.5


        if self.operatorController.getLeftTriggerAxis() > 0.2:
            self.snowveyor.tankDrive(1,0)

        elif self.operatorController.getRightTriggerAxis() > 0.2:
            self.snowveyor.tankDrive(1,-1)

        elif self.operatorController.getLeftBumper():
            self.snowveyor.tankDrive(-1,0)

        elif self.operatorController.getRightBumper():
            self.snowveyor.tankDrive(-1,1)


        self.drive.arcadeDrive(self.speed, self.direction)


    def testInit(self) -> None:
        # Cancels all running commands at the start of test mode
        commands2.CommandScheduler.getInstance().cancelAll()


if __name__ == "__main__":
    wpilib.run(MyRobot)
