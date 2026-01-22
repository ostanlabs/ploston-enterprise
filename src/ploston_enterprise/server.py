"""Enterprise server startup for Ploston Enterprise.

This module provides the server startup functionality with
license validation and enterprise feature configuration.
"""

import asyncio
import os
from typing import Optional

from ploston_core.mcp_frontend import MCPFrontend, MCPServerConfig
from ploston_core.extensions import (
    FeatureFlagRegistry,
    set_capabilities_provider,
)

from .defaults import get_enterprise_feature_flags
from .license import LicenseValidator, LicenseError
from .capabilities import EnterpriseCapabilitiesProvider


def create_server(config_path: Optional[str] = None) -> MCPFrontend:
    """Create Enterprise server with license validation.
    
    Args:
        config_path: Optional path to configuration file.
        
    Returns:
        Configured MCPFrontend server instance.
        
    Raises:
        SystemExit: If license validation fails.
    """
    # Validate license FIRST
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
    
    # Create server with default config
    config = MCPServerConfig()
    return MCPFrontend(config)


def main():
    """CLI entrypoint for ploston-enterprise-server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ploston Enterprise Server")
    parser.add_argument("-c", "--config", help="Config file path")
    parser.add_argument("-p", "--port", type=int, default=8080)
    parser.add_argument("--host", default="0.0.0.0")
    args = parser.parse_args()
    
    server = create_server(args.config)
    asyncio.run(server.run())


if __name__ == "__main__":
    main()

