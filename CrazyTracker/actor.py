import abc

from robocode_tank_royale import bot_api as ba

class Actor(abc.ABC):
    def __init__(self, bot: ba.Bot):
        self.bot = bot

    @abc.abstractmethod
    def apply(self) -> None:
        raise NotImplementedError('Child classes must implement `apply()`')