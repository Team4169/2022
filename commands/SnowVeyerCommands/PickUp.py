from subsystems.snowveyorsubsystem import SnowveyorSubsystem
import commands2
import wpilib

class pickUp(commands2.CommandBase):
    def __init__(self, duration: float, speed:float, snowveyor: SnowveyorSubsystem) -> None:
        super().__init__()
        self.snowveyor = snowveyor
        self.speed = speed
        self.duration = duration
        self.timer = wpilib.Timer()

    def initialize(self) -> None:
        self.timer.reset()
        self.timer.start()

    def execute(self) -> None:
        self.snowveyor.tankDrive(self.speed, 0)

    def end(self, interrupted: bool) -> None:
        self.snowveyor.tankDrive(0, 0)

    def isFinished(self) -> bool:
        return self.timer.get() > self.duration