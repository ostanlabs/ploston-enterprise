#!/bin/bash
# =============================================================================
# Ploston Enterprise Docker Entrypoint
# =============================================================================
# This script starts the Ploston Enterprise MCP server with HTTP transport.
# =============================================================================

set -e

# Build command arguments
CMD_ARGS="--host ${AEL_HOST:-0.0.0.0} --port ${AEL_PORT:-8080}"

# Add config file if specified
if [ -n "${AEL_CONFIG}" ]; then
    CMD_ARGS="${CMD_ARGS} --config ${AEL_CONFIG}"
fi

# Add license key if specified
if [ -n "${PLOSTON_LICENSE_KEY}" ]; then
    export PLOSTON_LICENSE_KEY
fi

# Start the enterprise server
exec ploston-enterprise-server ${CMD_ARGS}

