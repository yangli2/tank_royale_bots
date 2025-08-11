from typing import Any

from robocode_tank_royale.bot_api.events import HitBotEvent

from actor import Actor
from running_into_wall import RunningIntoWall

class Driver(Actor):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._turn_target = -180
        self._running = False

    def apply(self) -> None:
        if not self._running:
            self.bot.set_forward(40000)
            self._running = True
        if RunningIntoWall(self.bot).test():
            self._reverse_direction()
        self._maybe_execute_new_turn()

        
    def _reverse_direction(self) -> None:
        if self.bot.target_speed > 0.0:
            self.bot.set_back(40000)
        else:
            self.bot.set_forward(40000)
    
    def _maybe_execute_new_turn(self) -> None:
        if self.bot.turn_remaining == 0.0:
            self.bot.set_turn_left(self._turn_target)
            self._turn_target *= -1

    def on_hit_bot(self, bot_hit_bot_event: HitBotEvent) -> None:
        # If we're moving into the other bot, reverse!
        if bot_hit_bot_event.is_rammed:
            self._reverse_direction()
