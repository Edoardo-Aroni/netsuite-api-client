"""
NetSuite API Python Client

This package provides a modular way to authenticate with and call NetSuite's REST API.
"""

from .client import NetSuiteClient
from .auth import AuthManager
from . import config

__all__ = ["NetSuiteClient", "AuthManager", "config"]
