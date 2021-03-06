from subsystems.snowveyorsubsystem import SnowveyorSubsystem
import commands2
import wpilib

class Outtake(commands2.CommandBase):
    def __init__(self, speed: float, snowveyor: SnowveyorSubsystem) -> None:
        super().__init__()
        self.snowveyor = snowveyor
        self.speed = speed

    def initialize(self) -> None:
        pass

    def execute(self) -> None:
        self.snowveyor.tankDrive(self.speed, -self.speed)

    def end(self, interrupted: bool) -> None:
        self.snowveyor.tankDrive(0, 0)
