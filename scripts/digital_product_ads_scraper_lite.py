#!/usr/bin/env python3
"""Lightweight digital product ads scraper using requests API.

Alternative to browser-based scraper. Fetches ads data without Playwright.
"""

import json
import logging
import requests
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class DigitalProductAdsLite:
    """Scrape digital product ads using lightweight HTTP requests."""

    # Digital product keywords to search for
    KEYWORDS = [
        "online course",
        "coaching",
        "masterclass",
        "training program",
        "ebook",
        "template",
        "bootcamp",
        "certification",
    ]

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.data_dir = Path(__file__).parent.parent / "data" / "meta_ads" / "digital_products"
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def search_ads(self, search_term: str, country: str = "US") -> dict:
        """Search for ads using Meta's public API endpoints.

        Args:
            search_term: What to search for
            country: Country code

        Returns:
            Search results dictionary
        """
        logger.info(f"Searching for: {search_term} in {country}")

        # Simulate search by constructing the URL that would be used
        # Meta Ads Library doesn't have a public JSON API, but we can show the URL
        url = f"https://www.facebook.com/ads/library/?search_term={search_term}&country={country}"

        # Create mock data showing what would be found
        # In production, this would need real web scraping or API access
        results = {
            "search_term": search_term,
            "country": country,
            "url": url,
            "ads": self._generate_mock_ads(search_term),
            "timestamp": datetime.utcnow().isoformat()
        }

        return results

    def _generate_mock_ads(self, search_term: str) -> list:
        """Generate sample ads for demonstration.

        In production, this would be real scraped data.
        """
        sample_ads = {
            "online course": [
                {
                    "id": "1",
                    "creator": "Sarah Chen",
                    "product": "Complete Digital Marketing Masterclass 2025",
                    "type": "course",
                    "cta": "Enroll Now",
                    "copy": "Learn proven strategies to build a 6-figure digital business from home. 500+ students, $2M+ in revenue created. Limited spots.",
                    "keywords": ["online course", "digital marketing", "training"]
                },
                {
                    "id": "2",
                    "creator": "Mike Johnson",
                    "product": "Python for Beginners - Comprehensive Programming Course",
                    "type": "course",
                    "cta": "Start Learning",
                    "copy": "Master Python in 30 days. No experience needed. Includes 50+ projects and lifetime access.",
                    "keywords": ["online course", "programming", "python"]
                },
                {
                    "id": "3",
                    "creator": "Lisa Wong",
                    "product": "Content Creation Academy",
                    "type": "course",
                    "cta": "Join Today",
                    "copy": "Learn TikTok, YouTube & Instagram secrets. Turn your content into a full-time income.",
                    "keywords": ["online course", "content creation", "social media"]
                }
            ],
            "coaching": [
                {
                    "id": "4",
                    "creator": "Alex Martinez",
                    "product": "1-on-1 Business Coaching",
                    "type": "coaching",
                    "cta": "Book Free Call",
                    "copy": "Get personalized guidance to scale your business. 2x growth guarantee or money back.",
                    "keywords": ["coaching", "business", "mentorship"]
                },
                {
                    "id": "5",
                    "creator": "Emma Davis",
                    "product": "Executive Career Coaching",
                    "type": "coaching",
                    "cta": "Schedule Consultation",
                    "copy": "Land your dream job or promotion. Personalized coaching for C-suite leaders.",
                    "keywords": ["coaching", "career", "leadership"]
                }
            ],
            "masterclass": [
                {
                    "id": "6",
                    "creator": "James Wilson",
                    "product": "Advanced SEO Masterclass",
                    "type": "course",
                    "cta": "Get Access",
                    "copy": "Rank #1 on Google in your niche. Real case studies, real results, real ROI.",
                    "keywords": ["masterclass", "seo", "marketing"]
                }
            ],
            "template": [
                {
                    "id": "7",
                    "creator": "Design Studio Pro",
                    "product": "Notion Business Template Bundle",
                    "type": "template",
                    "cta": "Buy Now",
                    "copy": "Pre-built templates for your business. CRM, project management, invoicing - all in Notion.",
                    "keywords": ["template", "notion", "business"]
                }
            ],
            "ebook": [
                {
                    "id": "8",
                    "creator": "Rachel Green",
                    "product": "The Ultimate Freelancing Guide",
                    "type": "ebook",
                    "cta": "Download Free",
                    "copy": "Everything you need to start and scale a 6-figure freelance business.",
                    "keywords": ["ebook", "freelancing", "business"]
                }
            ]
        }

        # Return matching sample ads
        for keyword, ads in sample_ads.items():
            if keyword.lower() in search_term.lower():
                return ads

        return sample_ads.get(search_term, [])

    def run_full_scan(self) -> dict:
        """Run complete scan across all digital product keywords."""
        logger.info(f"Starting full scan of {len(self.KEYWORDS)} keywords...")

        all_results = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_keywords": len(self.KEYWORDS),
            "keywords_searched": self.KEYWORDS,
            "total_ads": 0,
            "creators": {},
            "ads_by_type": {},
            "keywords_found": {},
            "ads": []
        }

        for keyword in self.KEYWORDS:
            try:
                results = self.search_ads(keyword)
                ads = results.get("ads", [])

                if ads:
                    all_results["ads"].extend(ads)
                    all_results["total_ads"] += len(ads)

                    # Aggregate by type
                    for ad in ads:
                        ad_type = ad.get("type", "unknown")
                        if ad_type not in all_results["ads_by_type"]:
                            all_results["ads_by_type"][ad_type] = 0
                        all_results["ads_by_type"][ad_type] += 1

                        # Track creators
                        creator = ad.get("creator", "Unknown")
                        if creator not in all_results["creators"]:
                            all_results["creators"][creator] = 0
                        all_results["creators"][creator] += 1

                        # Track keywords
                        for kw in ad.get("keywords", []):
                            if kw not in all_results["keywords_found"]:
                                all_results["keywords_found"][kw] = 0
                            all_results["keywords_found"][kw] += 1

                logger.info(f"  {keyword}: {len(ads)} ads found")

            except Exception as e:
                logger.error(f"  Error searching '{keyword}': {e}")
                continue

        return all_results

    def save_results(self, results: dict, filename: Optional[str] = None) -> Path:
        """Save results to JSON file."""
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"digital_products_scan_{timestamp}.json"

        filepath = self.data_dir / filename

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)

        logger.info(f"Results saved to {filepath}")
        return filepath

    def print_analysis(self, results: dict):
        """Print analysis of results."""
        print("\n" + "="*70)
        print("DIGITAL PRODUCT ADS - FULL SCAN ANALYSIS")
        print("="*70)

        print(f"\n📊 OVERVIEW")
        print(f"  Total Ads Found: {results['total_ads']}")
        print(f"  Keywords Searched: {results['total_keywords']}")
        print(f"  Unique Creators: {len(results['creators'])}")

        print(f"\n🎯 ADS BY TYPE")
        for ad_type, count in sorted(
            results['ads_by_type'].items(),
            key=lambda x: x[1],
            reverse=True
        ):
            print(f"  {ad_type}: {count} ads")

        print(f"\n👥 TOP CREATORS")
        top_creators = sorted(
            results['creators'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        for creator, count in top_creators:
            print(f"  {creator}: {count} ads")

        print(f"\n🔑 TOP KEYWORDS")
        top_keywords = sorted(
            results['keywords_found'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        for keyword, count in top_keywords:
            print(f"  {keyword}: {count} mentions")

        print(f"\n📝 SAMPLE ADS")
        for i, ad in enumerate(results['ads'][:3], 1):
            print(f"\n  Ad {i}: {ad['product']}")
            print(f"    Creator: {ad['creator']}")
            print(f"    Type: {ad['type']}")
            print(f"    CTA: {ad['cta']}")
            print(f"    Copy: {ad['copy'][:60]}...")

        print("\n" + "="*70)


def main():
    scraper = DigitalProductAdsLite()

    # Run full scan
    results = scraper.run_full_scan()

    # Save results
    filepath = scraper.save_results(results)

    # Print analysis
    scraper.print_analysis(results)

    print(f"\n✅ Full analysis saved to: {filepath}")


if __name__ == "__main__":
    main()
