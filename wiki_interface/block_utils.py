from typing import List
from dataclasses import dataclass
from datetime import datetime, timezone


utc_min = datetime.replace(datetime.min, tzinfo=timezone.utc)
utc_max = datetime.replace(datetime.max, tzinfo=timezone.utc)


@dataclass(frozen=True)
class BaseBlockEvent:
    pass


@dataclass(frozen=True)
class BlockEvent(BaseBlockEvent):
    """A log event of type block/block or block/reblock.

    Target is the user who is blocked (called "title" in the logs).
    Note: the target field does not include the leading "User:".

    For an indef block, expiry will be None.  If an expiry is given,
    raises ValueError if expiry < timestamp.

    """
    target: str
    timestamp: datetime
    id: int
    expiry: datetime = None
    is_reblock: bool = False

    def __post_init__(self):
        if self.expiry and self.expiry < self.timestamp:
            raise ValueError(f'expiry ({self.expiry}) > timestamp({self.timestamp})')

    def __lt__(self, other):
        return self.timestamp < other.timestamp


@dataclass(frozen=True)
class UnblockEvent(BaseBlockEvent):
    """A log event of type block/unblock.

    Target is the user who is blocked (called "title" in the logs).
    Note: the target field does not include the leading "User:".

    """
    target: str
    timestamp: datetime
    id: int


@dataclass
class UserBlockHistory:
    """A representation of a user's block log.

    Constructor takes a iterable of BlockEvents and/or UnblockEvents
    in arbitrary order.

    """
    events: List[BaseBlockEvent]

    def __init__(self, unordered_events):
        self.events = sorted(unordered_events, key=lambda e: e.timestamp)


    def __post_init__(self):
        previous_timestamp = utc_min
        for event in self.events:
            if not isinstance(event, (BlockEvent, UnblockEvent)):
                raise ValueError(f'wrong type: {event}')
            if event.timestamp <= previous_timestamp:
                raise ValueError(f'event out of order: {event}')
            previous_timestamp = event.timestamp


    def is_blocked_at(self, timestamp):
        """Determine if the user was blocked at a specific point in time.

        Returns True if they were, False otherwise.

        """
        is_blocked = False
        for event in self.events:
            if event.timestamp > timestamp:
                break
            is_blocked = isinstance(event, BlockEvent)
        return is_blocked
