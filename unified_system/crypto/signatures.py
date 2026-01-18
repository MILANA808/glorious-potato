"""
Cryptographic Signature Module
================================

Provides cryptographic signing and verification capabilities using
Ed25519 digital signatures.
"""

import hashlib
import base64
import json
from typing import Dict, Any, Optional
from datetime import datetime


class CryptoSigner:
    """
    Handles cryptographic signing and verification of data.

    Uses Ed25519 for digital signatures, providing:
    - Strong security with small key sizes
    - Fast signing and verification
    - Deterministic signatures
    """

    def __init__(self, private_key: Optional[bytes] = None):
        """
        Initialize the CryptoSigner.

        Args:
            private_key: Optional Ed25519 private key (32 bytes).
                        If None, a new key pair will be generated.
        """
        try:
            from cryptography.hazmat.primitives.asymmetric import ed25519
            from cryptography.hazmat.primitives import serialization
            self._ed25519 = ed25519
            self._serialization = serialization
        except ImportError:
            raise ImportError(
                "cryptography library required. Install with: pip install cryptography"
            )

        if private_key:
            self.private_key = self._ed25519.Ed25519PrivateKey.from_private_bytes(private_key)
        else:
            self.private_key = self._ed25519.Ed25519PrivateKey.generate()

        self.public_key = self.private_key.public_key()

    def sign_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sign data with the private key.

        Args:
            data: Dictionary containing data to sign

        Returns:
            Dictionary with original data plus signature and metadata
        """
        # Add timestamp and convert to JSON
        signing_data = {
            **data,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # Serialize data for signing
        data_bytes = json.dumps(signing_data, sort_keys=True).encode('utf-8')

        # Create signature
        signature = self.private_key.sign(data_bytes)

        # Create signed document
        signed_doc = {
            "data": signing_data,
            "signature": base64.b64encode(signature).decode('utf-8'),
            "public_key": base64.b64encode(
                self.public_key.public_bytes(
                    encoding=self._serialization.Encoding.Raw,
                    format=self._serialization.PublicFormat.Raw
                )
            ).decode('utf-8'),
            "algorithm": "Ed25519",
        }

        return signed_doc

    def verify_signature(self, signed_doc: Dict[str, Any]) -> bool:
        """
        Verify a signed document.

        Args:
            signed_doc: Signed document with signature and public key

        Returns:
            True if signature is valid, False otherwise
        """
        try:
            # Extract components
            data = signed_doc["data"]
            signature = base64.b64decode(signed_doc["signature"])
            public_key_bytes = base64.b64decode(signed_doc["public_key"])

            # Reconstruct public key
            public_key = self._ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)

            # Serialize data for verification
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')

            # Verify signature
            public_key.verify(signature, data_bytes)
            return True

        except Exception as e:
            print(f"Verification failed: {e}")
            return False

    def get_fingerprint(self) -> str:
        """
        Get SHA-256 fingerprint of the public key.

        Returns:
            Hex-encoded fingerprint
        """
        public_key_bytes = self.public_key.public_bytes(
            encoding=self._serialization.Encoding.Raw,
            format=self._serialization.PublicFormat.Raw
        )
        return hashlib.sha256(public_key_bytes).hexdigest()

    def export_private_key(self) -> bytes:
        """
        Export private key in raw format.

        Returns:
            32-byte private key
        """
        return self.private_key.private_bytes(
            encoding=self._serialization.Encoding.Raw,
            format=self._serialization.PrivateFormat.Raw,
            encryption_algorithm=self._serialization.NoEncryption()
        )

    def export_public_key(self) -> bytes:
        """
        Export public key in raw format.

        Returns:
            32-byte public key
        """
        return self.public_key.public_bytes(
            encoding=self._serialization.Encoding.Raw,
            format=self._serialization.PublicFormat.Raw
        )
