"""
AKSI Bot Module
===============

Autonomous bot with SHA hashing capabilities for data integrity and verification.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional, Union
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AksiBot:
    """
    AKSI (Autonomous Knowledge & Security Integration) Bot.

    Provides SHA hashing and data integrity verification capabilities.
    """

    def __init__(self, bot_id: Optional[str] = None):
        """
        Initialize AKSI Bot.

        Args:
            bot_id: Unique identifier for the bot instance
        """
        self.hash_history: List[Dict[str, Any]] = []
        self.bot_id = bot_id or self._generate_bot_id()
        logger.info(f"AKSI Bot initialized with ID: {self.bot_id}")

    def _generate_bot_id(self) -> str:
        """Generate a unique bot ID based on timestamp."""
        timestamp = datetime.utcnow().isoformat()
        return f"aksi_{self.sha256(timestamp)[:16]}"

    def sha256(self, data: Union[str, bytes, Dict]) -> str:
        """
        Compute SHA-256 hash of data.

        Args:
            data: String, bytes, or dictionary to hash

        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode('utf-8')

        hash_obj = hashlib.sha256(data)
        hash_value = hash_obj.hexdigest()

        # Record in history
        self.hash_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm": "sha256",
            "hash": hash_value,
            "data_type": type(data).__name__
        })

        return hash_value

    def sha512(self, data: Union[str, bytes, Dict]) -> str:
        """
        Compute SHA-512 hash of data.

        Args:
            data: String, bytes, or dictionary to hash

        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode('utf-8')

        hash_obj = hashlib.sha512(data)
        hash_value = hash_obj.hexdigest()

        # Record in history
        self.hash_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm": "sha512",
            "hash": hash_value,
            "data_type": type(data).__name__
        })

        return hash_value

    def sha3_256(self, data: Union[str, bytes, Dict]) -> str:
        """
        Compute SHA3-256 hash of data.

        Args:
            data: String, bytes, or dictionary to hash

        Returns:
            Hexadecimal hash string
        """
        if isinstance(data, dict):
            data = json.dumps(data, sort_keys=True)
        if isinstance(data, str):
            data = data.encode('utf-8')

        hash_obj = hashlib.sha3_256(data)
        hash_value = hash_obj.hexdigest()

        # Record in history
        self.hash_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "algorithm": "sha3_256",
            "hash": hash_value,
            "data_type": type(data).__name__
        })

        return hash_value

    def verify_hash(self, data: Union[str, bytes, Dict], expected_hash: str,
                   algorithm: str = "sha256") -> bool:
        """
        Verify data against an expected hash.

        Args:
            data: Data to verify
            expected_hash: Expected hash value
            algorithm: Hash algorithm to use (sha256, sha512, sha3_256)

        Returns:
            True if hash matches, False otherwise
        """
        hash_func = getattr(self, algorithm, self.sha256)
        actual_hash = hash_func(data)
        is_valid = actual_hash == expected_hash

        logger.info(f"Hash verification: {is_valid} (algorithm: {algorithm})")
        return is_valid

    def create_integrity_manifest(self, files: Dict[str, Union[str, bytes]]) -> Dict[str, Any]:
        """
        Create an integrity manifest for multiple files/data items.

        Args:
            files: Dictionary mapping file names to content

        Returns:
            Integrity manifest with hashes for all files
        """
        manifest = {
            "bot_id": self.bot_id,
            "created_at": datetime.utcnow().isoformat(),
            "files": {}
        }

        for filename, content in files.items():
            manifest["files"][filename] = {
                "sha256": self.sha256(content),
                "sha512": self.sha512(content),
                "size": len(content) if isinstance(content, (str, bytes)) else None
            }

        # Add manifest self-hash
        manifest_json = json.dumps(manifest, sort_keys=True)
        manifest["manifest_hash"] = self.sha256(manifest_json)

        return manifest

    def verify_integrity_manifest(self, files: Dict[str, Union[str, bytes]],
                                  manifest: Dict[str, Any]) -> Dict[str, bool]:
        """
        Verify files against an integrity manifest.

        Args:
            files: Dictionary mapping file names to content
            manifest: Integrity manifest to verify against

        Returns:
            Dictionary mapping file names to verification results
        """
        results = {}

        for filename, content in files.items():
            if filename not in manifest["files"]:
                results[filename] = False
                logger.warning(f"File '{filename}' not found in manifest")
                continue

            expected_sha256 = manifest["files"][filename]["sha256"]
            results[filename] = self.verify_hash(content, expected_sha256, "sha256")

        return results

    def get_hash_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of all hash operations.

        Returns:
            List of hash operation records
        """
        return self.hash_history.copy()

    def clear_history(self):
        """Clear the hash history."""
        self.hash_history.clear()
        logger.info("Hash history cleared")

    def get_status(self) -> Dict[str, Any]:
        """
        Get current bot status and statistics.

        Returns:
            Dictionary with bot status information
        """
        return {
            "bot_id": self.bot_id,
            "total_hashes": len(self.hash_history),
            "algorithms_used": list(set(h["algorithm"] for h in self.hash_history)),
            "status": "active"
        }
