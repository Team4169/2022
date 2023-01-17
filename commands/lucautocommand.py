import commands2

import constants

from .drivedistance import DriveDistance
from .movecommand import MoveCommand
from subsystems.drivesubsystem import DriveSubsystem
from subsystems.snowveyorsubsystem import SnowveyorSubsystem
from .reset_gyro import ResetGyro
from .LEDcommand import LEDcommand
#from .SnowVeyerCommands.pickUp import pickUp
#from .SnowVeyerCommands.dropOff import dropOff

class LucAutoCommand(commands2.SequentialCommandGroup):
    """
    A complex auto command that drives forward, releases a hatch, and then drives backward.
    """

    def __init__(self, drive: DriveSubsystem, LEDserver): #def __init__(self, drive: DriveSubsystem, snowveyor: SnowveyorSubsystem):
        super().__init__(
            # Drive forward the specified distance
        ResetGyro(drive),
        # MoveCommand(-6.71875, 0, drive)
        # start the balencing program
        LEDcommand(LEDserver, 1),
        MoveCommand(-1.25, 0, drive),
        LEDcommand(LEDserver, 2),
        MoveCommand(0, 270, drive),
        LEDcommand(LEDserver, 3),
        MoveCommand(6, 270, drive),
        LEDcommand(LEDserver, 2),
        MoveCommand(0, 180, drive),
        LEDcommand(LEDserver, 1),
        # MoveCommand(15.5625, 180, drive),
        # # Pick up cone/cube
        #
        # MoveCommand(0, 0, drive),
        #
        # MoveCommand(15.5625, 0, drive),
        #
        # MoveCommand(0, 90, drive),
        #
        # MoveCommand(4.16667, 90, drive),
        #
        # MoveCommand(0, 0, drive),
        #
        # MoveCommand(1.25, 0, drive)
        )
