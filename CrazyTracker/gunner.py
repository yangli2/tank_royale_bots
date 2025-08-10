from typing import Any
import math
from robocode_tank_royale.bot_api.events import ScannedBotEvent
from actor import Actor


class Gunner(Actor):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.target_coords: list[float] | None = None
        self.target_aquisition_turn = 0

    def apply(self) -> None:
        # Turn the gun towards the tank.
        bearing_from_gun = 10000
        if self.target_coords is not None:
            bearing_from_gun = self.bot.gun_bearing_to(*self.target_coords)
            self.bot.set_turn_gun_left(bearing_from_gun)

        target_staleness = self.bot.get_turn_number() - self.target_aquisition_turn
        if (
            math.fabs(bearing_from_gun) > 3.0
            or self.target_coords is None
            or target_staleness > 30
        ):
            # We are not aimed, don't fire.
            return

        # We are aimed, fire according to distance.
        target_distance = self.bot.distance_to(*self.target_coords)
        if target_distance < 10:
            self.bot.set_fire(10)
        elif target_distance < 30:
            self.bot.set_fire(9)
        elif target_distance < 50:
            self.bot.set_fire(8)
        elif target_distance < 100:
            self.bot.set_fire(5)
        elif target_distance < 200:
            self.bot.set_fire(2.5)
        else:
            # If we're far away, fire with low power.
            self.bot.set_fire(1)

    def on_scanned_bot(self, scanned_bot_event: ScannedBotEvent) -> None:
        self.target_aquisition_turn = scanned_bot_event.turn_number
        self.target_coords = [scanned_bot_event.x, scanned_bot_event.y]
