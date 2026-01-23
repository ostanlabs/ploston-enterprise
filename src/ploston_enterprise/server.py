"""Enterprise server startup for Ploston Enterprise.

This module provides the server startup functionality with
license validation and enterprise feature configuration.
"""

import asyncio
import os
from typing import Optional

from ploston_core import PlostApplication
from ploston_core.extensions import (
    FeatureFlagRegistry,
    set_capabilities_provider,
)
from ploston_core.mcp_frontend import MCPFrontend, MCPServerConfig
from ploston_core.types import MCPTransport

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
        print(f"[Ploston Enterprise] Error: {e.message}")
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


async def create_server(
    config_path: Optional[str] = None,
    host: str = "0.0.0.0",
    port: int = 8080,
    with_rest_api: bool = True,
) -> PlostApplication:
    """Create Enterprise server with license validation.

    Args:
        config_path: Optional path to configuration file.
        host: HTTP host (default: 0.0.0.0)
        port: HTTP port (default: 8080)
        with_rest_api: Enable REST API alongside MCP (default: True)

    Returns:
        Configured PlostApplication instance (initialized).

    Raises:
        SystemExit: If license validation fails.
    """
    _validate_license_and_setup()

    # Create application with full component initialization
    app = PlostApplication(
        config_path=config_path,
        transport=MCPTransport.HTTP,
        http_host=host,
        http_port=port,
        with_rest_api=with_rest_api,
        rest_api_prefix="/api/v1",
        rest_api_docs=True,
    )
    await app.initialize()
    return app


def main():
    """CLI entrypoint for ploston-enterprise-server."""
    import argparse

    parser = argparse.ArgumentParser(description="Ploston Enterprise Server")
    parser.add_argument("-c", "--config", help="Config file path")
    parser.add_argument("-p", "--port", type=int, default=8080, help="HTTP port")
    parser.add_argument("--host", default="0.0.0.0", help="HTTP host")
    parser.add_argument(
        "--no-rest", action="store_true", help="Disable REST API (MCP only)"
    )
    args = parser.parse_args()

    # Validate license first (exits if invalid)
    license_info = _validate_license_and_setup()

    async def run_server():
        """Run the server with full initialization."""
        app = PlostApplication(
            config_path=args.config,
            transport=MCPTransport.HTTP,
            http_host=args.host,
            http_port=args.port,
            with_rest_api=not args.no_rest,
            rest_api_prefix="/api/v1",
            rest_api_docs=True,
        )

        mode = "dual-mode (MCP + REST)" if not args.no_rest else "MCP only"
        print(
            f"[Ploston Enterprise] Starting server on http://{args.host}:{args.port} ({mode})",
            flush=True,
        )
        print(
            f"[Ploston Enterprise] License: {license_info.tier} (expires: {license_info.expires_at})",
            flush=True,
        )

        try:
            await app.initialize()
            print("[Ploston Enterprise] Server initialized successfully", flush=True)
            await app.start()
        except KeyboardInterrupt:
            print("\n[Ploston Enterprise] Shutting down...", flush=True)
            await app.shutdown()
        except Exception as e:
            print(f"[Ploston Enterprise] Error: {e}", flush=True)
            await app.shutdown()
            raise

    asyncio.run(run_server())


if __name__ == "__main__":
    main()
