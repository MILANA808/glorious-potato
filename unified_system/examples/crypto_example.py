#!/usr/bin/env python3
"""
Example: Using the Crypto Signatures Module
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crypto.signatures import CryptoSigner


def main():
    print("=== Crypto Signatures Example ===\n")

    # Create a signer
    print("1. Creating crypto signer...")
    signer = CryptoSigner()
    print(f"   Key fingerprint: {signer.get_fingerprint()}\n")

    # Sign some data
    print("2. Signing data...")
    data = {
        "message": "Hello from MILANA808 unified system",
        "type": "test",
        "priority": "high"
    }
    signed_doc = signer.sign_data(data)
    print(f"   Data signed successfully")
    print(f"   Signature: {signed_doc['signature'][:50]}...\n")

    # Verify signature
    print("3. Verifying signature...")
    is_valid = signer.verify_signature(signed_doc)
    print(f"   Signature valid: {is_valid}\n")

    # Tamper with data and verify again
    print("4. Testing tampered data...")
    tampered_doc = signed_doc.copy()
    tampered_doc['data']['message'] = "Tampered message"
    is_valid = signer.verify_signature(tampered_doc)
    print(f"   Tampered signature valid: {is_valid}\n")

    print("=== Example Complete ===")


if __name__ == "__main__":
    main()
