from typing import Any

import asyncio

from gunner import Gunner
from scanner import Scanner
from driver import Driver

from robocode_tank_royale import bot_api as ba
from robocode_tank_royale.bot_api.events import (
    HitBotEvent,
    ScannedBotEvent,
)


class CrazyTracker(ba.Bot):
    """This robot moves in a zigzag pattern while tracking enemies with gun."""

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    async def run(self) -> None:
        self.driver = Driver(self)
        self.gunner = Gunner(self)
        self.scanner = Scanner(self)
        self.gun_turn_rate = 20.0

        while self.is_running():
            self.driver.apply()
            self.gunner.apply()
            self.scanner.apply()

            # Proceed with the turn.
            await self.go()

    async def on_scanned_bot(self, scanned_bot_event: ScannedBotEvent) -> None:
        self.gunner.on_scanned_bot(scanned_bot_event)

    async def on_hit_bot(self, bot_hit_bot_event: HitBotEvent) -> None:
        self.driver.on_hit_bot(bot_hit_bot_event)


async def main():
    b = CrazyTracker(server_secret='RECTjjm7ntrLpoYFh+kDuA/LHONbTYsLEnLMbuCnaU')
    await b.start()


if __name__ == "__main__":
    asyncio.run(main())
