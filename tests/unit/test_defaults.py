"""Unit tests for ploston-enterprise defaults module."""

from ploston_core.extensions import FeatureFlags

from ploston_enterprise.defaults import (
    ENTERPRISE_FEATURE_FLAGS,
    get_enterprise_feature_flags,
)


class TestEnterpriseFeatureFlags:
    """Test enterprise feature flags configuration."""

    def test_feature_flags_is_feature_flags_instance(self):
        """Test that ENTERPRISE_FEATURE_FLAGS is a FeatureFlags instance."""
        assert isinstance(ENTERPRISE_FEATURE_FLAGS, FeatureFlags)

    def test_feature_flags_has_core_features_enabled(self):
        """Test that core features are enabled."""
        assert ENTERPRISE_FEATURE_FLAGS.workflows is True
        assert ENTERPRISE_FEATURE_FLAGS.mcp is True
        assert ENTERPRISE_FEATURE_FLAGS.rest_api is True

    def test_feature_flags_has_premium_features_enabled(self):
        """Test that premium features are enabled for enterprise."""
        assert ENTERPRISE_FEATURE_FLAGS.policy is True
        assert ENTERPRISE_FEATURE_FLAGS.patterns is True
        assert ENTERPRISE_FEATURE_FLAGS.synthesis is True

    def test_feature_flags_has_enterprise_limits(self):
        """Test that enterprise limits are set correctly."""
        assert ENTERPRISE_FEATURE_FLAGS.max_concurrent_executions == 100
        assert ENTERPRISE_FEATURE_FLAGS.max_workflows is None  # Unlimited
        assert ENTERPRISE_FEATURE_FLAGS.telemetry_retention_days == 365

    def test_feature_flags_has_parallel_execution(self):
        """Test that parallel execution is enabled."""
        assert ENTERPRISE_FEATURE_FLAGS.parallel_execution is True

    def test_feature_flags_has_compensation_steps(self):
        """Test that compensation steps are enabled."""
        assert ENTERPRISE_FEATURE_FLAGS.compensation_steps is True

    def test_feature_flags_has_human_approval(self):
        """Test that human approval is enabled."""
        assert ENTERPRISE_FEATURE_FLAGS.human_approval is True

    def test_feature_flags_has_enabled_plugins(self):
        """Test that enterprise plugins are enabled."""
        plugins = ENTERPRISE_FEATURE_FLAGS.enabled_plugins
        assert "logging" in plugins
        assert "metrics" in plugins
        assert "policy" in plugins
        assert "patterns" in plugins
        assert "synthesis" in plugins


class TestGetEnterpriseFeatureFlags:
    """Test the get_enterprise_feature_flags function."""

    def test_returns_feature_flags_instance(self):
        """Test that function returns FeatureFlags instance."""

        # Create a mock license info
        class MockLicenseInfo:
            features = ["policy", "patterns", "synthesis"]

        flags = get_enterprise_feature_flags(MockLicenseInfo())
        assert isinstance(flags, FeatureFlags)

    def test_enables_features_based_on_license(self):
        """Test that features are enabled based on license."""

        class MockLicenseInfo:
            features = ["policy"]

        flags = get_enterprise_feature_flags(MockLicenseInfo())
        assert flags.policy is True
        assert flags.patterns is False
        assert flags.synthesis is False

    def test_core_features_always_enabled(self):
        """Test that core features are always enabled."""

        class MockLicenseInfo:
            features = []

        flags = get_enterprise_feature_flags(MockLicenseInfo())
        assert flags.workflows is True
        assert flags.mcp is True
        assert flags.rest_api is True
