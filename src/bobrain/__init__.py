"""Bobrain — local multi-source RAG server for Claude / Cursor / Claude Desktop."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("bobrain")
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"
