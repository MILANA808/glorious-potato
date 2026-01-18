#!/usr/bin/env python3
"""
Example: Using the AI Notary Module
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ai_notary.notary import AINotary


def main():
    print("=== AI Notary Example ===\n")

    # Create notary
    print("1. Creating AI Notary...")
    notary = AINotary()
    print(f"   Notary ID: {notary.notary_id}\n")

    # Notarize a document
    print("2. Notarizing document...")
    document = {
        "title": "Software License Agreement",
        "parties": ["MILANA808", "Client"],
        "terms": "Standard software license terms apply",
        "date": "2026-01-18"
    }
    notarized = notary.notarize_document(document, metadata={"type": "license"})
    print(f"   Document notarized")
    print(f"   Notarization ID: {notarized['notarization_id']}\n")

    # Verify notarization
    print("3. Verifying notarization...")
    verification = notary.verify_notarization(notarized)
    print(f"   Valid: {verification['valid']}")
    print(f"   Hash matches: {verification['hash_matches']}")
    print(f"   Certificate valid: {verification['certificate_valid']}\n")

    # Analyze document
    print("4. Analyzing document content...")
    analysis = notary.analyze_document_content(document)
    print(f"   Fields: {analysis['field_count']}")
    print(f"   Completeness score: {analysis['completeness_score']:.2f}\n")

    # Get statistics
    print("5. Notary statistics:")
    stats = notary.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
