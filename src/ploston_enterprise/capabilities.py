"""Enterprise capabilities provider for Ploston Enterprise."""

from typing import Optional

from ploston_core.extensions import FeatureFlagRegistry, PluginRegistry
from ploston_core.extensions.capabilities import (
    Capabilities,
    CapabilitiesProvider,
)

from .license import LicenseInfo


class EnterpriseCapabilitiesProvider(CapabilitiesProvider):
    """Enterprise capabilities provider.

    Returns full feature set and license info.
    """

    def __init__(self, version: str, license_info: Optional[LicenseInfo] = None):
        self._license = license_info
        self._version = version

    def get_capabilities(self) -> Capabilities:
        """Get enterprise capabilities based on license."""
        flags = FeatureFlagRegistry.flags()
        plugins = PluginRegistry.get().get_enabled_features()

        # Build license dict if license info is available
        license_dict = None
        if self._license:
            license_dict = {
                "id": self._license.id,
                "expires": self._license.expires.isoformat() if self._license.expires else None,
                "seats": self._license.seats,
                "features": self._license.features,
            }

        return Capabilities(
            tier="enterprise",
            version=self._version,
            features={
                "workflows": flags.workflows,
                "mcp": flags.mcp,
                "rest_api": flags.rest_api,
                "plugins": plugins,
                "policy": flags.policy,
                "patterns": flags.patterns,
                "synthesis": flags.synthesis,
                "parallel_execution": flags.parallel_execution,
            },
            limits={
                "max_concurrent_executions": flags.max_concurrent_executions,
                "max_workflows": flags.max_workflows,
                "telemetry_retention_days": flags.telemetry_retention_days,
            },
            license=license_dict,
        )

