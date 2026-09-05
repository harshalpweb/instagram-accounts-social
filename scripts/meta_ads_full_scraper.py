#!/usr/bin/env python3
"""Full scraper for Meta Ads Library - fetches ALL ads with pagination.

Uses requests + BeautifulSoup to scrape actual ads from:
https://facebook.com/ads/library

Gets complete results without pagination limits.
"""

import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode, quote
from dataclasses import dataclass, asdict

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@dataclass
class CreatorAd:
    """Digital product ad from a creator."""
    id: str
    creator_name: str
    product_name: str
    ad_copy: str
    cta_text: str
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    scraped_at: str = None

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)


class MetaAdsFullScraper:
    """Scrape ALL ads from Meta Ads Library with pagination."""

    BASE_URL = "https://www.facebook.com/ads/library"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        })
        self.data_dir = Path(__file__).parent.parent / "data" / "meta_ads" / "digital_products"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.ads_collected = []

    def build_url(self, search_term: str, country: str = "US", page: int = 1) -> str:
        """Build search URL with pagination support.

        Args:
            search_term: What to search for
            country: Country code
            page: Page number (for pagination)

        Returns:
            Full URL with parameters
        """
        params = {
            "search_type": "keyword_unordered",
            "search_term": search_term,
            "country": country,
            "active_status": "all",
            "ad_type": "all",
            "media_type": "all",
            "platform": "facebook,instagram",
        }

        # Add pagination (if supported by Meta's interface)
        if page > 1:
            params["page"] = page

        url = f"{self.BASE_URL}/?{urlencode(params)}"
        return url

    def fetch_search_results(
        self,
        search_term: str,
        country: str = "US",
        max_pages: int = 10,
        delay: float = 1.0
    ) -> list[dict]:
        """Fetch ads for a search term with pagination.

        Args:
            search_term: What to search for
            country: Country code
            max_pages: Maximum pages to fetch (10 = ~100+ ads)
            delay: Delay between requests in seconds

        Returns:
            List of ads found
        """
        all_ads = []
        logger.info(f"Fetching ads for '{search_term}' (country: {country})...")

        for page in range(1, max_pages + 1):
            try:
                url = self.build_url(search_term, country, page)
                logger.info(f"  Page {page}: {url}")

                response = self.session.get(url, timeout=10)
                response.raise_for_status()

                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')

                # Find all ad containers
                ad_containers = soup.find_all(
                    'div',
                    attrs={'data-testid': 'ad_library_ad_item'}
                )

                if not ad_containers:
                    # Try alternative selectors
                    ad_containers = soup.find_all('div', class_='x1a4a4an')
                    if not ad_containers:
                        logger.warning(f"  No ads found on page {page}")
                        break

                page_ads = []
                for idx, container in enumerate(ad_containers):
                    try:
                        ad = self._extract_ad_from_container(container, search_term, idx + (page - 1) * 10)
                        if ad:
                            page_ads.append(ad)
                    except Exception as e:
                        logger.debug(f"    Error extracting ad: {e}")
                        continue

                logger.info(f"  Found {len(page_ads)} ads on page {page}")
                all_ads.extend(page_ads)

                if len(page_ads) == 0:
                    # No more ads
                    break

                # Respectful delay between requests
                if page < max_pages:
                    time.sleep(delay)

            except requests.exceptions.RequestException as e:
                logger.error(f"  Error fetching page {page}: {e}")
                break
            except Exception as e:
                logger.error(f"  Unexpected error on page {page}: {e}")
                break

        logger.info(f"Total ads found for '{search_term}': {len(all_ads)}")
        self.ads_collected.extend(all_ads)
        return all_ads

    def _extract_ad_from_container(self, container, search_term: str, idx: int) -> Optional[dict]:
        """Extract ad data from HTML container.

        Args:
            container: BeautifulSoup element containing ad
            search_term: Search term used
            idx: Ad index

        Returns:
            Ad dictionary or None
        """
        try:
            # Extract text
            ad_text = container.get_text(separator='\n', strip=True)

            if not ad_text:
                return None

            lines = [line.strip() for line in ad_text.split('\n') if line.strip()]

            # Extract creator name (usually first line)
            creator_name = lines[0] if lines else "Unknown"

            # Extract product name (first few words or line)
            product_name = lines[1] if len(lines) > 1 else lines[0]

            # Get full copy
            ad_copy = '\n'.join(lines)

            # Extract CTA
            cta_text = self._extract_cta(ad_copy)

            # Look for image
            img = container.find('img')
            image_url = img.get('src') if img else None

            # Look for video
            video = container.find('video')
            video_url = video.get('src') if video else None

            ad_id = f"{search_term}_{idx}"

            return {
                "id": ad_id,
                "creator_name": creator_name[:100],
                "product_name": product_name[:150],
                "ad_copy": ad_copy[:1000],
                "cta_text": cta_text,
                "image_url": image_url,
                "video_url": video_url,
                "search_term": search_term,
                "scraped_at": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.debug(f"Error extracting ad: {e}")
            return None

    def _extract_cta(self, text: str) -> str:
        """Extract call-to-action from ad text.

        Args:
            text: Ad text

        Returns:
            CTA text
        """
        cta_keywords = ["learn", "enroll", "join", "sign up", "register", "buy", "start", "access", "book", "call", "download", "get"]
        text_lower = text.lower()

        for keyword in cta_keywords:
            if keyword in text_lower:
                for line in text.split('\n'):
                    if keyword in line.lower() and len(line) < 60:
                        return line.strip()

        # Return first short line that looks like a CTA
        for line in text.split('\n'):
            if 5 < len(line) < 60:
                return line.strip()

        return "Learn More"

    def search_multiple_terms(
        self,
        search_terms: list[str],
        country: str = "US",
        max_pages: int = 5,
        delay: float = 2.0
    ) -> dict:
        """Search multiple terms and collect all results.

        Args:
            search_terms: List of search terms
            country: Country code
            max_pages: Max pages per search term
            delay: Delay between searches in seconds

        Returns:
            Complete results dictionary
        """
        logger.info(f"Starting search for {len(search_terms)} terms...")

        for i, term in enumerate(search_terms, 1):
            logger.info(f"\n[{i}/{len(search_terms)}] Searching: {term}")
            self.fetch_search_results(term, country, max_pages, delay=0.5)

            if i < len(search_terms):
                time.sleep(delay)

        return self.generate_report()

    def generate_report(self) -> dict:
        """Generate analysis report of collected ads.

        Returns:
            Report dictionary
        """
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_ads": len(self.ads_collected),
            "unique_creators": len(set(ad['creator_name'] for ad in self.ads_collected)),
            "ads": self.ads_collected,
        }

        # Analysis
        by_creator = {}
        by_term = {}
        cta_usage = {}

        for ad in self.ads_collected:
            creator = ad['creator_name']
            term = ad['search_term']
            cta = ad['cta_text']

            by_creator[creator] = by_creator.get(creator, 0) + 1
            by_term[term] = by_term.get(term, 0) + 1
            cta_usage[cta] = cta_usage.get(cta, 0) + 1

        report['analysis'] = {
            "top_creators": sorted(by_creator.items(), key=lambda x: x[1], reverse=True)[:10],
            "ads_by_search_term": sorted(by_term.items(), key=lambda x: x[1], reverse=True),
            "top_ctas": sorted(cta_usage.items(), key=lambda x: x[1], reverse=True)[:10],
        }

        return report

    def save_results(self, report: dict, filename: Optional[str] = None) -> Path:
        """Save results to JSON.

        Args:
            report: Report dictionary
            filename: Output filename

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"all_digital_product_ads_{timestamp}.json"

        filepath = self.data_dir / filename

        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)

        logger.info(f"\n✅ Results saved to: {filepath}")
        return filepath

    def print_summary(self, report: dict):
        """Print summary of findings.

        Args:
            report: Report dictionary
        """
        print("\n" + "="*70)
        print("META ADS LIBRARY - COMPLETE SCAN RESULTS")
        print("="*70)

        print(f"\n📊 OVERVIEW")
        print(f"  Total Ads Collected: {report['total_ads']}")
        print(f"  Unique Creators: {report['unique_creators']}")

        analysis = report.get('analysis', {})

        print(f"\n🎯 ADS BY SEARCH TERM")
        for term, count in analysis.get('ads_by_search_term', []):
            print(f"  {term}: {count} ads")

        print(f"\n👥 TOP 10 MOST ACTIVE CREATORS")
        for idx, (creator, count) in enumerate(analysis.get('top_creators', []), 1):
            print(f"  {idx}. {creator}: {count} ads")

        print(f"\n🔘 TOP CTAs (Call-to-Actions)")
        for cta, count in analysis.get('top_ctas', []):
            print(f"  {cta}: {count} uses")

        print(f"\n📝 SAMPLE ADS (first 3)")
        for i, ad in enumerate(report.get('ads', [])[:3], 1):
            print(f"\n  Ad {i}")
            print(f"    Creator: {ad['creator_name']}")
            print(f"    Product: {ad['product_name']}")
            print(f"    CTA: {ad['cta_text']}")
            print(f"    Copy: {ad['ad_copy'][:80]}...")

        print("\n" + "="*70)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape ALL digital product ads from Meta Ads Library (no pagination limits)"
    )
    parser.add_argument(
        "--search",
        nargs="+",
        default=[
            "online course", "coaching", "masterclass", "ebook",
            "template", "bootcamp", "training program", "certification"
        ],
        help="Search terms (default: 8 digital product keywords)"
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=5,
        help="Max pages per search term (default: 5, ~50 ads per term)"
    )
    parser.add_argument(
        "--country",
        default="US",
        help="Country code (default: US)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=2.0,
        help="Delay between searches in seconds (default: 2.0)"
    )

    args = parser.parse_args()

    scraper = MetaAdsFullScraper()

    logger.info(f"Starting full scrape with {len(args.search)} search terms")
    logger.info(f"Max pages per term: {args.pages}")
    logger.info(f"Country: {args.country}")

    # Run scraper
    report = scraper.search_multiple_terms(
        search_terms=args.search,
        country=args.country,
        max_pages=args.pages,
        delay=args.delay
    )

    # Save results
    scraper.save_results(report)

    # Print summary
    scraper.print_summary(report)

    print(f"\n💾 Total data collected: {report['total_ads']} ads from {report['unique_creators']} creators")


if __name__ == "__main__":
    main()
