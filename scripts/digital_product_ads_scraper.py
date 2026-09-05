#!/usr/bin/env python3
"""Scrape and analyze digital product ads from individual creators.

Focuses on finding ads for:
- Online courses
- Ebooks
- Coaching/consulting
- Templates
- Masterclasses
- Digital downloads
- SaaS products
- Memberships

Usage:
    python scripts/digital_product_ads_scraper.py
    python scripts/digital_product_ads_scraper.py --search "digital marketing course"
    python scripts/digital_product_ads_scraper.py --analyze-file data/meta_ads/results.json
"""

import asyncio
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from dataclasses import dataclass, asdict

from playwright.async_api import async_playwright, Page

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Common digital product keywords
DIGITAL_PRODUCT_KEYWORDS = [
    # Courses
    "online course", "masterclass", "training program", "bootcamp",
    "certification course", "how to course", "learn online",

    # Coaching
    "coaching", "consulting", "mentorship", "business coaching",
    "life coaching", "career coaching",

    # Ebooks & Content
    "ebook", "guide", "workbook", "digital book", "pdf guide",

    # Templates & Resources
    "template", "presets", "Notion template", "Canva template",
    "design template", "business template",

    # Memberships & Access
    "membership", "access", "community", "private community",

    # SaaS & Tools
    "software", "tool", "app", "platform", "system",

    # Other
    "method", "framework", "blueprint", "formula", "secrets",
]

# Keywords to identify individual creators (vs brands)
CREATOR_KEYWORDS = [
    "entrepreneur", "founder", "creator", "solopreneur",
    "expert", "coach", "mentor", "trainer",
    "my system", "my method", "i teach", "i show", "i help",
]

# Negative keywords (big brands we want to exclude)
BRAND_EXCLUDES = [
    "nike", "adidas", "amazon", "apple", "microsoft", "google",
    "facebook", "instagram", "tiktok", "youtube", "netflix",
    "uber", "airbnb", "booking", "expedia", "dell", "hp",
    "coca cola", "pepsi", "mcdonald", "kfc", "starbucks",
]


@dataclass
class DigitalProductAd:
    """Represents a digital product ad from a creator."""

    id: str
    creator_name: str
    product_name: str
    product_type: str  # course, coaching, ebook, template, etc.
    ad_copy: str
    cta_text: str
    image_url: Optional[str]
    video_url: Optional[str]
    keywords_found: list[str]
    platform: str = "facebook,instagram"  # where ad runs
    scraped_at: str = None

    def __post_init__(self):
        if self.scraped_at is None:
            self.scraped_at = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        return asdict(self)


class DigitalProductAdsScraper:
    """Scrape digital product ads from creators across Meta platforms."""

    BASE_URL = "https://www.facebook.com/ads/library"

    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize scraper.

        Args:
            data_dir: Directory to store results (default: ./data/meta_ads)
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data" / "meta_ads" / "digital_products"

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.results: list[DigitalProductAd] = []

    async def search_digital_products(
        self,
        search_terms: Optional[list[str]] = None,
        country: str = "US",
        headless: bool = True,
    ) -> list[DigitalProductAd]:
        """Search for digital product ads from creators.

        Args:
            search_terms: Custom search terms (default: use built-in keywords)
            country: Country code
            headless: Run browser in headless mode

        Returns:
            List of found digital product ads
        """
        if search_terms is None:
            search_terms = DIGITAL_PRODUCT_KEYWORDS[:10]  # Start with top keywords

        logger.info(f"Searching for digital product ads with {len(search_terms)} terms")

        all_ads: list[DigitalProductAd] = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)

            for search_term in search_terms:
                try:
                    logger.info(f"Searching: '{search_term}'...")
                    page = await browser.new_page()

                    # Build search URL
                    url = f"{self.BASE_URL}/?search_term={search_term}&country={country}"

                    await page.goto(url, wait_until="networkidle", timeout=30000)

                    # Wait for ads to load
                    try:
                        await page.wait_for_selector(
                            '[data-testid="ad_library_ad_item"]',
                            timeout=10000
                        )
                    except:
                        logger.warning(f"No ads found for '{search_term}'")
                        await page.close()
                        continue

                    # Extract ads
                    ads = await self._extract_ads_from_page(page, search_term)
                    all_ads.extend(ads)

                    logger.info(f"Found {len(ads)} ads for '{search_term}'")
                    await page.close()

                except Exception as e:
                    logger.error(f"Error searching '{search_term}': {e}")
                    continue

            await browser.close()

        self.results = all_ads
        return all_ads

    async def _extract_ads_from_page(
        self,
        page: Page,
        search_term: str
    ) -> list[DigitalProductAd]:
        """Extract digital product ad data from page.

        Args:
            page: Playwright page object
            search_term: Search term used

        Returns:
            List of extracted ads
        """
        ads: list[DigitalProductAd] = []

        ad_containers = await page.query_selector_all('[data-testid="ad_library_ad_item"]')
        logger.debug(f"Found {len(ad_containers)} ad containers on page")

        for idx, container in enumerate(ad_containers):
            try:
                ad_text = await container.inner_text()

                # Skip if doesn't look like a digital product ad
                if not self._is_digital_product_ad(ad_text):
                    continue

                # Extract creator name (often appears first in the ad)
                creator_name = self._extract_creator_name(ad_text)

                # Determine product type
                product_type = self._determine_product_type(ad_text)

                # Extract CTA
                cta_text = self._extract_cta(ad_text)

                # Extract image/video
                image_url = None
                video_url = None

                img = await container.query_selector("img")
                if img:
                    image_url = await img.get_attribute("src")

                video = await container.query_selector("video")
                if video:
                    video_url = await video.get_attribute("src")

                # Find keywords in ad copy
                keywords_found = self._find_keywords(ad_text)

                ad = DigitalProductAd(
                    id=f"{search_term}_{idx}",
                    creator_name=creator_name or "Unknown Creator",
                    product_name=self._extract_product_name(ad_text),
                    product_type=product_type,
                    ad_copy=ad_text[:500],  # Truncate for storage
                    cta_text=cta_text,
                    image_url=image_url,
                    video_url=video_url,
                    keywords_found=keywords_found,
                )

                ads.append(ad)
                logger.debug(f"Extracted ad: {ad.product_name} by {ad.creator_name}")

            except Exception as e:
                logger.debug(f"Error extracting ad {idx}: {e}")
                continue

        return ads

    def _is_digital_product_ad(self, text: str) -> bool:
        """Check if ad is likely for a digital product.

        Args:
            text: Ad text content

        Returns:
            True if looks like digital product ad
        """
        text_lower = text.lower()

        # Must contain at least one digital product keyword
        has_product_keyword = any(
            keyword in text_lower for keyword in DIGITAL_PRODUCT_KEYWORDS
        )

        # Should NOT be a big brand
        is_big_brand = any(
            brand in text_lower for brand in BRAND_EXCLUDES
        )

        return has_product_keyword and not is_big_brand

    def _determine_product_type(self, text: str) -> str:
        """Determine the type of digital product being advertised.

        Args:
            text: Ad text

        Returns:
            Product type (course, coaching, ebook, template, etc.)
        """
        text_lower = text.lower()

        type_keywords = {
            "course": ["course", "training", "bootcamp", "certification"],
            "coaching": ["coaching", "consulting", "mentoring", "1-on-1"],
            "ebook": ["ebook", "guide", "book", "pdf", "workbook"],
            "template": ["template", "preset", "notion", "canva", "figma"],
            "community": ["community", "membership", "access", "group"],
            "saas": ["software", "tool", "app", "platform", "system"],
            "masterclass": ["masterclass", "workshop", "webinar", "seminar"],
        }

        for product_type, keywords in type_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return product_type

        return "digital_product"

    def _extract_creator_name(self, text: str) -> Optional[str]:
        """Extract creator/advertiser name from ad text.

        Args:
            text: Ad text

        Returns:
            Creator name or None
        """
        lines = text.split('\n')
        # Usually first non-empty line is the creator/product name
        for line in lines:
            line = line.strip()
            if line and len(line) < 100:  # Avoid long descriptions
                return line
        return None

    def _extract_product_name(self, text: str) -> str:
        """Extract product name from ad.

        Args:
            text: Ad text

        Returns:
            Product name
        """
        # Get first meaningful line
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if lines:
            name = lines[0]
            return name[:60] if len(name) > 60 else name
        return "Unnamed Product"

    def _extract_cta(self, text: str) -> str:
        """Extract call-to-action text.

        Args:
            text: Ad text

        Returns:
            CTA text
        """
        cta_keywords = ["learn", "enroll", "join", "sign up", "register", "buy", "start", "access"]
        text_lower = text.lower()

        for keyword in cta_keywords:
            if keyword in text_lower:
                # Find the phrase containing the keyword
                for line in text.split('\n'):
                    if keyword in line.lower():
                        return line.strip()[:60]

        return "Learn More"

    def _find_keywords(self, text: str) -> list[str]:
        """Find relevant keywords in ad text.

        Args:
            text: Ad text

        Returns:
            List of found keywords
        """
        text_lower = text.lower()
        found = []

        for keyword in DIGITAL_PRODUCT_KEYWORDS:
            if keyword in text_lower:
                found.append(keyword)

        return found[:5]  # Return top 5

    def save_results(self, filename: Optional[str] = None) -> Path:
        """Save scraped ads to JSON file.

        Args:
            filename: Output filename (default: digital_products_TIMESTAMP.json)

        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            filename = f"digital_products_{timestamp}.json"

        filepath = self.data_dir / filename

        data = {
            "scraped_at": datetime.utcnow().isoformat(),
            "ad_count": len(self.results),
            "ads": [ad.to_dict() for ad in self.results],
        }

        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

        logger.info(f"Saved {len(self.results)} ads to {filepath}")
        return filepath

    def analyze_results(self) -> dict[str, Any]:
        """Analyze scraped ads for insights.

        Returns:
            Dictionary with analysis results
        """
        if not self.results:
            return {"message": "No ads found"}

        # Group by product type
        by_type = {}
        for ad in self.results:
            if ad.product_type not in by_type:
                by_type[ad.product_type] = []
            by_type[ad.product_type].append(ad)

        # Find most common keywords
        all_keywords = {}
        for ad in self.results:
            for keyword in ad.keywords_found:
                all_keywords[keyword] = all_keywords.get(keyword, 0) + 1

        top_keywords = sorted(
            all_keywords.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Identify top creators
        by_creator = {}
        for ad in self.results:
            if ad.creator_name not in by_creator:
                by_creator[ad.creator_name] = []
            by_creator[ad.creator_name].append(ad)

        top_creators = sorted(
            by_creator.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )[:10]

        analysis = {
            "total_ads": len(self.results),
            "unique_creators": len(by_creator),
            "product_types": {
                ptype: len(ads) for ptype, ads in by_type.items()
            },
            "top_keywords": [{"keyword": kw, "count": count} for kw, count in top_keywords],
            "top_creators": [
                {
                    "name": creator,
                    "ad_count": len(ads),
                    "product_types": list(set(ad.product_type for ad in ads))
                }
                for creator, ads in top_creators
            ],
        }

        return analysis


async def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Scrape digital product ads from individual creators"
    )
    parser.add_argument(
        "--search",
        help="Custom search term",
        nargs="+",
    )
    parser.add_argument(
        "--country",
        default="US",
        help="Country code (default: US)",
    )
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Show browser window while scraping",
    )
    parser.add_argument(
        "--analyze-file",
        help="Analyze a previously saved results file",
    )

    args = parser.parse_args()

    scraper = DigitalProductAdsScraper()

    if args.analyze_file:
        # Load and analyze file
        with open(args.analyze_file) as f:
            data = json.load(f)
            scraper.results = [
                DigitalProductAd(**ad_dict) for ad_dict in data["ads"]
            ]
        logger.info(f"Loaded {len(scraper.results)} ads from {args.analyze_file}")

    else:
        # Run scraper
        search_terms = args.search if args.search else None
        await scraper.search_digital_products(
            search_terms=search_terms,
            country=args.country,
            headless=not args.no_headless,
        )
        scraper.save_results()

    # Show analysis
    analysis = scraper.analyze_results()
    print("\n" + "="*60)
    print("DIGITAL PRODUCT ADS ANALYSIS")
    print("="*60)
    print(json.dumps(analysis, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
