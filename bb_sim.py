import random

from enum import Enum
from dataclasses import dataclass
from typing import NamedTuple, Optional, List


class PAResult(Enum):
    """Result of one plate appearance"""
    hit = 1
    strikeout = 2


class GroundResult(NamedTuple):
    """Result of one plate appearance in the view of game"""
    scores: int
    outs: int


@dataclass
class Batter:
    avg: float = 0.0

    def hits_or_is_out(self) -> PAResult:
        """Get the result of this batter in this PA"""
        value = random.random()

        if self.avg > value:
            return PAResult.hit
        else:
            return PAResult.strikeout


class Ground:
    def __init__(self) -> None:
        # [home, 1st base, 2nd base, 3rd base]
        self.bases: List[Optional[Batter]] = [None, None, None, None]

    def advance(self, before: int, after: int) -> int:
        """Advance batter or runner to given base.

        Args:
            before (int): the base where runner or batter is now.
            after (int): the base where runner or batter will be.

        Returns:
            int: if runner arrives at home, return value is 1, else 0
        """
        score = 0
        if self.bases[before] is not None:
            if before != 3:
                self.bases[after] = self.bases[before]
            else:
                score += 1
            self.bases[before] = None

        return score

    def simulate_one_pa(self, batter: Batter) -> GroundResult:
        """simulate one PA

        Args:
            batter (Batter): batter who is on the box now.

        Returns:
            GroundResult: total number of scores and outs results from this PA.
        """
        # CAUTION: batter at home might be separated from ground object
        # and state of ground might be handled with PAreault directly.
        scores = 0
        outs = 0
        self.bases[0] = batter
        result = self.bases[0].hits_or_is_out()

        if result == PAResult.hit:
            for base in range(3, -1, -1):
                scores += self.advance(base, base + 1)

        elif result == PAResult.strikeout:
            outs += 1
            self.bases[0] = None

        return GroundResult(scores=scores, outs=outs)

    def end_inning(self) -> None:
        self.bases = [None, None, None, None]
