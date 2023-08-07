#!@PYTHON@
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method

import asyncio

UID = "com.usebottles.bottles.Daemon"
UID_AS_PATH = "/com/usebottles/bottles/Daemon"


class BottlesDaemon(ServiceInterface):
    def __init__(self):
        super().__init__(UID)

    @method()
    def RunCommand(self, arguments: "as") -> "s":
        import subprocess

        result = subprocess.run(
            ["bottles-cli"] + arguments, capture_output=True, text=True
        )
        return result.stdout

    @method()
    def RunGuiCommand(self, arguments: "as") -> "s":
        import subprocess

        result = subprocess.run(["bottles"] + arguments, capture_output=True, text=True)
        return result.stdout

    """
    @method()
    def hello(self, your_name: "s") -> "s":
        return f"Hi there, {your_name}!"
    """


async def main():
    bus = await MessageBus().connect()
    interface = BottlesDaemon()
    bus.export(UID_AS_PATH, interface)
    await bus.request_name(UID)

    await bus.wait_for_disconnect()


asyncio.get_event_loop().run_until_complete(main())
