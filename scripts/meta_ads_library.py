"""Access and scrape Meta Ads Library for competitive analysis.

The Meta Ads Library (https://facebook.com/ads/library) allows viewing public ads
across Facebook, Instagram, and Messenger. This module provides tools to:

1. Scrape public ads by category/search terms
2. Store ad data locally for analysis
3. Query ads by various filters

No API access required - uses web scraping via Playwright.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlencode, quote

import requests
from playwright.async_api import async_playwright, Browser, Page

logger = logging.getLogger(__name__)


class MetaAdsLibraryScraper:
    """Scrape Meta Ads Library for public ads."""

    BASE_URL = "https://www.facebook.com/ads/library"

    # Ad library supports these categories
    CATEGORIES = {
        "all": "",
        "politics": "POLITICS",
        "housing": "HOUSING",
        "employment": "EMPLOYMENT",
        "credit": "CREDIT",
        "social_issues": "SOCIAL_ISSUES",
    }

    def __init__(self, data_dir: Optional[Path] = None):
        """Initialize scraper.

        Args:
            data_dir: Directory to store scraped ads (default: ./data/meta_ads)
        """
        if data_dir is None:
            data_dir = Path(__file__).parent.parent / "data" / "meta_ads"

        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _build_search_url(
        self,
        search_term: str,
        country: str = "US",
        category: str = "all",
        platform: str = "facebook,instagram"
    ) -> str:
        """Build Meta Ads Library search URL.

        Args:
            search_term: What to search for (advertiser name, brand, etc)
            country: Country code (US, GB, CA, etc)
            category: One of CATEGORIES keys
            platform: Comma-separated platforms (facebook, instagram, messenger)

        Returns:
            Full search URL for the Ads Library
        """
        params = {
            "active_status": "all",
            "ad_type": "all",
            "country": country,
            "media_type": "all",
            "platform": platform,
            "search_type": "keyword_unordered",
        }

        # Add category if specified
        if category and category != "all":
            params["ad_type"] = self.CATEGORIES.get(category, "")

        # Add search term
        if search_term:
            params["search_type"] = "keyword_unordered"
            # The search_term needs to be in the URL path, not params

        # Build URL: base + search_term + params
        url = f"{self.BASE_URL}/?{urlencode(params)}"

        # Append search term to path if provided
        if search_term:
            url = f"{self.BASE_URL}/?search_term={quote(search_term)}&{urlencode(params)}"

        return url

    async def scrape_ads_by_advertiser(
        self,
        advertiser_name: str,
        country: str = "US",
        headless: bool = True
    ) -> list[dict[str, Any]]:
        """Scrape ads from a specific advertiser.

        Args:
            advertiser_name: Name of the advertiser/brand
            country: Country code
            headless: Run browser in headless mode

        Returns:
            List of ad data dicts
        """
        url = self._build_search_url(
            search_term=advertiser_name,
            country=country
        )

        logger.info(f"Scraping ads for '{advertiser_name}' from {url}")

        ads = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=headless)
            page = await browser.new_page()

            try:
                # Navigate to ads library
                await page.goto(url, wait_until="networkidle")

                # Wait for ads to load
                await page.wait_for_selector('[data-testid="ad_library_ad_item"]', timeout=10000)

                # Extract ad data
                ads = await self._extract_ads_from_page(page, advertiser_name)

            except Exception as e:
                logger.error(f"Error scraping ads: {e}")
            finally:
                await browser.close()

        return ads

    async def _extract_ads_from_page(
        self,
        page: Page,
        advertiser_name: str
    ) -> list[dict[str, Any]]:
        """Extract ad data from loaded page.

        Args:
            page: Playwright page object
            advertiser_name: Name of advertiser

        Returns:
            List of ad data
        """
        ads = []

        # Get all ad containers
        ad_containers = await page.query_selector_all('[data-testid="ad_library_ad_item"]')
        logger.info(f"Found {len(ad_containers)} ads on page")

        for idx, container in enumerate(ad_containers):
            try:
                # Extract ad text
                ad_text = await container.inner_text()

                # Try to extract more structured data
                ad_data = {
                    "advertiser": advertiser_name,
                    "text": ad_text,
                    "scraped_at": datetime.utcnow().isoformat(),
                    "index": idx,
                }

                # Look for images
                img = await container.query_selector("img")
                if img:
                    ad_data["image_url"] = await img.get_attribute("src")

                # Look for call-to-action button text
                cta_btn = await container.query_selector("[role='button']")
                if cta_btn:
                    ad_data["cta_text"] = await cta_btn.inner_text()

                ads.append(ad_data)

            except Exception as e:
                logger.warning(f"Error extracting ad {idx}: {e}")
                continue

        return ads

    def save_ads(self, ads: list[dict], advertiser_name: str) -> Path:
        """Save ads to JSON file.

        Args:
            ads: List of ad dicts
            advertiser_name: Advertiser name for filename

        Returns:
            Path to saved file
        """
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{advertiser_name.replace(' ', '_')}_{timestamp}.json"
        filepath = self.data_dir / filename

        with open(filepath, "w") as f:
            json.dump({
                "advertiser": advertiser_name,
                "ad_count": len(ads),
                "scraped_at": datetime.utcnow().isoformat(),
                "ads": ads,
            }, f, indent=2)

        logger.info(f"Saved {len(ads)} ads to {filepath}")
        return filepath

    def load_ads(self, filename: str) -> dict[str, Any]:
        """Load previously scraped ads from file.

        Args:
            filename: JSON filename in data directory

        Returns:
            Ads data dict
        """
        filepath = self.data_dir / filename
        with open(filepath) as f:
            return json.load(f)


class MetaAdsLibraryAPI:
    """Alternative: Use Meta Marketing API for ads data.

    Requires:
    - Access token from Meta Business Account
    - App with Ad Account permissions
    """

    API_VERSION = "v21.0"
    BASE_URL = f"https://graph.facebook.com/{API_VERSION}"

    def __init__(self, access_token: str):
        """Initialize API client.

        Args:
            access_token: Meta Business access token
        """
        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
        })

    def get_ad_account_campaigns(self, ad_account_id: str) -> list[dict]:
        """Get campaigns from an ad account.

        Args:
            ad_account_id: Ad account ID (act_XXXXX format)

        Returns:
            List of campaign objects
        """
        url = f"{self.BASE_URL}/{ad_account_id}/campaigns"
        params = {
            "fields": "id,name,objective,status,created_time",
            "limit": 100,
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])

    def get_campaign_ads(self, campaign_id: str) -> list[dict]:
        """Get ads in a campaign.

        Args:
            campaign_id: Campaign ID

        Returns:
            List of ad objects
        """
        url = f"{self.BASE_URL}/{campaign_id}/ads"
        params = {
            "fields": "id,name,adset_id,creative,status,created_time",
            "limit": 100,
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", [])


if __name__ == "__main__":
    import asyncio
    import sys

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) < 2:
        print("Usage: python meta_ads_library.py <advertiser_name> [country]")
        print("Example: python meta_ads_library.py 'Nike' US")
        sys.exit(1)

    advertiser = sys.argv[1]
    country = sys.argv[2] if len(sys.argv) > 2 else "US"

    async def main():
        scraper = MetaAdsLibraryScraper()
        ads = await scraper.scrape_ads_by_advertiser(advertiser, country)
        scraper.save_ads(ads, advertiser)

    asyncio.run(main())
