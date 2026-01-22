"""Enterprise capabilities provider for Ploston Enterprise."""

from ploston_core.extensions.capabilities import (
    Capabilities,
    LicenseInfo as CapLicenseInfo,
    CapabilitiesProvider,
)
from ploston_core.extensions import FeatureFlagRegistry, PluginRegistry

from .license import LicenseInfo


class EnterpriseCapabilitiesProvider(CapabilitiesProvider):
    """Enterprise capabilities provider.
    
    Returns full feature set and license info.
    """
    
    def __init__(self, license_info: LicenseInfo, version: str):
        self._license = license_info
        self._version = version
    
    def get_capabilities(self) -> Capabilities:
        """Get enterprise capabilities based on license."""
        flags = FeatureFlagRegistry.flags()
        plugins = PluginRegistry.get().get_enabled_features()
        
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
            },
            limits={
                "max_concurrent_workflows": flags.max_concurrent_workflows,
                "max_workflow_steps": flags.max_workflow_steps,
            },
            license=CapLicenseInfo(
                id=self._license.id,
                expires=self._license.expires.isoformat(),
                seats=self._license.seats,
                features=self._license.features,
            ),
        )

