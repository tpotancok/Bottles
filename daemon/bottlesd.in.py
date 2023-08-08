#!@PYTHON@
from dbus_next.aio import MessageBus
from dbus_next.service import ServiceInterface, method

import asyncio as aio

UID = "com.usebottles.bottles.Daemon"
UID_AS_PATH = "/com/usebottles/bottles/Daemon"


class BottlesDaemon(ServiceInterface):
    def __init__(self):
        super().__init__(UID)

    @method()
    async def RunGuiCommand(self, args: "as") -> "s":
        import shlex

        cmd = shlex.join(["bottles"] + args)
        proc = await aio.create_subprocess_shell(
            cmd, stdout=aio.subprocess.PIPE, stderr=aio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        if stdout:
            return stdout.decode()
        else:
            return ""

    @method()
    async def RunCommand(self, args: "as") -> "s":
        import shlex

        cmd = shlex.join(["bottles-cli"] + args)
        proc = await aio.create_subprocess_shell(
            cmd, stdout=aio.subprocess.PIPE, stderr=aio.subprocess.PIPE
        )

        stdout, _ = await proc.communicate()
        if stdout:
            return stdout.decode()
        else:
            return ""


async def main():
    bus = await MessageBus().connect()
    interface = BottlesDaemon()
    bus.export(UID_AS_PATH, interface)
    await bus.request_name(UID)

    await bus.wait_for_disconnect()
    print("disconnected")


aio.run(main())
