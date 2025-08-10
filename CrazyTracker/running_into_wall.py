from robocode_tank_royale import bot_api as ba
from robocode_tank_royale.bot_api.events import Condition

class RunningIntoWall(Condition):
    """Condition that is triggered when the bot is driving into a wall."""

    def __init__(self, bot: ba.Bot, wall_margin: float = 50.):
        super().__init__(name="RunningIntoWall")
        self.bot = bot
        self._wall_margin = wall_margin

    def test(self) -> bool:
        """Check if the bot is driving into a wall."""
        moving_forward = self.bot.get_speed() > 0.
        my_x, my_y = self.bot.get_x(), self.bot.get_y()
        wall_distances = [my_x, self.bot.get_arena_width() - my_x, my_y, self.bot.get_arena_height() - my_y]
        direction = self.bot.get_direction()
        heading_left = direction > 90 and direction < 270
        heading_right = direction < 90 or direction > 270
        heading_up = direction > 0 and direction < 180
        heading_down = direction > 180 and direction < 360
        forward_direction_checks = [heading_left, heading_right, heading_down, heading_up]
        reverse_direction_checks = [heading_right, heading_left, heading_up, heading_down]
        min_dist = min(wall_distances)
        if min_dist > self._wall_margin:
            # Too far from the wall to be running into it.
            return False
        if moving_forward:
            direction_checks = forward_direction_checks
        else:
            direction_checks = reverse_direction_checks
        return direction_checks[wall_distances.index(min_dist)]