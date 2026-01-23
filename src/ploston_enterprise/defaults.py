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
        # Enterprise limits
        max_concurrent_workflows=100,
        max_workflow_steps=1000,
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
    # Enterprise limits
    max_concurrent_workflows=100,
    max_workflow_steps=1000,
)
