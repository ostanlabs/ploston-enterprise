"""Server smoke tests for Ploston Enterprise.

These tests verify that the enterprise server starts correctly and responds
to basic requests. Tests include license validation behavior.
"""

import os
import socket
import subprocess
import sys
import time

import httpx
import pytest

# Mark all tests in this module as integration and smoke tests
pytestmark = [pytest.mark.integration, pytest.mark.smoke]


def find_free_port() -> int:
    """Find a free port to use for testing."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture
def server_port() -> int:
    """Get a free port for the test server."""
    return find_free_port()


@pytest.fixture
def mock_license_key():
    """Provide a mock license key for testing.
    
    In real tests, this would be a valid test license.
    For smoke tests, we test the failure path without a license.
    """
    return "test-license-key-for-smoke-tests"


class TestEnterpriseServerWithoutLicense:
    """Test enterprise server behavior without a valid license."""

    def test_server_exits_without_license(self, server_port):
        """Test that server exits gracefully without a license."""
        # Start server without license
        env = os.environ.copy()
        env.pop("PLOSTON_LICENSE_KEY", None)
        env.pop("PLOSTON_LICENSE_FILE", None)
        
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "ploston_enterprise.server",
                "--port",
                str(server_port),
                "--host",
                "127.0.0.1",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
        
        # Server should exit with error code
        try:
            return_code = process.wait(timeout=10)
            assert return_code != 0, "Server should exit with error without license"
            
            stdout, stderr = process.communicate(timeout=5)
            # Should mention license error
            output = stdout + stderr
            assert "license" in output.lower() or "error" in output.lower()
        except subprocess.TimeoutExpired:
            process.kill()
            pytest.fail("Server should have exited without license")


@pytest.mark.skipif(
    not os.environ.get("PLOSTON_LICENSE_KEY") and not os.environ.get("PLOSTON_LICENSE_FILE"),
    reason="Requires valid license key or file"
)
class TestEnterpriseServerWithLicense:
    """Test enterprise server with a valid license.
    
    These tests only run when a valid license is available.
    """

    @pytest.fixture
    def server_process(self, server_port: int):
        """Start the enterprise server with license."""
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "ploston_enterprise.server",
                "--port",
                str(server_port),
                "--host",
                "127.0.0.1",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        
        # Wait for server to be ready
        start_time = time.time()
        server_ready = False
        
        while time.time() - start_time < 10:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(1)
                    result = s.connect_ex(("127.0.0.1", server_port))
                    if result == 0:
                        server_ready = True
                        break
            except Exception:
                pass
            time.sleep(0.1)
        
        if not server_ready:
            process.kill()
            stdout, stderr = process.communicate(timeout=5)
            pytest.fail(f"Server failed to start.\nstdout: {stdout}\nstderr: {stderr}")
        
        yield process
        
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()

    def test_server_starts_with_license(self, server_process, server_port):
        """Test that server starts with valid license."""
        assert server_process.poll() is None

    def test_health_endpoint(self, server_process, server_port):
        """Test health endpoint responds."""
        response = httpx.get(f"http://127.0.0.1:{server_port}/health", timeout=5)
        assert response.status_code == 200

    def test_mcp_endpoint(self, server_process, server_port):
        """Test MCP endpoint responds."""
        response = httpx.post(
            f"http://127.0.0.1:{server_port}/mcp",
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2024-11-05",
                    "clientInfo": {"name": "smoke-test", "version": "1.0.0"},
                },
            },
            timeout=5,
        )
        assert response.status_code == 200

    def test_rest_api_workflows_endpoint(self, server_process, server_port):
        """Test REST API workflows endpoint (dual-mode)."""
        response = httpx.get(
            f"http://127.0.0.1:{server_port}/api/v1/workflows",
            timeout=5,
        )
        assert response.status_code == 200

    def test_rest_api_tools_endpoint(self, server_process, server_port):
        """Test REST API tools endpoint (dual-mode)."""
        response = httpx.get(
            f"http://127.0.0.1:{server_port}/api/v1/tools",
            timeout=5,
        )
        assert response.status_code == 200
