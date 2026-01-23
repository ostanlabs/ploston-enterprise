"""License models for Ploston Enterprise."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class LicenseInfo:
    """Validated license information."""

    id: str
    customer: str
    expires: datetime
    seats: int
    features: list[str]
    instance_id: str

    def is_expired(self) -> bool:
        """Check if the license has expired."""
        return datetime.utcnow() > self.expires

    def days_until_expiry(self) -> int:
        """Get the number of days until license expiry."""
        delta = self.expires - datetime.utcnow()
        return max(0, delta.days)


class LicenseError(Exception):
    """License validation error."""

    def __init__(self, message: str, code: str = "LICENSE_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)
