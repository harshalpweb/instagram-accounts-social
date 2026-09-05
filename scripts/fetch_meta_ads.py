#!/usr/bin/env python3
"""Fetch ads data from Meta using the Graph API.

This script integrates with your existing Meta authentication setup in ig_common.py
to fetch ads data through the Meta Marketing API.

Usage:
    # Fetch ads insights for your business account
    python scripts/fetch_meta_ads.py --ad-account-id act_XXXXX

    # List campaigns
    python scripts/fetch_meta_ads.py --ad-account-id act_XXXXX --campaigns

    # Get ads from a specific campaign
    python scripts/fetch_meta_ads.py --campaign-id 123456 --ads
"""

import argparse
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import requests

from ig_common import MetaGraphClient, GRAPH_API_VERSION

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class MetaAdsClient:
    """Fetch ads data from Meta Graph API."""

    def __init__(self, access_token: str):
        """Initialize with access token.

        Args:
            access_token: Meta/Facebook access token
        """
        self.client = MetaGraphClient(access_token=access_token)
        self.token = access_token

    def get_ad_accounts(self) -> list[dict[str, Any]]:
        """Get all ad accounts the user has access to.

        Returns:
            List of ad account objects
        """
        logger.info("Fetching ad accounts...")
        response = self.client.get(
            path="me/adaccounts",
            params={
                "fields": "id,name,business_name,currency,timezone_name",
            }
        )
        accounts = response.get("data", [])
        logger.info(f"Found {len(accounts)} ad accounts")
        return accounts

    def get_campaigns(self, ad_account_id: str) -> list[dict[str, Any]]:
        """Get campaigns from an ad account.

        Args:
            ad_account_id: Ad account ID (act_XXXXX)

        Returns:
            List of campaign objects
        """
        logger.info(f"Fetching campaigns from {ad_account_id}...")

        # Ensure account ID has 'act_' prefix
        if not ad_account_id.startswith("act_"):
            ad_account_id = f"act_{ad_account_id}"

        response = self.client.get(
            path=f"{ad_account_id}/campaigns",
            params={
                "fields": "id,name,objective,status,created_time,updated_time",
                "limit": 100,
            }
        )

        campaigns = response.get("data", [])
        logger.info(f"Found {len(campaigns)} campaigns")
        return campaigns

    def get_ads(self, campaign_id: str) -> list[dict[str, Any]]:
        """Get ads in a campaign.

        Args:
            campaign_id: Campaign ID

        Returns:
            List of ad objects
        """
        logger.info(f"Fetching ads from campaign {campaign_id}...")

        response = self.client.get(
            path=f"{campaign_id}/ads",
            params={
                "fields": (
                    "id,name,status,created_time,updated_time,adset_id,"
                    "creative{body,image_url,video_data,title,description}"
                ),
                "limit": 100,
            }
        )

        ads = response.get("data", [])
        logger.info(f"Found {len(ads)} ads")
        return ads

    def get_adset_ads(self, adset_id: str) -> list[dict[str, Any]]:
        """Get ads in an ad set.

        Args:
            adset_id: Ad set ID

        Returns:
            List of ad objects
        """
        logger.info(f"Fetching ads from ad set {adset_id}...")

        response = self.client.get(
            path=f"{adset_id}/ads",
            params={
                "fields": (
                    "id,name,status,created_time,updated_time,"
                    "creative{body,image_url,video_data,title,description}"
                ),
                "limit": 100,
            }
        )

        ads = response.get("data", [])
        logger.info(f"Found {len(ads)} ads")
        return ads

    def get_ad_insights(
        self,
        ad_id: str,
        fields: Optional[list[str]] = None,
        date_start: Optional[str] = None,
        date_stop: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Get performance insights for an ad.

        Args:
            ad_id: Ad ID
            fields: Fields to retrieve (default: impressions, clicks, spend, cpc)
            date_start: Start date (YYYY-MM-DD)
            date_stop: End date (YYYY-MM-DD)

        Returns:
            List of insight objects
        """
        if fields is None:
            fields = ["impressions", "clicks", "spend", "cpc", "ctr"]

        params = {
            "fields": ",".join(fields),
            "level": "ad",
        }

        if date_start:
            params["date_start"] = date_start
        if date_stop:
            params["date_stop"] = date_stop

        response = self.client.get(path=f"{ad_id}/insights", params=params)
        return response.get("data", [])

    def save_data(self, data: Any, filename: str, category: str = "ads") -> Path:
        """Save fetched data to JSON file.

        Args:
            data: Data to save
            filename: Output filename
            category: Category subdirectory (campaigns, ads, insights, etc)

        Returns:
            Path to saved file
        """
        output_dir = Path(__file__).parent.parent / "data" / "meta_ads" / category
        output_dir.mkdir(parents=True, exist_ok=True)

        filepath = output_dir / filename

        with open(filepath, "w") as f:
            json.dump({
                "fetched_at": datetime.utcnow().isoformat(),
                "data": data,
            }, f, indent=2)

        logger.info(f"Saved data to {filepath}")
        return filepath


def main():
    parser = argparse.ArgumentParser(
        description="Fetch Meta ads data using Graph API"
    )
    parser.add_argument(
        "--token",
        help="Access token (or use IG_ACCESS_TOKEN env var)",
    )
    parser.add_argument(
        "--ad-account-id",
        help="Ad account ID (act_XXXXX)",
    )
    parser.add_argument(
        "--campaign-id",
        help="Campaign ID",
    )
    parser.add_argument(
        "--adset-id",
        help="Ad set ID",
    )
    parser.add_argument(
        "--ad-id",
        help="Ad ID (for insights)",
    )
    parser.add_argument(
        "--campaigns",
        action="store_true",
        help="Fetch campaigns",
    )
    parser.add_argument(
        "--ads",
        action="store_true",
        help="Fetch ads",
    )
    parser.add_argument(
        "--insights",
        action="store_true",
        help="Fetch insights",
    )
    parser.add_argument(
        "--list-accounts",
        action="store_true",
        help="List available ad accounts",
    )

    args = parser.parse_args()

    # Get token from args or environment
    token = args.token or os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        logger.error("No access token provided. Set IG_ACCESS_TOKEN or use --token")
        return

    client = MetaAdsClient(access_token=token)

    try:
        if args.list_accounts:
            accounts = client.get_ad_accounts()
            for account in accounts:
                print(f"  {account['id']}: {account['name']}")

        elif args.campaigns and args.ad_account_id:
            campaigns = client.get_campaigns(args.ad_account_id)
            client.save_data(campaigns, "campaigns.json", category="campaigns")
            for campaign in campaigns:
                print(f"  {campaign['id']}: {campaign['name']} ({campaign['status']})")

        elif args.ads and args.campaign_id:
            ads = client.get_ads(args.campaign_id)
            client.save_data(ads, f"campaign_{args.campaign_id}_ads.json")
            for ad in ads:
                print(f"  {ad['id']}: {ad['name']} ({ad['status']})")

        elif args.ads and args.adset_id:
            ads = client.get_adset_ads(args.adset_id)
            client.save_data(ads, f"adset_{args.adset_id}_ads.json")
            for ad in ads:
                print(f"  {ad['id']}: {ad['name']} ({ad['status']})")

        elif args.insights and args.ad_id:
            insights = client.get_ad_insights(args.ad_id)
            client.save_data(insights, f"ad_{args.ad_id}_insights.json", category="insights")
            print(json.dumps(insights, indent=2))

        else:
            parser.print_help()

    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == "__main__":
    main()
