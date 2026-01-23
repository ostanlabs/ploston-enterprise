"""Enterprise server startup for Ploston Enterprise.

This module provides the server startup functionality with
license validation and enterprise feature configuration.
"""

import asyncio
import os
from typing import Optional

from ploston_core.extensions import (
    FeatureFlagRegistry,
    set_capabilities_provider,
)
from ploston_core.mcp_frontend import MCPFrontend, MCPServerConfig

from .capabilities import EnterpriseCapabilitiesProvider
from .defaults import get_enterprise_feature_flags
from .license import LicenseError, LicenseValidator


def _validate_license_and_setup():
    """Validate license and set up enterprise features.

    Returns:
        LicenseInfo on success.

    Raises:
        SystemExit: If license validation fails.
    """
    license_key = os.environ.get("PLOSTON_LICENSE_KEY")
    license_file = os.environ.get("PLOSTON_LICENSE_FILE")

    validator = LicenseValidator()

    try:
        license_info = validator.validate(
            key=license_key,
            file_path=license_file,
        )
    except LicenseError as e:
        print(f"Error: {e.message}")
        print("")
        print("Options:")
        print("  1. Renew license: Contact sales@ostanlabs.com")
        print("  2. Downgrade to OSS: pip install ploston (replaces enterprise)")
        print("")
        print("Your workflows and data are preserved. OSS supports all core features.")
        raise SystemExit(1)

    # Set enterprise feature flags based on license
    flags = get_enterprise_feature_flags(license_info)
    FeatureFlagRegistry.set_flags(flags)

    # Set enterprise capabilities provider
    from . import __version__

    provider = EnterpriseCapabilitiesProvider(license_info, __version__)
    set_capabilities_provider(provider)

    return license_info


def create_server(config_path: Optional[str] = None) -> MCPFrontend:
    """Create Enterprise server with license validation.

    Args:
        config_path: Optional path to configuration file.

    Returns:
        Configured MCPFrontend server instance.

    Raises:
        SystemExit: If license validation fails.
    """
    _validate_license_and_setup()
    config = MCPServerConfig()
    return MCPFrontend(config)


def create_server_with_config(
    config_path: Optional[str], server_config: MCPServerConfig
) -> MCPFrontend:
    """Create Enterprise server with custom config and license validation.

    Args:
        config_path: Optional path to configuration file.
        server_config: Server configuration to use.

    Returns:
        Configured MCPFrontend server instance.

    Raises:
        SystemExit: If license validation fails.
    """
    _validate_license_and_setup()
    return MCPFrontend(server_config)


def main():
    """CLI entrypoint for ploston-enterprise-server."""
    import argparse

    from ploston_core.config import MCPHTTPConfig
    from ploston_core.types import MCPTransport

    parser = argparse.ArgumentParser(description="Ploston Enterprise Server")
    parser.add_argument("-c", "--config", help="Config file path")
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()

    # Create HTTP config from CLI args
    http_config = MCPHTTPConfig(host=args.host, port=args.port)

    # Create server with HTTP transport
    config = MCPServerConfig(
        transport=MCPTransport.HTTP,
        http=http_config,
    )

    # Validate license and set up enterprise features
    server = create_server_with_config(args.config, config)
    asyncio.run(server.start())


if __name__ == "__main__":
    main()
