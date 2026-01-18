"""
GitHub Bounty Issue Finder
===========================

Searches GitHub for issues with bounties and rewards.
"""

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BountyFinder:
    """
    Finds and tracks GitHub issues with bounties/rewards.

    Searches for issues with bounty-related keywords and labels,
    helping identify rewarded work opportunities.
    """

    # Common bounty-related keywords and labels
    BOUNTY_KEYWORDS = [
        "bounty", "reward", "prize", "compensation", "payment",
        "$", "USD", "EUR", "BTC", "ETH", "crypto",
        "gitcoin", "algora", "bountysource"
    ]

    BOUNTY_LABELS = [
        "bounty", "💰 bounty", "💵 bounty", "reward",
        "paid", "compensation", "prize"
    ]

    def __init__(self):
        """Initialize BountyFinder."""
        self.found_bounties: List[Dict[str, Any]] = []
        logger.info("BountyFinder initialized")

    def search_bounties(self, query: str = "", language: Optional[str] = None,
                       min_stars: int = 0) -> List[Dict[str, Any]]:
        """
        Search for bounty issues on GitHub.

        Args:
            query: Additional search query terms
            language: Filter by programming language
            min_stars: Minimum repository stars

        Returns:
            List of potential bounty issues
        """
        # Build search query
        search_terms = ["is:issue", "is:open"]

        # Add bounty keywords
        bounty_terms = " OR ".join(f'"{keyword}"' for keyword in self.BOUNTY_KEYWORDS[:5])
        search_terms.append(f"({bounty_terms})")

        if language:
            search_terms.append(f"language:{language}")

        if min_stars > 0:
            search_terms.append(f"stars:>={min_stars}")

        if query:
            search_terms.append(query)

        full_query = " ".join(search_terms)

        logger.info(f"Search query: {full_query}")

        # Return search query for external use (GitHub API/CLI)
        return {
            "query": full_query,
            "instructions": "Use GitHub API or CLI to execute this search",
            "example_command": f'gh search issues "{full_query}" --limit 100',
            "web_url": f"https://github.com/search?q={full_query.replace(' ', '+')}&type=issues"
        }

    def extract_bounty_amount(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract bounty amount from issue text.

        Args:
            text: Issue title or body text

        Returns:
            Dictionary with amount and currency if found
        """
        # Common patterns for bounty amounts
        patterns = [
            r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $1,000.00
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*USD',  # 1000 USD
            r'(\d+(?:\.\d+)?)\s*BTC',  # 0.5 BTC
            r'(\d+(?:\.\d+)?)\s*ETH',  # 1.5 ETH
            r'€(\d+(?:,\d{3})*(?:\.\d{2})?)',  # €1,000.00
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                currency = 'USD'

                if 'BTC' in text[match.start():match.end() + 5]:
                    currency = 'BTC'
                elif 'ETH' in text[match.start():match.end() + 5]:
                    currency = 'ETH'
                elif '€' in text[match.start():match.end()]:
                    currency = 'EUR'

                try:
                    amount = float(amount_str)
                    return {
                        "amount": amount,
                        "currency": currency,
                        "raw_text": match.group(0)
                    }
                except ValueError:
                    continue

        return None

    def analyze_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an issue to determine if it's likely a bounty.

        Args:
            issue_data: Issue data from GitHub API

        Returns:
            Analysis results with bounty likelihood score
        """
        title = issue_data.get("title", "")
        body = issue_data.get("body", "")
        labels = [label.get("name", "") for label in issue_data.get("labels", [])]

        # Calculate bounty score
        score = 0
        indicators = []

        # Check title for keywords
        title_lower = title.lower()
        for keyword in self.BOUNTY_KEYWORDS:
            if keyword.lower() in title_lower:
                score += 10
                indicators.append(f"Keyword in title: {keyword}")

        # Check body for keywords
        body_lower = body.lower()
        for keyword in self.BOUNTY_KEYWORDS:
            if keyword.lower() in body_lower:
                score += 5
                indicators.append(f"Keyword in body: {keyword}")

        # Check labels
        for label in labels:
            label_lower = label.lower()
            if any(bl.lower() in label_lower for bl in self.BOUNTY_LABELS):
                score += 20
                indicators.append(f"Bounty label: {label}")

        # Extract amount
        amount_info = self.extract_bounty_amount(title + " " + body)
        if amount_info:
            score += 30
            indicators.append(f"Amount found: {amount_info['raw_text']}")

        analysis = {
            "issue_url": issue_data.get("html_url", ""),
            "issue_number": issue_data.get("number"),
            "title": title,
            "repository": issue_data.get("repository_url", "").split("/")[-2:],
            "bounty_score": score,
            "is_likely_bounty": score >= 20,
            "indicators": indicators,
            "bounty_amount": amount_info,
            "labels": labels,
            "analyzed_at": datetime.utcnow().isoformat()
        }

        return analysis

    def rank_bounties(self, issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank issues by bounty likelihood and amount.

        Args:
            issues: List of issue data from GitHub API

        Returns:
            Sorted list of analyzed issues
        """
        analyzed = [self.analyze_issue(issue) for issue in issues]

        # Sort by bounty score (descending)
        ranked = sorted(analyzed, key=lambda x: x["bounty_score"], reverse=True)

        # Filter to likely bounties only
        likely_bounties = [b for b in ranked if b["is_likely_bounty"]]

        logger.info(f"Found {len(likely_bounties)} likely bounties out of {len(issues)} issues")

        self.found_bounties = likely_bounties
        return likely_bounties

    def filter_by_language(self, bounties: List[Dict[str, Any]],
                          language: str) -> List[Dict[str, Any]]:
        """
        Filter bounties by programming language.

        Args:
            bounties: List of analyzed bounties
            language: Programming language to filter by

        Returns:
            Filtered list of bounties
        """
        # This would require repository API calls for language detection
        # For now, return all (to be enhanced with actual API integration)
        logger.info(f"Language filter: {language} (requires API integration)")
        return bounties

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about found bounties.

        Returns:
            Statistics dictionary
        """
        if not self.found_bounties:
            return {
                "total_bounties": 0,
                "status": "no bounties found yet"
            }

        total = len(self.found_bounties)
        with_amounts = sum(1 for b in self.found_bounties if b["bounty_amount"])

        amounts = [
            b["bounty_amount"]["amount"]
            for b in self.found_bounties
            if b["bounty_amount"] and b["bounty_amount"]["currency"] == "USD"
        ]

        return {
            "total_bounties": total,
            "with_amount_info": with_amounts,
            "average_score": sum(b["bounty_score"] for b in self.found_bounties) / total,
            "max_usd_amount": max(amounts) if amounts else None,
            "min_usd_amount": min(amounts) if amounts else None,
            "generated_at": datetime.utcnow().isoformat()
        }

    def export_bounties(self, filename: Optional[str] = None) -> str:
        """
        Export found bounties to JSON.

        Args:
            filename: Optional filename to save to

        Returns:
            JSON string of bounties
        """
        export_data = {
            "exported_at": datetime.utcnow().isoformat(),
            "total_bounties": len(self.found_bounties),
            "bounties": self.found_bounties
        }

        json_str = json.dumps(export_data, indent=2)

        if filename:
            with open(filename, 'w') as f:
                f.write(json_str)
            logger.info(f"Bounties exported to {filename}")

        return json_str

    def create_search_commands(self, languages: Optional[List[str]] = None) -> List[str]:
        """
        Create GitHub CLI search commands for finding bounties.

        Args:
            languages: Optional list of programming languages

        Returns:
            List of gh CLI commands to execute
        """
        commands = []

        base_terms = [
            'is:issue',
            'is:open',
            '(bounty OR reward OR prize OR "$")'
        ]

        if languages:
            for lang in languages:
                search = ' '.join(base_terms + [f'language:{lang}'])
                commands.append(f'gh search issues "{search}" --limit 50')
        else:
            search = ' '.join(base_terms)
            commands.append(f'gh search issues "{search}" --limit 100')

        return commands
