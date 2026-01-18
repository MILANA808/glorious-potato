#!/usr/bin/env python3
"""
Unified System Main Script
===========================

Command-line interface for the unified MILANA808 system.
Provides access to all modules: crypto signatures, AKSI bot, AI notary, and bounty finder.
"""

import argparse
import json
import sys
from typing import Optional

from crypto.signatures import CryptoSigner
from aksi_bot.bot import AksiBot
from ai_notary.notary import AINotary
from bounty_finder.finder import BountyFinder


def main():
    """Main entry point for the unified system CLI."""
    parser = argparse.ArgumentParser(
        description="Unified MILANA808 System - Crypto, AKSI Bot, AI Notary, Bounty Finder"
    )

    subparsers = parser.add_subparsers(dest="module", help="Module to use")

    # Crypto module commands
    crypto_parser = subparsers.add_parser("crypto", help="Cryptographic signatures")
    crypto_parser.add_argument("--sign", help="Sign data from JSON file")
    crypto_parser.add_argument("--verify", help="Verify signed document from JSON file")
    crypto_parser.add_argument("--fingerprint", action="store_true", help="Show key fingerprint")

    # AKSI Bot commands
    aksi_parser = subparsers.add_parser("aksi", help="AKSI Bot operations")
    aksi_parser.add_argument("--sha256", help="Compute SHA-256 hash of text")
    aksi_parser.add_argument("--sha512", help="Compute SHA-512 hash of text")
    aksi_parser.add_argument("--verify", nargs=2, metavar=("DATA", "HASH"),
                           help="Verify data against hash")
    aksi_parser.add_argument("--manifest", help="Create integrity manifest from directory")
    aksi_parser.add_argument("--status", action="store_true", help="Show bot status")

    # AI Notary commands
    notary_parser = subparsers.add_parser("notary", help="AI Notary operations")
    notary_parser.add_argument("--notarize", help="Notarize document from JSON file")
    notary_parser.add_argument("--verify", help="Verify notarized document from JSON file")
    notary_parser.add_argument("--analyze", help="Analyze document from JSON file")
    notary_parser.add_argument("--stats", action="store_true", help="Show statistics")

    # Bounty Finder commands
    bounty_parser = subparsers.add_parser("bounty", help="GitHub bounty finder")
    bounty_parser.add_argument("--search", nargs="?", const="", help="Search for bounties")
    bounty_parser.add_argument("--language", help="Filter by programming language")
    bounty_parser.add_argument("--min-stars", type=int, default=0, help="Minimum stars")
    bounty_parser.add_argument("--commands", action="store_true",
                             help="Generate GitHub CLI search commands")

    args = parser.parse_args()

    if not args.module:
        parser.print_help()
        return

    # Execute based on module
    if args.module == "crypto":
        execute_crypto(args)
    elif args.module == "aksi":
        execute_aksi(args)
    elif args.module == "notary":
        execute_notary(args)
    elif args.module == "bounty":
        execute_bounty(args)


def execute_crypto(args):
    """Execute crypto module commands."""
    signer = CryptoSigner()

    if args.fingerprint:
        print(f"Key fingerprint: {signer.get_fingerprint()}")

    elif args.sign:
        with open(args.sign, 'r') as f:
            data = json.load(f)
        signed = signer.sign_data(data)
        print(json.dumps(signed, indent=2))

    elif args.verify:
        with open(args.verify, 'r') as f:
            signed_doc = json.load(f)
        is_valid = signer.verify_signature(signed_doc)
        print(f"Signature valid: {is_valid}")

    else:
        print("No action specified. Use --help for options.")


def execute_aksi(args):
    """Execute AKSI bot commands."""
    bot = AksiBot()

    if args.sha256:
        hash_value = bot.sha256(args.sha256)
        print(f"SHA-256: {hash_value}")

    elif args.sha512:
        hash_value = bot.sha512(args.sha512)
        print(f"SHA-512: {hash_value}")

    elif args.verify:
        data, expected_hash = args.verify
        is_valid = bot.verify_hash(data, expected_hash, "sha256")
        print(f"Hash valid: {is_valid}")

    elif args.manifest:
        import os
        files = {}
        for filename in os.listdir(args.manifest):
            filepath = os.path.join(args.manifest, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'rb') as f:
                    files[filename] = f.read()
        manifest = bot.create_integrity_manifest(files)
        print(json.dumps(manifest, indent=2))

    elif args.status:
        status = bot.get_status()
        print(json.dumps(status, indent=2))

    else:
        print("No action specified. Use --help for options.")


def execute_notary(args):
    """Execute AI notary commands."""
    notary = AINotary()

    if args.notarize:
        with open(args.notarize, 'r') as f:
            document = json.load(f)
        notarized = notary.notarize_document(document)
        print(json.dumps(notarized, indent=2))

    elif args.verify:
        with open(args.verify, 'r') as f:
            notarized_doc = json.load(f)
        result = notary.verify_notarization(notarized_doc)
        print(json.dumps(result, indent=2))

    elif args.analyze:
        with open(args.analyze, 'r') as f:
            document = json.load(f)
        analysis = notary.analyze_document_content(document)
        print(json.dumps(analysis, indent=2))

    elif args.stats:
        stats = notary.get_statistics()
        print(json.dumps(stats, indent=2))

    else:
        print("No action specified. Use --help for options.")


def execute_bounty(args):
    """Execute bounty finder commands."""
    finder = BountyFinder()

    if args.search is not None:
        search_info = finder.search_bounties(
            query=args.search,
            language=args.language,
            min_stars=args.min_stars
        )
        print(json.dumps(search_info, indent=2))
        print("\nTo find bounties, run the suggested command or visit the web URL.")

    elif args.commands:
        languages = [args.language] if args.language else None
        commands = finder.create_search_commands(languages)
        print("GitHub CLI commands to find bounties:")
        for cmd in commands:
            print(f"  {cmd}")

    else:
        print("No action specified. Use --help for options.")


if __name__ == "__main__":
    main()
