"""Enterprise tier defaults for Ploston Enterprise.

This module defines the default feature flags and capabilities
for the enterprise tier based on license information.
"""

from typing import TYPE_CHECKING

from ploston_core.extensions import FeatureFlags

if TYPE_CHECKING:
    from .license import LicenseInfo


def get_enterprise_feature_flags(license_info: "LicenseInfo") -> FeatureFlags:
    """Get enterprise feature flags based on license.

    Args:
        license_info: Validated license information.

    Returns:
        FeatureFlags configured for enterprise tier.
    """
    # Base enterprise features
    flags = FeatureFlags(
        # Core features (always enabled)
        workflows=True,
        mcp=True,
        rest_api=True,
        # Premium features (enabled based on license)
        policy="policy" in license_info.features,
        patterns="patterns" in license_info.features,
        synthesis="synthesis" in license_info.features,
        parallel_execution=True,
        compensation_steps=True,
        human_approval=True,
        # Enterprise limits
        max_concurrent_executions=100,
        max_workflows=None,  # Unlimited
        telemetry_retention_days=365,
        enabled_plugins=["logging", "metrics", "policy", "patterns", "synthesis"],
    )

    return flags


ENTERPRISE_FEATURE_FLAGS = FeatureFlags(
    # Core features (enabled)
    workflows=True,
    mcp=True,
    rest_api=True,
    # Premium features (enabled)
    policy=True,
    patterns=True,
    synthesis=True,
    parallel_execution=True,
    compensation_steps=True,
    human_approval=True,
    # Enterprise limits
    max_concurrent_executions=100,
    max_workflows=None,  # Unlimited
    telemetry_retention_days=365,
    enabled_plugins=["logging", "metrics", "policy", "patterns", "synthesis"],
)
