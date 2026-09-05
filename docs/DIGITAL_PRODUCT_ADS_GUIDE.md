# Finding Digital Product Ads from Creators

Find what digital products individual creators are advertising across Meta platforms (Facebook, Instagram, Messenger).

## Quick Start

**Search for all digital product ads:**
```bash
python scripts/digital_product_ads_scraper.py
```

**Search for specific products (e.g., online courses):**
```bash
python scripts/digital_product_ads_scraper.py --search "online course"
python scripts/digital_product_ads_scraper.py --search "coaching" "masterclass"
```

**Search by country:**
```bash
python scripts/digital_product_ads_scraper.py --country GB
python scripts/digital_product_ads_scraper.py --country CA
```

**See the browser scraping live (for debugging):**
```bash
python scripts/digital_product_ads_scraper.py --no-headless
```

## What It Does

The scraper searches Meta Ads Library for digital product ads and automatically:

✓ **Identifies creators** (filters out big brands like Nike, Amazon, etc.)  
✓ **Categorizes products** (courses, coaching, ebooks, templates, SaaS, etc.)  
✓ **Extracts key data**:
  - Creator name
  - Product name
  - Ad copy (first 500 chars)
  - Call-to-action text
  - Images/videos if present

✓ **Analyzes patterns**:
  - Most common product types
  - Top keywords being used
  - Most active creators
  - Which CTAs work

## Default Search Terms

By default it searches for these keywords:

**Courses & Training:**
- online course, masterclass, training program, bootcamp, certification course

**Coaching:**
- coaching, consulting, mentorship, business coaching, life coaching

**Content:**
- ebook, guide, workbook, digital book

**Templates & Resources:**
- template, presets, Notion template, Canva template

**Memberships:**
- membership, community, private community

**Tools & SaaS:**
- software, tool, app, platform

## Output Format

Results are saved to `./data/meta_ads/digital_products/` as JSON:

```json
{
  "scraped_at": "2026-09-05T12:34:56.789Z",
  "ad_count": 42,
  "ads": [
    {
      "id": "online course_0",
      "creator_name": "John Doe",
      "product_name": "Complete Digital Marketing Masterclass",
      "product_type": "course",
      "ad_copy": "Learn how to build a 6-figure business online...",
      "cta_text": "Enroll Now",
      "image_url": "https://...",
      "video_url": null,
      "keywords_found": ["online course", "training program"],
      "platform": "facebook,instagram",
      "scraped_at": "2026-09-05T12:34:56.789Z"
    },
    // ... more ads
  ]
}
```

## Analysis Report

After scraping, you get an automatic analysis showing:

```
DIGITAL PRODUCT ADS ANALYSIS
============================================================
{
  "total_ads": 42,
  "unique_creators": 18,
  "product_types": {
    "course": 24,
    "coaching": 12,
    "template": 4,
    "ebook": 2
  },
  "top_keywords": [
    {"keyword": "online course", "count": 18},
    {"keyword": "coaching", "count": 12},
    {"keyword": "masterclass", "count": 9}
  ],
  "top_creators": [
    {
      "name": "John Doe",
      "ad_count": 8,
      "product_types": ["course"]
    },
    {
      "name": "Jane Smith",
      "ad_count": 6,
      "product_types": ["coaching", "course"]
    }
  ]
}
```

## Use Cases for Niche Research

### 1. **Market Demand Analysis**
```bash
# See what's actually selling in your niche
python scripts/digital_product_ads_scraper.py --search "digital marketing"
# Shows: top product types, most active creators, popular CTAs
```

### 2. **Competitor Intelligence**
```bash
# Find who's advertising in your space
python scripts/digital_product_ads_scraper.py --search "social media marketing" "content marketing"
# Identify: biggest competitors, their messaging, their positioning
```

### 3. **Trend Spotting**
```bash
# Discover emerging product categories
python scripts/digital_product_ads_scraper.py --search "ai" "automation"
# Find: new product types, emerging keywords, market shifts
```

### 4. **Messaging Research**
```bash
# See what copy gets ad spend
python scripts/digital_product_ads_scraper.py --search "business coaching"
# Analyze: common pain points, benefits highlighted, urgency tactics
```

## Programmatic Usage

```python
import asyncio
from scripts.digital_product_ads_scraper import DigitalProductAdsScraper

async def analyze_niche():
    scraper = DigitalProductAdsScraper()
    
    # Search for ads
    ads = await scraper.search_digital_products(
        search_terms=["digital marketing course", "seo training"],
        country="US",
        headless=True
    )
    
    # Save results
    filepath = scraper.save_results("my_niche_analysis.json")
    
    # Get insights
    analysis = scraper.analyze_results()
    
    # Print top creators
    for creator in analysis["top_creators"]:
        print(f"{creator['name']}: {creator['ad_count']} ads")
    
    # Print trending keywords
    for keyword_data in analysis["top_keywords"]:
        print(f"  {keyword_data['keyword']}: {keyword_data['count']} uses")

asyncio.run(analyze_niche())
```

## Analyzing Previous Results

Already scraped data? Analyze it without re-scraping:

```bash
python scripts/digital_product_ads_scraper.py \
  --analyze-file data/meta_ads/digital_products/digital_products_20260905_123456.json
```

## Advanced: Custom Search Terms

Create a custom search list:

```python
# my_research.py
import asyncio
from scripts.digital_product_ads_scraper import DigitalProductAdsScraper

async def research_niche():
    scraper = DigitalProductAdsScraper()
    
    custom_searches = [
        "AI course",
        "machine learning bootcamp", 
        "data science training",
        "coding tutorial",
        "python programming"
    ]
    
    ads = await scraper.search_digital_products(
        search_terms=custom_searches,
        country="US"
    )
    
    scraper.save_results("ai_niche_research.json")
    
    # Analyze
    analysis = scraper.analyze_results()
    print(f"Found {analysis['total_ads']} AI-related digital product ads")
    print(f"From {analysis['unique_creators']} different creators")

asyncio.run(research_niche())
```

## Tips for Best Results

1. **Use specific, narrow terms** - "Python course" finds more relevant results than just "course"

2. **Search related keywords** - If researching email marketing:
   ```bash
   python scripts/digital_product_ads_scraper.py \
     --search "email marketing" "email course" "email automation"
   ```

3. **Check different countries** - Same product may have different messaging:
   ```bash
   python scripts/digital_product_ads_scraper.py --search "business coaching" --country GB
   python scripts/digital_product_ads_scraper.py --search "business coaching" --country AU
   ```

4. **Save results by niche** - Organize your research:
   ```bash
   # Run multiple searches
   python scripts/digital_product_ads_scraper.py --search "fitness coaching"
   # Results auto-save with timestamp
   ```

5. **Track changes over time** - Compare how market evolves:
   ```bash
   # Week 1: Save baseline
   python scripts/digital_product_ads_scraper.py --search "AI course" > week1.json
   
   # Week 2: Compare
   python scripts/digital_product_ads_scraper.py --search "AI course" > week2.json
   # Analyze what's new, what's trending
   ```

## What Patterns to Look For

When analyzing results:

- **Product Type Distribution** - Which type of digital product dominates?
- **Creator Activity** - Who's spending the most on ads?
- **Keyword Trends** - Which words appear most in ad copy?
- **CTA Patterns** - What action words convert best?
- **Messaging Themes** - What pain points are being addressed?
- **Visual Strategy** - Are they using images or videos primarily?

## Limitations

- Meta Ads Library may have rate limiting - be respectful with searches
- Scraper extracts text-based data only (creative strategy visible in copy)
- Results depend on Meta's UI - if their selectors change, script may need updates
- Geo-targeted ads may differ by region

## Troubleshooting

**No ads found:**
- Try broader search terms
- Check country code is valid
- May be throttled by Meta - wait and try again

**Scraper hangs:**
- Use `--no-headless` to see what's happening
- Try individual search terms instead of batches
- Check your internet connection

**Browser won't open:**
- Ensure Playwright is installed: `pip install playwright`
- Install browser: `playwright install chromium`

## Next Steps

Once you have the data:

1. **Extract best practices** - What are successful creators doing?
2. **Identify market gaps** - What products aren't advertised?
3. **Benchmark messaging** - Compare your copy to top performers
4. **Track competitors** - Set up regular monitoring of key competitors
5. **Plan your product** - Use insights to inform your offering
