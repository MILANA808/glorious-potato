#!/usr/bin/env python3
"""
Comprehensive Test Script for All Unified System Modules
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from crypto.signatures import CryptoSigner
from aksi_bot.bot import AksiBot
from ai_notary.notary import AINotary
from bounty_finder.finder import BountyFinder


def test_crypto():
    """Test crypto signatures module."""
    print("=" * 60)
    print("Testing Crypto Signatures Module")
    print("=" * 60)

    try:
        # Create signer
        signer = CryptoSigner()
        print("✓ CryptoSigner initialized")

        # Test signing
        data = {"test": "data", "number": 42}
        signed = signer.sign_data(data)
        assert "signature" in signed
        assert "public_key" in signed
        print("✓ Data signed successfully")

        # Test verification
        is_valid = signer.verify_signature(signed)
        assert is_valid is True
        print("✓ Signature verified successfully")

        # Test fingerprint
        fingerprint = signer.get_fingerprint()
        assert len(fingerprint) == 64  # SHA-256 hex
        print(f"✓ Fingerprint generated: {fingerprint[:16]}...")

        # Test tampered data
        tampered = signed.copy()
        tampered['data']['test'] = "tampered"
        is_valid = signer.verify_signature(tampered)
        assert is_valid is False
        print("✓ Tampered data correctly rejected")

        print("\n✅ All crypto tests passed!\n")
        return True

    except Exception as e:
        print(f"\n❌ Crypto test failed: {e}\n")
        return False


def test_aksi_bot():
    """Test AKSI bot module."""
    print("=" * 60)
    print("Testing AKSI Bot Module")
    print("=" * 60)

    try:
        # Create bot
        bot = AksiBot()
        assert bot.bot_id is not None
        print(f"✓ AKSI Bot initialized: {bot.bot_id}")

        # Test SHA-256
        data = "test data"
        hash_value = bot.sha256(data)
        assert len(hash_value) == 64  # SHA-256 hex length
        print(f"✓ SHA-256 computed: {hash_value[:16]}...")

        # Test hash verification
        is_valid = bot.verify_hash(data, hash_value)
        assert is_valid is True
        print("✓ Hash verification successful")

        # Test SHA-512
        hash_512 = bot.sha512(data)
        assert len(hash_512) == 128  # SHA-512 hex length
        print(f"✓ SHA-512 computed: {hash_512[:16]}...")

        # Test SHA3-256
        hash_3 = bot.sha3_256(data)
        assert len(hash_3) == 64
        print(f"✓ SHA3-256 computed: {hash_3[:16]}...")

        # Test integrity manifest
        files = {
            "file1.txt": "content1",
            "file2.txt": "content2"
        }
        manifest = bot.create_integrity_manifest(files)
        assert "files" in manifest
        assert len(manifest["files"]) == 2
        print(f"✓ Integrity manifest created for {len(files)} files")

        # Test manifest verification
        results = bot.verify_integrity_manifest(files, manifest)
        assert all(results.values())
        print("✓ Manifest verification successful")

        # Test status
        status = bot.get_status()
        assert "bot_id" in status
        assert status["status"] == "active"
        print("✓ Bot status retrieved")

        print("\n✅ All AKSI bot tests passed!\n")
        return True

    except Exception as e:
        print(f"\n❌ AKSI bot test failed: {e}\n")
        return False


def test_ai_notary():
    """Test AI notary module."""
    print("=" * 60)
    print("Testing AI Notary Module")
    print("=" * 60)

    try:
        # Create notary
        notary = AINotary()
        assert notary.notary_id is not None
        print(f"✓ AI Notary initialized: {notary.notary_id}")

        # Test notarization
        document = {
            "title": "Test Document",
            "content": "Important content",
            "version": "1.0"
        }
        notarized = notary.notarize_document(document)
        assert "notarization_certificate" in notarized
        assert "notarization_id" in notarized
        print(f"✓ Document notarized: {notarized['notarization_id']}")

        # Test verification
        verification = notary.verify_notarization(notarized)
        assert verification["valid"] is True
        assert verification["hash_matches"] is True
        print("✓ Notarization verified successfully")

        # Test tampered document
        tampered = notarized.copy()
        tampered["original_document"]["title"] = "Tampered"
        verification = notary.verify_notarization(tampered)
        assert verification["valid"] is False
        print("✓ Tampered document correctly rejected")

        # Test document analysis
        analysis = notary.analyze_document_content(document)
        assert "field_count" in analysis
        assert analysis["field_count"] == 3
        print("✓ Document analysis completed")

        # Test statistics
        stats = notary.get_statistics()
        assert stats["total_notarizations"] >= 1
        print("✓ Statistics retrieved")

        # Test export/import
        exported = notary.export_records()
        assert isinstance(exported, str)
        new_notary = AINotary()
        count = new_notary.import_records(exported)
        assert count >= 1
        print("✓ Export/import successful")

        print("\n✅ All AI notary tests passed!\n")
        return True

    except Exception as e:
        print(f"\n❌ AI notary test failed: {e}\n")
        return False


def test_bounty_finder():
    """Test bounty finder module."""
    print("=" * 60)
    print("Testing Bounty Finder Module")
    print("=" * 60)

    try:
        # Create finder
        finder = BountyFinder()
        print("✓ Bounty Finder initialized")

        # Test search query generation
        search_info = finder.search_bounties(language="python", min_stars=100)
        assert "query" in search_info
        assert "python" in search_info["query"] or "language:python" in search_info["query"]
        print(f"✓ Search query generated")

        # Test amount extraction
        text1 = "We offer $500 for this feature"
        amount = finder.extract_bounty_amount(text1)
        assert amount is not None
        assert amount["amount"] == 500
        assert amount["currency"] == "USD"
        print("✓ USD amount extracted correctly")

        text2 = "Reward: 0.5 BTC for completion"
        amount = finder.extract_bounty_amount(text2)
        assert amount is not None
        assert amount["amount"] == 0.5
        assert amount["currency"] == "BTC"
        print("✓ BTC amount extracted correctly")

        # Test issue analysis
        test_issue = {
            "number": 123,
            "title": "Feature Request - $1000 Bounty",
            "body": "We are offering a $1000 USD bounty",
            "html_url": "https://github.com/test/repo/issues/123",
            "labels": [{"name": "bounty"}, {"name": "enhancement"}],
            "repository_url": "https://api.github.com/repos/test/repo"
        }
        analysis = finder.analyze_issue(test_issue)
        assert analysis["is_likely_bounty"] is True
        assert analysis["bounty_score"] > 0
        assert analysis["bounty_amount"] is not None
        print(f"✓ Issue analyzed: score={analysis['bounty_score']}")

        # Test ranking
        issues = [
            test_issue,
            {
                "number": 456,
                "title": "Normal issue",
                "body": "No bounty here",
                "html_url": "https://github.com/test/repo/issues/456",
                "labels": [{"name": "bug"}],
                "repository_url": "https://api.github.com/repos/test/repo"
            }
        ]
        bounties = finder.rank_bounties(issues)
        assert len(bounties) >= 1
        assert bounties[0]["bounty_score"] >= 20
        print(f"✓ {len(bounties)} bounties found and ranked")

        # Test statistics
        stats = finder.get_statistics()
        assert stats["total_bounties"] >= 1
        print("✓ Statistics retrieved")

        # Test command generation
        commands = finder.create_search_commands(["python", "javascript"])
        assert len(commands) == 2
        assert all("gh search issues" in cmd for cmd in commands)
        print("✓ GitHub CLI commands generated")

        print("\n✅ All bounty finder tests passed!\n")
        return True

    except Exception as e:
        print(f"\n❌ Bounty finder test failed: {e}\n")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("UNIFIED SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 60 + "\n")

    results = {
        "Crypto Signatures": test_crypto(),
        "AKSI Bot": test_aksi_bot(),
        "AI Notary": test_ai_notary(),
        "Bounty Finder": test_bounty_finder()
    }

    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for module, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{module}: {status}")

    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  SOME TESTS FAILED")
    print("=" * 60 + "\n")

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
