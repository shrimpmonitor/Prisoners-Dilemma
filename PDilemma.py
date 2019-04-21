from axelrod.action import Action
from axelrod.player import Player

C, D = Action.C, Action.D


class AutoP(Player):
    name = "AutoP"
    classifier = {
        "memory_depth": 3,
        "stochastic": False,
        "makes_use_of": set(),
        "long_run_time": False,
        "inspects_source": False,
        "manipulates_source": False,
        "manipulates_state": False,
    }

    def __init__(self) -> None:
        """Initialise the player."""
        super().__init__()
        self.history = []
        self.score = 0
        self.mem_length = 3
        self.grudged = False
        self.grudge_memory = 0

    def strategy(self, opponent: Player) -> Action:
        """
        Player begins by playing 'C', will play 'D' if: opponent has defected more than 10% of the time, and opponent's
        last move was 'D'. Player will continue playing 'D' for 3 turns, where it will forget its grudge ONLY if
        opponent's previous move at that point is 'C'.
        """
        try:
            if opponent.defections > len(opponent.history) / 10.0:
                if opponent.history[-1] == D:
                    self.grudged = True
            if self.grudge_memory >= self.mem_length:
                if opponent.history[-1] == C:
                    self.grudge_memory = 0
                    self.grudged = False
            if self.grudged:
                self.grudge_memory += 1
                return D
            else:
                return C
        except IndexError:
            return C

    def reset(self):
        """Resets scores and history."""
        self.history = []
        self.grudged = False
        self.grudge_memory = 0
