# Accessing Meta Ads Library

This project provides two approaches to access Meta ads data:

## 1. **Graph API Method** (Recommended for Your Account)

Use `scripts/fetch_meta_ads.py` to fetch ads from your own Meta business accounts using the Graph API.

### Setup

Your existing authentication in `ig_common.py` already handles token management. Just set your access token:

```bash
export IG_ACCESS_TOKEN="your_meta_access_token_here"
```

### Usage Examples

**List your ad accounts:**
```bash
python scripts/fetch_meta_ads.py --list-accounts
```

**Fetch campaigns from an ad account:**
```bash
python scripts/fetch_meta_ads.py --ad-account-id act_XXXXX --campaigns
```

**Fetch ads from a campaign:**
```bash
python scripts/fetch_meta_ads.py --campaign-id 123456 --ads
```

**Fetch ads from an ad set:**
```bash
python scripts/fetch_meta_ads.py --adset-id 123456 --ads
```

**Get performance insights for an ad:**
```bash
python scripts/fetch_meta_ads.py --ad-id 123456 --insights
```

### Data Storage

All fetched data is automatically saved to `./data/meta_ads/` in JSON format:
- `campaigns/` - Campaign data
- `ads/` - Ad creative and details
- `insights/` - Performance metrics

### API Fields Reference

The script fetches these fields by default:

**Campaigns:**
- id, name, objective, status, created_time, updated_time

**Ads:**
- id, name, status, created_time, updated_time
- creative.body (ad copy text)
- creative.image_url (ad image)
- creative.video_data (video info)
- creative.title, creative.description

**Insights:**
- impressions, clicks, spend, cpc (cost per click), ctr (click-through rate)

## 2. **Web Scraping Method** (Public Ads Library)

Use `scripts/meta_ads_library.py` to scrape the public Meta Ads Library without authentication.

### Setup

Requires Playwright for browser automation (usually already installed):

```bash
# Install if needed
pip install playwright

# Download browser
playwright install chromium
```

### Usage

**Scrape ads by advertiser name:**
```bash
python scripts/meta_ads_library.py "Nike" US
python scripts/meta_ads_library.py "Coca-Cola" GB
```

### Programmatic Usage

```python
import asyncio
from scripts.meta_ads_library import MetaAdsLibraryScraper

async def fetch_competitor_ads():
    scraper = MetaAdsLibraryScraper()
    
    # Scrape ads from a competitor
    ads = await scraper.scrape_ads_by_advertiser("Competitor Brand", country="US")
    
    # Save to file
    filepath = scraper.save_ads(ads, "Competitor Brand")
    
    # Load later
    data = scraper.load_ads(filepath.name)
    print(f"Found {len(data['ads'])} ads")

asyncio.run(fetch_competitor_ads())
```

### Data Structure

Scraped ads are saved as JSON with structure:
```json
{
  "advertiser": "Brand Name",
  "ad_count": 42,
  "scraped_at": "2026-09-05T12:34:56.789Z",
  "ads": [
    {
      "advertiser": "Brand Name",
      "text": "Ad copy text...",
      "image_url": "url_to_image",
      "cta_text": "Learn More",
      "scraped_at": "2026-09-05T12:34:56.789Z",
      "index": 0
    }
  ]
}
```

## Comparison

| Feature | Graph API | Web Scraping |
|---------|-----------|--------------|
| Auth Required | Yes | No |
| Data Type | Your own ads + insights | Public ads only |
| Real-time | ✓ | ✓ |
| Performance Metrics | ✓ | ✗ |
| Competitor Ads | ✗ | ✓ |
| Rate Limits | Meta API limits | Browser/network limits |
| Reliability | High | Medium (depends on site changes) |

## For Niche Research

To gather domain/niche ideas by analyzing competitor ads:

1. **Identify competitors** in your niche
2. **Scrape their ads** using the web scraping method
3. **Analyze patterns**:
   - What messaging resonates?
   - What platforms do they advertise on?
   - What's their content strategy?
   - What CTAs are they using?

Example workflow:
```bash
# Scrape several competitors
python scripts/meta_ads_library.py "CompetitorA" US
python scripts/meta_ads_library.py "CompetitorB" US
python scripts/meta_ads_library.py "CompetitorC" US

# Analyze the saved JSON files to understand the niche
```

## Limitations

- **Graph API**: Only access ads from accounts you manage
- **Web Scraping**: Meta Ads Library may have rate limiting; respect it
- Both methods are subject to Meta's Terms of Service

## Troubleshooting

### "403 Forbidden" on Graph API
- Check your access token is valid: `python scripts/check_token.py`
- Ensure your app has required permissions
- Verify the ad account ID format (should be `act_XXXXX`)

### Scraper hangs or gets no results
- Meta Ads Library UI changes occasionally; may need selector updates
- Check your internet connection
- Try a different advertiser name
- Run with `headless=False` to see what's happening:
  ```python
  ads = await scraper.scrape_ads_by_advertiser("Nike", headless=False)
  ```

### "Page did not load" in scraper
- You may need a VPN or proxy depending on your location
- Try a different country: `await scraper.scrape_ads_by_advertiser("Nike", country="GB")`

## Integration with Your Project

Consider adding these to your workflow:
- Weekly scrape of competitor ads
- Store in database for trend analysis
- Compare against your own ad strategy
- Generate insights for content strategy

See the main repo documentation for integrating this into your automation flows.
