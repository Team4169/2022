import commands2
import wpilib
from subsystems.drivesubsystem import DriveSubsystem


class MoveCommandTimed(commands2.CommandBase):
    def __init__(self, x: float, y: float, zrot: float float, drive: DriveSubsystem, time: float) -> None:
        super().__init__()
        # Feature to add - difference tolerance per command instance. Currently uses the default from DriveSubsystem
        # Feature to add - different max speed for each command. Currently uses method of DriveSubsystem.
        self.drive = drive
        self.x = x
        self.y= y
        self.zrot=zrot
        # print("distance goal", distance)
        # print("turn goal", heading)
        self.addRequirements(drive)
        self.time = time
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.drive.resetEncoders()
        # This increases everytime the robot remains in the target
        self.in_threshold = 0
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.drive.driveCartesian(self.x,self.y,self.zrot)

    def end(self, interrupted: bool) -> None:
        self.drive.driveCartesian(0,0,0)

    def isFinished(self) -> bool:
        if self.timer.get() > self.time:
            return True
        return False

