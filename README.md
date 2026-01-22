# ploston-enterprise

Ploston Enterprise - Premium Agent Execution Layer

## Overview

This package provides enterprise features for the Ploston agent execution platform,
including license validation, policy-based access control, pattern mining, and
workflow synthesis.

## Installation

```bash
pip install ploston-enterprise
```

## Usage

Set your license key:

```bash
export PLOSTON_LICENSE_KEY=your-license-key
# or
export PLOSTON_LICENSE_FILE=/path/to/license.jwt
```

Start the enterprise server:

```bash
ploston-enterprise-server --port 8080
```

## Features

- License validation (online and offline)
- Policy-based access control (RBAC/ABAC)
- Workflow pattern mining
- Workflow synthesis
- Extended limits and quotas

## License

Proprietary - Contact sales@ostanlabs.com
