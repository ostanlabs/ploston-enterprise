"""License validator for Ploston Enterprise.

This module provides license validation functionality supporting:
- Online validation via license key
- Offline validation via license file (JWT)
"""

import os
from typing import Optional

from .models import LicenseError, LicenseInfo


class LicenseValidator:
    """Validates Ploston Enterprise licenses.

    Supports:
    - Online validation via license key
    - Offline validation via license file (JWT)
    """

    LICENSE_SERVER = "https://licensing.ostanlabs.com"
    PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA...
    -----END PUBLIC KEY-----"""

    def __init__(self):
        self._cached_license: Optional[LicenseInfo] = None

    def validate(
        self,
        key: Optional[str] = None,
        file_path: Optional[str] = None,
    ) -> LicenseInfo:
        """Validate license from key or file.

        Args:
            key: License key for online validation.
            file_path: Path to license file for offline validation.

        Returns:
            Validated LicenseInfo.

        Raises:
            LicenseError: If validation fails.
        """
        if not key and not file_path:
            raise LicenseError(
                "No license provided. Set PLOSTON_LICENSE_KEY or PLOSTON_LICENSE_FILE",
                code="NO_LICENSE",
            )

        if file_path:
            return self._validate_file(file_path)

        return self._validate_key(key)

    def _validate_key(self, key: str) -> LicenseInfo:
        """Validate license key online.

        This is a stub implementation. In production, this would
        make an HTTP request to the license server.
        """
        # TODO: Implement online validation
        raise LicenseError(
            "Online license validation not yet implemented",
            code="NOT_IMPLEMENTED",
        )

    def _validate_file(self, file_path: str) -> LicenseInfo:
        """Validate license file (JWT).

        This is a stub implementation. In production, this would
        verify the JWT signature and extract license info.
        """
        if not os.path.exists(file_path):
            raise LicenseError(
                f"License file not found: {file_path}",
                code="FILE_NOT_FOUND",
            )

        # TODO: Implement JWT validation
        raise LicenseError(
            "Offline license validation not yet implemented",
            code="NOT_IMPLEMENTED",
        )

    def _get_instance_id(self) -> str:
        """Get or create unique instance ID for this installation."""
        import uuid

        instance_file = os.path.expanduser("~/.ploston/instance_id")

        if os.path.exists(instance_file):
            with open(instance_file, "r") as f:
                return f.read().strip()

        instance_id = str(uuid.uuid4())
        os.makedirs(os.path.dirname(instance_file), exist_ok=True)
        with open(instance_file, "w") as f:
            f.write(instance_id)

        return instance_id
