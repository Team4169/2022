import wpilib
import wpilib.drive
import ctre
from constants import constants
from networktables import NetworkTables
import navx

class MyRobot(wpilib.TimedRobot):
    def robotInit(self):
        self.front_left_motor = ctre.WPI_TalonSRX(constants["frontLeftPort"])
        self.rear_left_motor = ctre.WPI_VictorSPX(constants["rearLeftPort"])
        self.rear_left_motor.setInverted(True)
        self.left = wpilib.SpeedControllerGroup(
            self.front_left_motor, self.rear_left_motor)

        self.front_right_motor = ctre.WPI_TalonSRX(constants["frontRightPort"])
        self.rear_right_motor = ctre.WPI_VictorSPX(constants["rearRightPort"])
        self.rear_right_motor.setInverted(True)
        self.right = wpilib.SpeedControllerGroup(
            self.front_right_motor, self.rear_right_motor)

        self.drive = wpilib.drive.DifferentialDrive(
            self.right,
            self.left
        )

        self.controller = wpilib.XboxController(0)
        self.timer = wpilib.Timer()
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.gyro = navx.AHRS.create_i2c()
        self.front_left_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)
        self.front_right_motor.configSelectedFeedbackSensor(
            ctre.FeedbackDevice.QuadEncoder, 0, 0)

    def autnomousInit(self):
        self.timer.reset()
        self.timer.start()

    def autonomousPeriodic(self):
        print("Time: ", self.timer.get())

    def teleopInit(self):
        print("Starting teleop...")

    def teleopPeriodic(self):
        # print("The drive X value is: ", self.controller.getX(
        #     self.controller.Hand.kLeftHand))
        # print("The drive Y value is: ", self.controller.getY(
        #     self.controller.Hand.kLeftHand))
        # print("The gyro Yaw value is: ", self.gyro.getYaw())
        # self.sd.putValue("Gyro Yaw", self.gyro.getYaw())
        # self.sd.putValue("Left Encoder Value",
        #                  self.front_left_motor.getSelectedSonsorPosition())
        # self.sd.putValue("Right Encoder Value",
        #                  self.front_right_motor.getSelectedSensorPosition())
        # self.drive.arcadeDrive(
        # 	self.controller.getX(self.controller.Hand.kLeftHand),
        # 	self.controller.getY(self.controller.Hand.kLeftHand),
        # 	True
        # )
        limelight = NetworkTables.getTable("limelight")
        print(limelight)
        print("tv: ", limelight.getNumber("tv", 0))
        print("tx: ", limelight.getNumber("tx", 0))
        print("ty: ", limelight.getNumber("ty", 0))
        print("ta: ", limelight.getNumber("ta", 0))
        print("ts: ", limelight.getNumber("ts", 0))
        print("____________________________")

if __name__ == "__main__":
    wpilib.run(MyRobot)

