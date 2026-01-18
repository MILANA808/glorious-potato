#!/usr/bin/env python3
"""
Example: Using the Bounty Finder Module
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from bounty_finder.finder import BountyFinder


def main():
    print("=== Bounty Finder Example ===\n")

    # Create finder
    print("1. Creating Bounty Finder...")
    finder = BountyFinder()
    print("   Bounty finder initialized\n")

    # Generate search query
    print("2. Generating search query...")
    search_info = finder.search_bounties(language="python", min_stars=100)
    print(f"   Query: {search_info['query']}")
    print(f"   Web URL: {search_info['web_url']}\n")

    # Example: Analyze sample issues
    print("3. Analyzing sample issues...")
    sample_issues = [
        {
            "number": 123,
            "title": "Feature Request - $500 Bounty Available",
            "body": "We are offering a $500 USD bounty for implementing this feature.",
            "html_url": "https://github.com/example/repo/issues/123",
            "labels": [{"name": "bounty"}, {"name": "enhancement"}],
            "repository_url": "https://api.github.com/repos/example/repo"
        },
        {
            "number": 456,
            "title": "Bug fix needed",
            "body": "This is a regular bug fix with no bounty",
            "html_url": "https://github.com/example/repo/issues/456",
            "labels": [{"name": "bug"}],
            "repository_url": "https://api.github.com/repos/example/repo"
        },
        {
            "number": 789,
            "title": "Reward: €200 for documentation improvement",
            "body": "Help us improve documentation. €200 EUR reward.",
            "html_url": "https://github.com/example/repo/issues/789",
            "labels": [{"name": "documentation"}, {"name": "💰 bounty"}],
            "repository_url": "https://api.github.com/repos/example/repo"
        }
    ]

    bounties = finder.rank_bounties(sample_issues)
    print(f"   Found {len(bounties)} likely bounties\n")

    for bounty in bounties:
        print(f"   Issue #{bounty['issue_number']}: {bounty['title']}")
        print(f"   Score: {bounty['bounty_score']}")
        if bounty['bounty_amount']:
            print(f"   Amount: {bounty['bounty_amount']['raw_text']}")
        print()

    # Get statistics
    print("4. Bounty statistics:")
    stats = finder.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print("\n=== Example Complete ===")


if __name__ == "__main__":
    main()
