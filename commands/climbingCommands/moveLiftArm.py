from subsystems.climbingsubsystem import ClimbingSubsystem
import commands2


class MoveLiftArm(commands2.CommandBase):
    def __init__(self, power: float, climb: ClimbingSubsystem) -> None:
        super().__init__()
        self.power = power
        self.climb = climb

    def initialize(self):
        pass

    def execute(self) -> None:
        self.climb.setLiftArm(self.power)

    def end(self, interrupted: bool) -> None:
        self.climb.setLiftArm(0)

    def isFinished(self) -> bool:
        if self.climb.getLiftArmLimitSwitchPressed() and self.power > 0:
            return True
        if self.climb.getLiftArmEncoderDistance() < 50 and not self.climb.allow_negative:
            return True