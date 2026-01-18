"""
Unified System for MILANA808 Repository Consolidation
======================================================

This module consolidates functionality from multiple MILANA808 repositories:
- Crypto signatures for secure signing
- AKSI bot with SHA hashing capabilities
- AI notary for document verification
- GitHub bounty issue finder for discovering rewarded issues
"""

__version__ = "1.0.0"
__author__ = "MILANA808"

from .crypto.signatures import CryptoSigner
from .aksi_bot.bot import AksiBot
from .ai_notary.notary import AINotary
from .bounty_finder.finder import BountyFinder

__all__ = [
    "CryptoSigner",
    "AksiBot",
    "AINotary",
    "BountyFinder",
]
