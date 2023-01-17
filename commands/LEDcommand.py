import commands2

from subsystems.drivesubsystem import DriveSubsystem


class LEDcommand(commands2.CommandBase):
    def __init__(self, LEDserver, command: int) -> None:
        super().__init__()
        # Feature to add - difference tolerance per command instance. Currently uses the default from DriveSubsystem
        # Feature to add - different max speed for each command. Currently uses method of DriveSubsystem.
        self.command = command
        self.LEDserver = LEDserver

    def initialize(self) -> None:
        self.sendLEDCommand(self.command)

    def execute(self) -> None:
        pass

    def end(self, interrupted: bool) -> None:
        pass

    def isFinished(self) -> bool:
        return True

    def sendLEDCommand(self, command):
        # send the specified command to the LEDserver
        if self.LEDserver.writeBulk(memoryview(bytes([command]))):
            print("Got an error sending command ", command)
            return True
        else:
            print("Success sending command ", command)
            return False