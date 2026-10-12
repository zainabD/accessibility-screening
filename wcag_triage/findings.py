"""What a finding looks like, and how findings get sorted.

Finding the problems is the easy part. Most accessibility tools stop there and
hand you a long flat list. What I actually needed to know was which ones to fix
first, so that is what this sorts on.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum


class Impact(IntEnum):
    """How badly a problem blocks someone.

    Ordered worst first so sorting works. This is about what it does to the
    person using the page, not how hard it is to fix.
    """

    BLOCKER = 4   # a user relying on assistive tech cannot complete the task
    SERIOUS = 3   # the task is possible but significantly harder
    MODERATE = 2  # confusing or inconsistent, workable
    MINOR = 1     # a polish issue


@dataclass(frozen=True)
class Criterion:
    """A WCAG success criterion."""

    number: str   # e.g. "1.1.1"
    name: str     # e.g. "Non-text Content"
    level: str    # "A" or "AA"

    def __str__(self) -> str:
        return f"WCAG {self.number} {self.name} (Level {self.level})"


@dataclass
class Finding:
    criterion: Criterion
    impact: Impact
    message: str
    snippet: str
    # How many times this same problem shows up on the page. One missing alt
    # is a bug. Forty means something is wrong with the process, and you fix
    # that differently.
    count: int = 1
    remediation: str | None = None
    tags: list[str] = field(default_factory=list)

    @property
    def priority(self) -> tuple:
        """Sort key: worst impact first, then most widespread, then Level A."""
        return (-self.impact, -self.count, self.criterion.level != "A")
