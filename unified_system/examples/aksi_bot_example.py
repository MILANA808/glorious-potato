#!/usr/bin/env python3
"""
Example: Using the AKSI Bot Module
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from aksi_bot.bot import AksiBot


def main():
    print("=== AKSI Bot Example ===\n")

    # Create bot
    print("1. Creating AKSI bot...")
    bot = AksiBot()
    print(f"   Bot ID: {bot.bot_id}\n")

    # Compute SHA-256 hash
    print("2. Computing SHA-256 hash...")
    test_data = "Hello, AKSI Bot!"
    hash_value = bot.sha256(test_data)
    print(f"   Data: {test_data}")
    print(f"   SHA-256: {hash_value}\n")

    # Verify hash
    print("3. Verifying hash...")
    is_valid = bot.verify_hash(test_data, hash_value)
    print(f"   Hash verification: {is_valid}\n")

    # Create integrity manifest
    print("4. Creating integrity manifest...")
    files = {
        "file1.txt": "Content of file 1",
        "file2.txt": "Content of file 2",
        "config.json": '{"key": "value"}'
    }
    manifest = bot.create_integrity_manifest(files)
    print(f"   Manifest created for {len(files)} files")
    print(f"   Manifest hash: {manifest['manifest_hash']}\n")

    # Verify manifest
    print("5. Verifying manifest...")
    results = bot.verify_integrity_manifest(files, manifest)
    print(f"   Verification results: {results}\n")

    # Get status
    print("6. Bot status:")
    status = bot.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
